from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from auth.cryptography import verify_password
from auth.dependencies import AuthGuard
from auth.exceptions import invalid_password_exception
from db.dependencies import get_db
from db.models import User
from user.tools import pick_out_permissions

from .crud import user_crud
from .schemas import UpdatePasswordSchema, UpdateUserSchema, UserSchema

router = APIRouter()


@router.get(
    "/me/", response_model=UserSchema, status_code=status.HTTP_200_OK, name="Get current user"
)
async def get_me(user: User = Depends(AuthGuard(["user:read"]))) -> UserSchema:
    return user


@router.put(
    "/me/", response_model=UserSchema, status_code=status.HTTP_200_OK, name="Update current user"
)
async def update_me(
    user_in: UpdateUserSchema,
    db: Session = Depends(get_db),
    user: User = Depends(AuthGuard(["user:read", "user:update"])),
) -> UserSchema:
    # update user
    updated_user = user_crud.update(db, db_obj=user, obj_in=user_in)

    return updated_user


@router.delete(
    "/me/", response_model=str, status_code=status.HTTP_200_OK, name="Delete current user"
)
async def delete_me(
    password: str,
    user: User = Depends(AuthGuard(["user:read", "user:delete"])),
    db: Session = Depends(get_db),
) -> str:
    # verify password
    verified = verify_password(password, user.password)

    # forbidden if password is not correct
    if not verified:
        raise invalid_password_exception()

    # delete user
    user_crud.delete(db, id=user.id)
    return "user has been deleted"


@router.patch(
    "/me/password/",
    response_model=str,
    status_code=status.HTTP_200_OK,
    name="Update current user password",
)
async def update_password(
    password: UpdatePasswordSchema,
    user: User = Depends(AuthGuard(["user:read", "user:update"])),
    db: Session = Depends(get_db),
) -> str:
    user_crud.update_password(db, db_obj=user, new_password=password.password)
    return "Password has been updated"


@router.get(
    "/me/permissions/",
    response_model=list[str],
    name="Get authenticated user permissions",
    status_code=status.HTTP_200_OK,
)
async def get_user_permissions(user: User = Depends(AuthGuard(["user:read"]))) -> list[str]:
    return pick_out_permissions(user)
