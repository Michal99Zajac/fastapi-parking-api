from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.cryptography import verify_password
from auth.dependencies import required_permission
from auth.exceptions import invalid_password_exception
from db.dependencies import get_db
from dependencies import PaginationQuery
from exceptions import not_found_exception
from user.tools import pick_out_permissions

from .crud import user_crud
from .models import User
from .schemas import CreateUserSchema, UpdateUserSchema, UserSchema

router = APIRouter()

# permissions
read_me_permission = required_permission(["me:read"])
update_me_permission = required_permission(["me:read", "me:update"])
delete_me_permission = required_permission(["me:delete", "me:read"])
read_user_permission = required_permission(["user:read"])
delete_user_permission = required_permission(["user:read", "user:delete"])
update_user_permission = required_permission(["user:read", "user:update"])


@router.get(
    "/",
    response_model=list[UserSchema],
    dependencies=[Depends(read_user_permission)],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    pagination: PaginationQuery = Depends(), db: Session = Depends(get_db)
) -> list[UserSchema]:
    """Get all users"""
    return user_crud.get_multi(db, page=pagination.page, limit=pagination.limit)


@router.post(
    "/",
    response_model=str,
    description="create new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(create_user: CreateUserSchema, db: Session = Depends(get_db)) -> str:
    """Create new user with hashed password"""
    try:
        user_crud.create(db, obj_in=create_user)
        return "User created"
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


@router.get(
    "/me/", response_model=UserSchema, status_code=status.HTTP_200_OK, name="Get current user"
)
async def get_me(user: User = Depends(read_me_permission)) -> UserSchema:
    return user


@router.put(
    "/me/", response_model=UserSchema, status_code=status.HTTP_200_OK, name="Update current user"
)
async def update_me(
    user_in: UpdateUserSchema,
    db: Session = Depends(get_db),
    user: User = Depends(update_me_permission),
) -> UserSchema:
    # update user
    updated_user = user_crud.update(db, db_obj=user, obj_in=user_in)

    return updated_user


@router.delete(
    "/me/", response_model=str, status_code=status.HTTP_200_OK, name="Delete current user"
)
async def delete_me(
    password: str, user: User = Depends(delete_me_permission), db: Session = Depends(get_db)
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
    password: str, user: User = Depends(update_user_permission), db: Session = Depends(get_db)
) -> str:
    user_crud.update_password(db, db_obj=user, new_password=password)
    return "Password has been updated"


@router.get(
    "/me/permissions/",
    response_model=list[str],
    name="Get authenticated user permissions",
    status_code=status.HTTP_200_OK,
)
async def get_user_permissions(user: User = Depends(read_me_permission)) -> list[str]:
    return pick_out_permissions(user)


@router.get(
    "/{user_id}/",
    response_model=UserSchema,
    dependencies=[Depends(read_user_permission)],
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: str, db: Session = Depends(get_db)) -> UserSchema:
    """Get user by id"""
    db_user = user_crud.get(db, user_id)

    # check if user exists
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user


@router.delete(
    "/{user_id}/",
    response_model=str,
    dependencies=[Depends(delete_user_permission)],
    status_code=status.HTTP_200_OK,
)
async def delete_user(user_id: str, db: Session = Depends(get_db)) -> str:
    # delete user
    deleted_user = user_crud.delete(db, id=user_id)

    # check if user exists
    if not deleted_user:
        raise not_found_exception()

    return "user has been deleted"


@router.put(
    "/{user_id}/",
    response_model=UserSchema,
    dependencies=[Depends(update_user_permission)],
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: str, user_in: UpdateUserSchema, db: Session = Depends(get_db)
) -> UserSchema:
    # find user
    db_user = user_crud.get(db, user_id)

    if not db_user:
        raise not_found_exception()

    # update user
    updated_user = user_crud.update(db, db_obj=db_user, obj_in=user_in)

    return updated_user
