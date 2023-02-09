from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.dependencies import get_db
from dependencies import PaginationQuery
from user.crud import user_crud
from user.schemas import UserSchema

router = APIRouter(prefix="/users")


@router.get("/", response_model=list[UserSchema], status_code=status.HTTP_200_OK)
async def get_users(
    pagination: PaginationQuery = Depends(), db: Session = Depends(get_db)
) -> list[UserSchema]:
    """
    Get all users in database
    """
    return user_crud.get_multi(db, page=pagination.page, limit=pagination.limit)
