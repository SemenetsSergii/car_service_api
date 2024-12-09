from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import argon2
from db.engine import get_async_db
from models import Car, Service
from models.mechanics import Mechanic
from models.appointments import Appointment
from schemas.mechanics import MechanicCreate, MechanicRead, MechanicUpdate
from schemas.appointments import AppointmentRead

router = APIRouter()


async def is_login_unique(login: str, db: AsyncSession) -> bool:
    """Check if a mechanic login is unique."""
    stmt = select(Mechanic).where(Mechanic.login == login)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is None


@router.get("/", response_model=list[MechanicRead])
async def get_all_mechanics(db: AsyncSession = Depends(get_async_db)):
    """Retrieve all mechanics."""
    stmt = select(Mechanic)
    mechanics = (await db.execute(stmt)).scalars().all()
    if not mechanics:
        raise HTTPException(status_code=404, detail="No mechanics found.")
    return mechanics


@router.get("/{mechanic_id}", response_model=MechanicRead)
async def get_mechanic(mechanic_id: int, db: AsyncSession = Depends(get_async_db)):
    """Retrieve a mechanic by ID."""
    stmt = select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
    mechanic = (await db.execute(stmt)).scalar_one_or_none()
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found.")
    return mechanic


@router.post("/", response_model=MechanicRead, status_code=status.HTTP_201_CREATED)
async def create_mechanic(mechanic: MechanicCreate, db: AsyncSession = Depends(get_async_db)):
    """Create a new mechanic."""
    if not await is_login_unique(mechanic.login, db):
        raise HTTPException(status_code=400, detail="Mechanic with this login already exists.")

    hashed_password = argon2.hash(mechanic.password)
    new_mechanic = Mechanic(
        name=mechanic.name,
        birth_date=mechanic.birth_date,
        login=mechanic.login,
        password=hashed_password,
        role=mechanic.role,
        position=mechanic.position,
    )
    db.add(new_mechanic)
    await db.commit()
    await db.refresh(new_mechanic)
    return new_mechanic


@router.put("/{mechanic_id}", response_model=MechanicRead)
async def update_mechanic(mechanic_id: int, updated_mechanic: MechanicUpdate, db: AsyncSession = Depends(get_async_db)):
    """Update mechanic details."""
    stmt = select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
    mechanic = (await db.execute(stmt)).scalar_one_or_none()

    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found.")

    if updated_mechanic.login and updated_mechanic.login != mechanic.login:
        if not await is_login_unique(updated_mechanic.login, db):
            raise HTTPException(status_code=400, detail="Mechanic with this login already exists.")

    if updated_mechanic.password:
        updated_mechanic.password = argon2.hash(updated_mechanic.password)

    for key, value in updated_mechanic.dict(exclude_unset=True).items():
        setattr(mechanic, key, value)

    await db.commit()
    await db.refresh(mechanic)
    return mechanic


@router.delete("/{mechanic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mechanic(mechanic_id: int, db: AsyncSession = Depends(get_async_db)):
    """Delete a mechanic."""
    stmt = select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
    mechanic = (await db.execute(stmt)).scalar_one_or_none()

    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found.")

    await db.delete(mechanic)
    await db.commit()
    return {"message": f"Mechanic with ID {mechanic_id} has been deleted."}
