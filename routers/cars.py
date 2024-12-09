from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.engine import get_async_db
from models.car import Car
from schemas.car import CarCreate, CarRead, CarUpdate

router = APIRouter()


async def validate_car_uniqueness(car_data: dict, db: AsyncSession, car_id: int = None):
    """Validate that the car's plate number and VIN are unique."""
    stmt = select(Car).where(Car.plate_number == car_data["plate_number"])
    if car_id:
        stmt = stmt.where(Car.car_id != car_id)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Car with this plate number already exists.")

    stmt = select(Car).where(Car.vin == car_data["vin"])
    if car_id:
        stmt = stmt.where(Car.car_id != car_id)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Car with this VIN already exists.")


@router.post("/", response_model=CarRead, status_code=status.HTTP_201_CREATED)
async def create_car(car: CarCreate, db: AsyncSession = Depends(get_async_db)):
    """Create a new car."""
    car_data = car.dict()
    await validate_car_uniqueness(car_data, db)

    new_car = Car(**car_data)
    db.add(new_car)
    await db.commit()
    await db.refresh(new_car)
    return new_car


@router.get("/", response_model=list[CarRead])
async def get_all_cars(db: AsyncSession = Depends(get_async_db)):
    """Retrieve all cars."""
    stmt = select(Car)
    cars = (await db.execute(stmt)).scalars().all()
    if not cars:
        raise HTTPException(status_code=404, detail="No cars found.")
    return cars


@router.get("/{car_id}", response_model=CarRead)
async def get_car(car_id: int, db: AsyncSession = Depends(get_async_db)):
    """Retrieve a car by ID."""
    stmt = select(Car).where(Car.car_id == car_id)
    car = (await db.execute(stmt)).scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found.")
    return car


@router.put("/{car_id}", response_model=CarRead)
async def update_car(car_id: int, updated_car: CarUpdate, db: AsyncSession = Depends(get_async_db)):
    """Update car details."""
    stmt = select(Car).where(Car.car_id == car_id)
    car = (await db.execute(stmt)).scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found.")

    updated_car_data = updated_car.dict(exclude_unset=True)
    if "plate_number" in updated_car_data or "vin" in updated_car_data:
        await validate_car_uniqueness(updated_car_data, db, car_id=car_id)

    for key, value in updated_car_data.items():
        setattr(car, key, value)

    await db.commit()
    await db.refresh(car)
    return car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int, db: AsyncSession = Depends(get_async_db)):
    """Delete a car."""
    stmt = select(Car).where(Car.car_id == car_id)
    car = (await db.execute(stmt)).scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found.")

    await db.delete(car)
    await db.commit()
    return {"message": f"Car with ID {car_id} has been deleted."}
