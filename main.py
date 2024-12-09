from fastapi import FastAPI
from routers import users, cars, services, mechanics, appointments

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(cars.router, prefix="/cars", tags=["Cars"])
app.include_router(services.router, prefix="/services", tags=["Services"])
app.include_router(mechanics.router, prefix="/mechanics", tags=["Mechanics"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Car Service API"}
