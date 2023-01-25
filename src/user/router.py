from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.dependencies import for_user, get_current_user, only_admin
from db.dependencies import get_db
from user.tools import pick_out_roles

from .crud import user_crud
from .models import User
from .schemas import CreateUserSchema, UserSchema

router = APIRouter()


@router.get(
    "/",
    response_model=list[UserSchema],
    dependencies=[Depends(only_admin)],
    status_code=status.HTTP_200_OK,
)
async def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    return user_crud.get_multi(db)


@router.post(
    "/",
    response_model=str,
    description="create new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(create_user: CreateUserSchema, db: Session = Depends(get_db)):
    """Create new user with hashed password"""
    try:
        user_crud.create(db, obj_in=create_user)
        return "User created"
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


@router.get(
    "/me/", response_model=UserSchema, status_code=status.HTTP_200_OK, name="Get current user"
)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.get(
    "/me/permissions/",
    response_model=list[str],
    name="Get authenticated user permissions",
    status_code=status.HTTP_200_OK,
)
async def get_user_permissions(user: User = Depends(for_user)):
    return pick_out_roles(user)


@router.get(
    "/{user_id}/",
    response_model=UserSchema,
    dependencies=[Depends(only_admin)],
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by id"""
    db_user = user_crud.get(db, user_id)

    # check if user exists
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user
