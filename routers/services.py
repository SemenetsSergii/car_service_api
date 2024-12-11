from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.engine import get_async_db
from models.services import Service
from schemas.services import (
    ServiceCreate,
    ServiceRead,
    ServiceUpdate
)

router = APIRouter()


async def get_service_by_id(service_id: int, db: AsyncSession) -> Service:
    """
    Helper function to fetch a service by ID.
    """
    stmt = select(Service).where(Service.service_id == service_id)
    result = await db.execute(stmt)
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found.")
    return service


@router.post(
    "/",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED
)
async def create_service(
    service: ServiceCreate, db: AsyncSession = Depends(get_async_db)
):
    """
    Create a new service. Checks for duplicate service names.
    """
    stmt = select(Service).where(Service.name == service.name)
    existing_service = (await db.execute(stmt)).scalar_one_or_none()
    if existing_service:
        raise HTTPException(
            status_code=400,
            detail=f"A service with the name '{service.name}' already exists.",
        )

    new_service = Service(**service.dict())
    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)
    return new_service


@router.get("/", response_model=list[ServiceRead])
async def get_all_services(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all services.
    """
    stmt = select(Service)
    services = (await db.execute(stmt)).scalars().all()
    if not services:
        raise HTTPException(status_code=404, detail="No services found.")
    return services


@router.get("/{service_id}", response_model=ServiceRead)
async def get_service(
        service_id: int,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Retrieve a service by ID.
    """
    return await get_service_by_id(service_id, db)


@router.put("/{service_id}", response_model=ServiceRead)
async def update_service(
    service_id: int,
    updated_service: ServiceUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    """
    Update service details.
    """
    service = await get_service_by_id(service_id, db)

    if updated_service.name and updated_service.name != service.name:
        stmt = select(Service).where(Service.name == updated_service.name)
        existing_service = (await db.execute(stmt)).scalar_one_or_none()
        if existing_service:
            raise HTTPException(
                status_code=400,
                detail=f"A service with the name "
                       f"'{updated_service.name}' already exists.",
            )

    for key, value in updated_service.dict(exclude_unset=True).items():
        setattr(service, key, value)

    await db.commit()
    await db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
        service_id: int,
        db: AsyncSession = Depends(get_async_db)
):
    """
    Delete a service.
    """
    service = await get_service_by_id(service_id, db)
    await db.delete(service)
    await db.commit()
    return {"message": f"Service with ID {service_id} has been deleted."}
