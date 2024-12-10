import pytest

from models.car import Car


@pytest.fixture
def sample_car_data():
    """Fixture for sample car data."""
    return {
        "user_id": 1,
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2020,
        "plate_number": "AA1234BB",
        "vin": "1HGCM82633A123456",
    }


@pytest.mark.asyncio
async def test_create_car(async_session, sample_car_data):
    """Test creating a car."""
    car = Car(**sample_car_data)
    async_session.add(car)
    await async_session.commit()
    await async_session.refresh(car)

    assert car.car_id is not None
    assert car.brand == sample_car_data["brand"]
    assert car.model == sample_car_data["model"]
    assert car.year == sample_car_data["year"]
    assert car.plate_number == sample_car_data["plate_number"]
    assert car.vin == sample_car_data["vin"]


@pytest.mark.asyncio
async def test_read_car(async_session, sample_car_data):
    """Test reading a car."""
    car = Car(**sample_car_data)
    async_session.add(car)
    await async_session.commit()
    await async_session.refresh(car)

    retrieved_car = await async_session.get(Car, car.car_id)
    assert retrieved_car is not None
    assert retrieved_car.car_id == car.car_id
    assert retrieved_car.brand == car.brand


@pytest.mark.asyncio
async def test_update_car(async_session, sample_car_data):
    """Test updating a car."""
    sample_car_data["vin"] = "1HGCM82633A123457"
    car = Car(**sample_car_data)
    async_session.add(car)
    await async_session.commit()
    await async_session.refresh(car)

    car.brand = "Honda"
    car.model = "Civic"
    await async_session.commit()
    await async_session.refresh(car)

    updated_car = await async_session.get(Car, car.car_id)
    assert updated_car.brand == "Honda"
    assert updated_car.model == "Civic"


@pytest.mark.asyncio
async def test_delete_car(async_session, sample_car_data):
    """Test deleting a car."""
    sample_car_data["vin"] = "1HGCM82633A123458"
    car = Car(**sample_car_data)
    async_session.add(car)
    await async_session.commit()
    await async_session.refresh(car)

    await async_session.delete(car)
    await async_session.commit()

    deleted_car = await async_session.get(Car, car.car_id)
    assert deleted_car is None
