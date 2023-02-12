from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from src.auth.dependencies import get_current_user
from src.db.dependencies import get_db
from src.db.models import Parking, User
from src.dependencies import PaginationQuery
from src.exceptions import forbidden_exception
from src.parking.schemas import CreateParkingSchema, ParkingSchema

from .crud import parking_crud

router = APIRouter()


@router.get("/", response_model=list[ParkingSchema], status_code=status.HTTP_200_OK)
async def get_all_parkings(
    pagination: PaginationQuery = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Parking]:
    """Get all user parkings"""
    parkings = parking_crud.get_multi_by_owner(
        db, page=pagination.page, limit=pagination.limit, owner_id=current_user.id
    )
    return parkings


@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_parking(
    new_parking: CreateParkingSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> str:
    """Create new parking to current user"""
    parking_crud.create(db, obj_in=new_parking, user=current_user)
    return "Parking's been created"


@router.get("/{parking_id}/", response_model=ParkingSchema, status_code=status.HTTP_200_OK)
async def get_parking(
    parking_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Parking:
    parking = parking_crud.get_by_owner(db, parking_id=parking_id, owner_id=current_user.id)

    if not parking:
        raise forbidden_exception(
            detail="parking doesn't exist or you don't have access to resources"
        )

    return parking


@router.delete("/{parking_id}/", response_model=str, status_code=status.HTTP_200_OK)
async def delete_parking(
    parking_id: UUID4, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> str:
    # find parking
    parking = parking_crud.get_by_owner(db, parking_id=parking_id, owner_id=current_user.id)

    if not parking:
        raise forbidden_exception(
            detail="parking doesn't exist or you don't have access to resources"
        )

    # delete parking
    parking_crud.delete(db, id=parking.id)
    return "Parking has been deleted"
