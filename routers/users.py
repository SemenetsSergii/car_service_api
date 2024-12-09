from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import argon2
import jwt
from datetime import datetime, timedelta, timezone
from db.engine import get_async_db
from models.users import Users, UserRole
from schemas.users import UserCreate, UserRead, UserUpdate


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_user_by_email(email: str, db: AsyncSession) -> Users:
    """
    Retrieve a user by their email.
    """
    stmt = select(Users).where(Users.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(user_id: int, db: AsyncSession) -> Users:
    """
    Retrieve a user by their ID.
    """
    stmt = select(Users).where(Users.user_id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


async def validate_user_email_uniqueness(email: str, db: AsyncSession):
    """
    Check if a user with the given email already exists.
    """
    if await get_user_by_email(email, db):
        raise HTTPException(status_code=400, detail="Email already exists.")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)):
    """
    Get the currently authenticated user from the JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token.")
        return await get_user_by_id(user_id, db)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token.")


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Create a new user in the database.
    """
    await validate_user_email_uniqueness(user.email, db)

    hashed_password = argon2.hash(user.password)
    new_user = Users(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role.value,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/auth/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_async_db)):
    """
    Authenticate a user and generate a JWT token.
    """
    user = await get_user_by_email(form_data.username, db)
    if not user or not argon2.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"user_id": user.user_id, "exp": datetime.now(timezone.utc) + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def get_user_profile(current_user: Users = Depends(get_current_user)):
    """
    Retrieve the profile of the currently authenticated user.
    """
    return current_user


@router.get("/", response_model=list[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve all users from the database.
    """
    stmt = select(Users)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Retrieve a user by their ID.
    """
    return await get_user_by_id(user_id, db)


@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, updated_user: UserUpdate, db: AsyncSession = Depends(get_async_db)):
    """
    Update a user's details in the database.
    """
    user = await get_user_by_id(user_id, db)
    if updated_user.email and updated_user.email != user.email:
        await validate_user_email_uniqueness(updated_user.email, db)

    if updated_user.password:
        updated_user.password = argon2.hash(updated_user.password)

    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Delete a user from the database.
    """
    user = await get_user_by_id(user_id, db)
    await db.delete(user)
    await db.commit()
    return {"message": f"User with ID {user_id} has been deleted."}
