from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from auth.schemas import UserModel, CreateUserModel
from db.dependencies import get_db
from auth import crud

router = APIRouter()


@router.get(
    "/",
    response_model=list[UserModel],
    description="get all users",
    status_code=status.HTTP_200_OK,
)
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserModel,
    description="get user by id",
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return db_user


@router.post(
    "/",
    response_model=str,
    description="create new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(create_user: CreateUserModel, db: Session = Depends(get_db)):
    try:
        crud.create_user(db, create_user)
        return "User created"
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
