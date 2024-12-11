import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import text
from db.engine import get_async_db, engine
from models.users import Users
from models.car import Car
from models.services import Service
from models.mechanics import Mechanic
from models.appointments import Appointment


async def load_data():
    with open("example_data.json", "r") as file:
        data = json.load(file)

    async for session in get_async_db():
        try:
            print("Clearing tables...")
            await session.execute(text("DELETE FROM appointments"))
            await session.execute(text("DELETE FROM cars"))
            await session.execute(text("DELETE FROM services"))
            await session.execute(text("DELETE FROM mechanics"))
            await session.execute(text("DELETE FROM users"))
            await session.commit()
            print("Tables cleared.")

            print("Adding users...")
            for user in data["users"]:
                session.add(Users(**user))
            await session.commit()
            print("Users added.")

            print("Adding cars...")
            for car in data["cars"]:
                session.add(Car(**car))
            await session.commit()
            print("Cars added.")

            print("Adding services...")
            for service in data["services"]:
                session.add(Service(**service))
            await session.commit()
            print("Services added.")

            print("Adding mechanics...")
            for mechanic in data["mechanics"]:
                session.add(Mechanic(**mechanic))
            await session.commit()
            print("Mechanics added.")

            print("Adding appointments...")
            for appointment in data["appointments"]:
                session.add(Appointment(**appointment))
            await session.commit()
            print("Appointments added.")

        except Exception as e:
            await session.rollback()
            print(f"Error: {e}")
        finally:
            await session.close()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(load_data())
