from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timezone
from db.engine import get_async_db
from models.appointments import Appointment, AppointmentStatus
from models.users import Users
from models.car import Car
from models.services import Service
from models.mechanics import Mechanic
from schemas.appointments import AppointmentCreate, AppointmentRead, AppointmentUpdate
from utils.email import send_email

router = APIRouter()


async def validate_user(user_id: int, db: AsyncSession):
    """Validate if a user exists."""
    stmt = select(Users).where(Users.user_id == user_id)
    user = (await db.execute(stmt)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


async def validate_car(car_id: int, user_id: int, db: AsyncSession):
    """Validate if a car exists and belongs to the user."""
    stmt = select(Car).where(Car.car_id == car_id)
    car = (await db.execute(stmt)).scalar_one_or_none()
    if not car:
        raise HTTPException(status_code=404, detail=f"Car with ID {car_id} not found.")
    if car.user_id != user_id:
        raise HTTPException(
            status_code=400,
            detail=f"Car with ID {car_id} does not belong to User with ID {user_id}."
        )
    return car


async def validate_service(service_id: int, db: AsyncSession):
    """Validate if a service exists."""
    stmt = select(Service).where(Service.service_id == service_id)
    service = (await db.execute(stmt)).scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail=f"Service with ID {service_id} not found.")
    return service


async def validate_mechanic(mechanic_id: int, db: AsyncSession):
    """Validate if a mechanic exists."""
    stmt = select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
    mechanic = (await db.execute(stmt)).scalar_one_or_none()
    if not mechanic:
        raise HTTPException(status_code=404, detail=f"Mechanic with ID {mechanic_id} not found.")
    return mechanic


@router.post("/", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: AppointmentCreate, db: AsyncSession = Depends(get_async_db)):
    """Create a new appointment with validation."""
    await validate_user(appointment.user_id, db)
    await validate_car(appointment.car_id, appointment.user_id, db)
    await validate_service(appointment.service_id, db)
    if appointment.mechanic_id:
        await validate_mechanic(appointment.mechanic_id, db)

    try:
        appointment_date = datetime.fromisoformat(appointment.appointment_date.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD format.")

    if appointment_date <= datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Appointment date must be in the future.")

    new_appointment = Appointment(
        user_id=appointment.user_id,
        car_id=appointment.car_id,
        service_id=appointment.service_id,
        mechanic_id=appointment.mechanic_id,
        appointment_date=appointment_date,
        status=appointment.status,
    )
    db.add(new_appointment)
    await db.commit()
    await db.refresh(new_appointment)

    user_stmt = select(Users).where(Users.user_id == appointment.user_id)
    user = (await db.execute(user_stmt)).scalar_one_or_none()
    if user:
        email_body = (
            f"Dear {user.name},\n\n"
            f"Your appointment has been confirmed:\n"
            f"Date: {appointment_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Service: {appointment.service_id}\n"
            f"Thank you for choosing our service!"
        )
        send_email(user.email, "Appointment Confirmation", email_body)
    return new_appointment


@router.get("/", response_model=list[AppointmentRead])
async def get_all_appointments(db: AsyncSession = Depends(get_async_db)):
    """Retrieve all appointments."""
    stmt = select(Appointment)
    appointments = (await db.execute(stmt)).scalars().all()
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentRead)
async def get_appointment(appointment_id: int, db: AsyncSession = Depends(get_async_db)):
    """Retrieve an appointment by ID."""
    stmt = select(Appointment).where(Appointment.appointment_id == appointment_id)
    appointment = (await db.execute(stmt)).scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")
    return appointment


@router.put("/{appointment_id}", response_model=AppointmentRead)
async def update_appointment(appointment_id: int, updated_appointment: AppointmentUpdate, db: AsyncSession = Depends(get_async_db)):
    """Update appointment details."""
    stmt = select(Appointment).where(Appointment.appointment_id == appointment_id)
    appointment = (await db.execute(stmt)).scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")

    if updated_appointment.appointment_date:
        try:
            appointment_date = datetime.fromisoformat(updated_appointment.appointment_date.replace("Z", "+00:00"))
            if appointment_date <= datetime.now(timezone.utc):
                raise HTTPException(status_code=400, detail="Appointment date must be in the future.")
            updated_appointment.appointment_date = appointment_date
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD format.")

    for key, value in updated_appointment.dict(exclude_unset=True).items():
        setattr(appointment, key, value)

    await db.commit()
    await db.refresh(appointment)
    return appointment


@router.patch("/{appointment_id}/status", response_model=AppointmentRead)
async def update_appointment_status(appointment_id: int, status: AppointmentStatus, db: AsyncSession = Depends(get_async_db)):
    """Update the status of an appointment."""
    stmt = select(Appointment).where(Appointment.appointment_id == appointment_id)
    appointment = (await db.execute(stmt)).scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")

    appointment.status = status
    await db.commit()
    await db.refresh(appointment)
    return appointment


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, db: AsyncSession = Depends(get_async_db)):
    """Delete an appointment."""
    stmt = select(Appointment).where(Appointment.appointment_id == appointment_id)
    appointment = (await db.execute(stmt)).scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found.")

    await db.delete(appointment)
    await db.commit()
    return {"message": f"Appointment with ID {appointment_id} has been deleted."}
