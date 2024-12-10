import pytest

from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession

from models.mechanics import Mechanic, MechanicRole


@pytest.fixture
def mechanic_data():
    """Fixture for mechanic data."""
    return {
        "name": "John Doe",
        "birth_date": date(1990, 5, 15),
        "login": "johndoe",
        "password": "SecureP@ss123",
        "role": MechanicRole.MECHANIC,
        "position": "Technician",
    }


@pytest.mark.asyncio
async def test_create_mechanic(async_session: AsyncSession, mechanic_data):
    """Test creating a mechanic."""
    mechanic = Mechanic(**mechanic_data)
    async_session.add(mechanic)
    await async_session.commit()
    await async_session.refresh(mechanic)

    assert mechanic.mechanic_id is not None
    assert mechanic.name == mechanic_data["name"]
    assert mechanic.login == mechanic_data["login"]
    assert mechanic.role == mechanic_data["role"]


@pytest.mark.asyncio
async def test_read_mechanic(async_session: AsyncSession, mechanic_data):
    """Test reading a mechanic."""
    mechanic = Mechanic(**mechanic_data)
    async_session.add(mechanic)
    await async_session.commit()
    await async_session.refresh(mechanic)

    fetched_mechanic = await async_session.get(Mechanic, mechanic.mechanic_id)
    assert fetched_mechanic is not None
    assert fetched_mechanic.name == mechanic.name
    assert fetched_mechanic.position == mechanic.position


@pytest.mark.asyncio
async def test_update_mechanic(async_session: AsyncSession, mechanic_data):
    """Test updating a mechanic."""
    mechanic = Mechanic(**mechanic_data)
    async_session.add(mechanic)
    await async_session.commit()
    await async_session.refresh(mechanic)

    mechanic.name = "Jane Doe"
    mechanic.position = "Senior Technician"
    await async_session.commit()
    await async_session.refresh(mechanic)

    updated_mechanic = await async_session.get(Mechanic, mechanic.mechanic_id)
    assert updated_mechanic.name == "Jane Doe"
    assert updated_mechanic.position == "Senior Technician"


@pytest.mark.asyncio
async def test_delete_mechanic(async_session: AsyncSession, mechanic_data):
    """Test deleting a mechanic."""
    mechanic = Mechanic(**mechanic_data)
    async_session.add(mechanic)
    await async_session.commit()
    await async_session.refresh(mechanic)

    await async_session.delete(mechanic)
    await async_session.commit()

    deleted_mechanic = await async_session.get(Mechanic, mechanic.mechanic_id)
    assert deleted_mechanic is None
