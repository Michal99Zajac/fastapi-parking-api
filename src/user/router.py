from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.cryptography import verify_password
from auth.dependencies import AuthGuard
from auth.exceptions import invalid_password_exception
from db.dependencies import get_db
from db.models import User
from user.tools import pick_out_permissions

from .crud import user_crud
from .exceptions import RoleDoesntExistException, UserAlreadyExistsException
from .schemas import CreateUserSchema, UpdatePasswordSchema, UpdateUserSchema, UserSchema

router = APIRouter()


@router.get(
    "/me/", response_model=UserSchema, status_code=status.HTTP_200_OK, name="Get current user"
)
async def get_current_user(user: User = Depends(AuthGuard(["user:read"]))) -> UserSchema:
    """
    Get current user informations
    """
    return user


@router.put(
    "/me/", response_model=UserSchema, status_code=status.HTTP_200_OK, name="Update current user"
)
async def update_current_user(
    user_in: UpdateUserSchema,
    db: Session = Depends(get_db),
    user: User = Depends(AuthGuard(["user:read", "user:update"])),
) -> UserSchema:
    """
    Update current user without password
    """
    return user_crud.update(db, db_obj=user, obj_in=user_in)


@router.delete(
    "/me/", response_model=str, status_code=status.HTTP_200_OK, name="Delete current user"
)
async def delete_current_user(
    password: str,
    user: User = Depends(AuthGuard(["user:read", "user:delete"])),
    db: Session = Depends(get_db),
) -> str:
    """
    Delete current user
    """
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
async def update_current_user_password(
    body: UpdatePasswordSchema,
    user: User = Depends(AuthGuard(["user:read", "user:update"])),
    db: Session = Depends(get_db),
) -> str:
    """
    Update current user password
    """
    user_crud.update_password(db, db_obj=user, new_password=body.password)
    return "Password has been updated"


@router.get(
    "/me/permissions/",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
)
async def get_current_user_permissions(user: User = Depends(AuthGuard(["user:read"]))) -> list[str]:
    """
    Get current user permissions
    """
    return pick_out_permissions(user)


@router.post("/register/", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def register_new_user(body: CreateUserSchema, db: Session = Depends(get_db)) -> UserSchema:
    """
    Register new user in app
    """
    try:
        new_user = user_crud.create(db, obj_in=body)
    except (RoleDoesntExistException, UserAlreadyExistsException) as error:
        raise HTTPException(status_code=error.status, detail=error.message)

    return new_user
