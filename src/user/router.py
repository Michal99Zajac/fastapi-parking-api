from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.cryptography import verify_password
from auth.dependencies import required_permission
from auth.exceptions import invalid_password_exception
from db.dependencies import get_db
from user.tools import pick_out_permissions

from .crud import user_crud
from .models import User
from .schemas import CreateUserSchema, UserSchema

router = APIRouter()

# permissions
read_me_permission = required_permission(["me:read"])
read_user_permission = required_permission(["user:read"])
delete_me_permission = required_permission(["me:delete", "me:read"])
delete_user_permission = required_permission(["user:read", "user:delete"])


@router.get(
    "/",
    response_model=list[UserSchema],
    dependencies=[Depends(read_user_permission)],
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
async def get_me(user: User = Depends(read_me_permission)):
    return user


@router.delete(
    "/me/", response_model=str, status_code=status.HTTP_200_OK, name="Delete current user"
)
async def delete_me(
    password: str, user: User = Depends(delete_me_permission), db: Session = Depends(get_db)
):
    # verify password
    verified = verify_password(password, user.password)

    # forbidden if password is not correct
    if not verified:
        raise invalid_password_exception()

    # delete user
    user_crud.delete(db, id=user.id)
    return "user has been deleted"


# TODO: add data update for user
# TODO: add update for admin


@router.get(
    "/me/permissions/",
    response_model=list[str],
    name="Get authenticated user permissions",
    status_code=status.HTTP_200_OK,
)
async def get_user_permissions(user: User = Depends(read_me_permission)):
    return pick_out_permissions(user)


@router.get(
    "/{user_id}/",
    response_model=UserSchema,
    dependencies=[Depends(read_user_permission)],
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user by id"""
    db_user = user_crud.get(db, user_id)

    # check if user exists
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user


@router.delete(
    "/{user_id}",
    response_model=str,
    dependencies=[Depends(delete_user_permission)],
    status_code=status.HTTP_200_OK,
)
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    # delete user
    user_crud.delete(db, id=user_id)
    return "user has been deleted"
