from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.dependencies import get_db

from .crud import user_crud
from .schemas import CreateUserSchema, UserSchema

router = APIRouter()


@router.get(
    "/",
    response_model=list[UserSchema],
    description="get all users",
    status_code=status.HTTP_200_OK,
)
async def get_users(db: Session = Depends(get_db)):
    return user_crud.get_multi(db)


@router.post(
    "/",
    response_model=str,
    description="create new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(create_user: CreateUserSchema, db: Session = Depends(get_db)):
    try:
        user_crud.create(db, obj_in=create_user)
        return "User created"
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")


@router.get(
    "/{user_id}",
    response_model=UserSchema,
    description="get user by id",
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = user_crud.get(db, user_id)

    # check if user exists
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user


@router.get(
    "/{user_id}/permissions",
    response_model=list[str],
    description="get user permissions",
    status_code=status.HTTP_200_OK,
)
async def get_user_permissions(user_id: str, db: Session = Depends(get_db)):
    db_user = user_crud.get(db, user_id)

    # check if user exists
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # get all permissions from roles and extract their names
    permissions_subsets: list[list[str]] = [
        map(lambda permission: str(permission.name), role.permissions) for role in db_user.roles
    ]

    # flat the list of subsets
    # see: https://stackoverflow.com/a/45323085
    response: list[str] = []
    for subset in permissions_subsets:
        response.extend(subset)

    # flat the list and remove repetitions
    return list(set(response))
