from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth.dependencies import AuthGuard
from src.db.dependencies import get_db
from src.db.models import User
from src.dependencies import PaginationQuery
from src.exceptions import not_found_exception
from src.user.crud import user_crud
from src.user.exceptions import RoleDoesntExistException, UserAlreadyExistsException
from src.user.schemas import CreateUserSchema, UpdatePasswordSchema, UpdateUserSchema, UserSchema

router = APIRouter(prefix="/users")


@router.get(
    "/",
    response_model=list[UserSchema],
    dependencies=[Depends(AuthGuard(admin=True))],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    pagination: PaginationQuery = Depends(), db: Session = Depends(get_db)
) -> list[User]:
    """
    Get all users in database
    """
    return user_crud.get_multi(db, page=pagination.page, limit=pagination.limit)


@router.post(
    "/",
    response_model=UserSchema,
    dependencies=[Depends(AuthGuard(admin=True))],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(body: CreateUserSchema, db: Session = Depends(get_db)) -> User:
    """
    Create new user in database
    """

    try:
        new_user = user_crud.create(db, obj_in=body)
    except (RoleDoesntExistException, UserAlreadyExistsException) as error:
        raise HTTPException(status_code=error.status, detail=error.message)
    return new_user


@router.get(
    "/{user_id}/",
    response_model=UserSchema,
    dependencies=[Depends(AuthGuard(admin=True))],
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: str, db: Session = Depends(get_db)) -> User:
    """
    Get specific user
    """
    user = user_crud.get(db, id=user_id)

    if not user:
        raise not_found_exception()

    return user


@router.delete(
    "/{user_id}/",
    response_model=str,
    dependencies=[Depends(AuthGuard(admin=True))],
    status_code=status.HTTP_200_OK,
)
async def delete_user(user_id: str, db: Session = Depends(get_db)) -> str:
    """
    Delete user from the database
    """
    user_crud.delete(db, id=user_id)
    return "User has been deleted"


@router.put(
    "/{user_id}/",
    response_model=UserSchema,
    dependencies=[Depends(AuthGuard(admin=True))],
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: str, user_in: UpdateUserSchema, db: Session = Depends(get_db)
) -> User:
    """
    Update user data without password
    """
    # get user
    user = user_crud.get(db, id=user_id)

    # user doesn't exist
    if not user:
        raise not_found_exception()

    # update user data
    updated_user = user_crud.update(db, db_obj=user, obj_in=user_in)
    return updated_user


@router.patch(
    "/{user_id}/password/",
    response_model=str,
    dependencies=[Depends(AuthGuard(admin=True))],
    status_code=status.HTTP_200_OK,
)
async def update_user_password(
    user_id: str, body: UpdatePasswordSchema, db: Session = Depends(get_db)
) -> str:
    """
    Update user password
    """
    # get user
    user = user_crud.get(db, user_id)

    # user doesn't exist
    if not user:
        raise not_found_exception()

    # update password
    user_crud.update_password(db, db_obj=user, new_password=body.password)
    return "Password has been updated"
