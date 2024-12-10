import pytest

from models.services import Service


@pytest.fixture
def sample_service_data():
    """Fixture for sample service data."""
    return {
        "name": "Oil Change",
        "description": "Engine oil replacement service",
        "price": 50.0,
        "duration": 30,
    }


@pytest.mark.asyncio
async def test_create_service(async_session, sample_service_data):
    """Test creating a new service."""
    service = Service(**sample_service_data)
    async_session.add(service)
    await async_session.commit()
    await async_session.refresh(service)

    assert service.service_id is not None
    assert service.name == sample_service_data["name"]
    assert service.description == sample_service_data["description"]
    assert service.price == sample_service_data["price"]
    assert service.duration == sample_service_data["duration"]


@pytest.mark.asyncio
async def test_read_service(async_session, sample_service_data):
    """Test reading a service."""
    service = Service(**sample_service_data)
    async_session.add(service)
    await async_session.commit()
    await async_session.refresh(service)

    retrieved_service = await async_session.get(Service, service.service_id)
    assert retrieved_service is not None
    assert retrieved_service.service_id == service.service_id
    assert retrieved_service.name == service.name
    assert retrieved_service.description == service.description
    assert retrieved_service.price == service.price


@pytest.mark.asyncio
async def test_update_service(async_session, sample_service_data):
    """Test updating a service."""
    service = Service(**sample_service_data)
    async_session.add(service)
    await async_session.commit()
    await async_session.refresh(service)

    service.name = "Advanced Oil Change"
    service.price = 70.0
    await async_session.commit()
    await async_session.refresh(service)

    updated_service = await async_session.get(Service, service.service_id)
    assert updated_service.name == "Advanced Oil Change"
    assert updated_service.price == 70.0


@pytest.mark.asyncio
async def test_delete_service(async_session, sample_service_data):
    """Test deleting a service."""
    service = Service(**sample_service_data)
    async_session.add(service)
    await async_session.commit()
    await async_session.refresh(service)

    await async_session.delete(service)
    await async_session.commit()

    deleted_service = await async_session.get(Service, service.service_id)
    assert deleted_service is None
