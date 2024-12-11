import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from models.appointments import Appointment, AppointmentStatus


@pytest.fixture
def appointment_data():
    """Fixture with data for appointment record."""
    future_date = (
            datetime.now(timezone.utc) + timedelta(days=1)
    ).replace(microsecond=0)
    return {
        "user_id": 1,
        "car_id": 1,
        "service_id": 1,
        "mechanic_id": 1,
        "appointment_date": future_date,
        "status": AppointmentStatus.PENDING,
    }


@pytest.mark.asyncio
async def test_create_appointment(
        async_session: AsyncSession,
        appointment_data
):
    """Test creation of appointment record."""
    appointment = Appointment(**appointment_data)
    async_session.add(appointment)
    await async_session.commit()
    await async_session.refresh(appointment)

    assert appointment.appointment_id is not None
    assert appointment.user_id == appointment_data["user_id"]
    assert appointment.car_id == appointment_data["car_id"]
    assert appointment.service_id == appointment_data["service_id"]
    assert appointment.mechanic_id == appointment_data["mechanic_id"]
    assert appointment.status == appointment_data["status"]

    assert (appointment.appointment_date ==
            appointment_data["appointment_date"].replace(tzinfo=None))


@pytest.mark.asyncio
async def test_read_appointment(async_session: AsyncSession, appointment_data):
    """Test reading of appointment record."""
    appointment = Appointment(**appointment_data)
    async_session.add(appointment)
    await async_session.commit()
    await async_session.refresh(appointment)

    fetched_appointment = await async_session.get(
        Appointment,
        appointment.appointment_id
    )
    assert fetched_appointment is not None
    assert fetched_appointment.user_id == appointment.user_id
    assert fetched_appointment.car_id == appointment.car_id
    assert fetched_appointment.service_id == appointment.service_id
    assert fetched_appointment.status == appointment.status


@pytest.mark.asyncio
async def test_update_appointment(
        async_session: AsyncSession,
        appointment_data
):
    """Test updating of appointment record."""
    appointment = Appointment(**appointment_data)
    async_session.add(appointment)
    await async_session.commit()
    await async_session.refresh(appointment)

    new_date = appointment.appointment_date + timedelta(days=1)
    appointment.appointment_date = new_date
    appointment.status = AppointmentStatus.COMPLETED
    await async_session.commit()
    await async_session.refresh(appointment)

    updated_appointment = await async_session.get(
        Appointment,
        appointment.appointment_id
    )
    assert updated_appointment.appointment_date == new_date
    assert updated_appointment.status == AppointmentStatus.COMPLETED


@pytest.mark.asyncio
async def test_delete_appointment(
        async_session: AsyncSession,
        appointment_data
):
    """Test deleting of appointment record."""
    appointment = Appointment(**appointment_data)
    async_session.add(appointment)
    await async_session.commit()
    await async_session.refresh(appointment)

    await async_session.delete(appointment)
    await async_session.commit()

    deleted_appointment = await async_session.get(
        Appointment,
        appointment.appointment_id
    )
    assert deleted_appointment is None
