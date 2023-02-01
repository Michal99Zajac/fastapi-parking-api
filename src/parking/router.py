from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from db.dependencies import get_db
from dependencies import PaginationQuery
from parking.models import Parking
from parking.schemas import CreateParkingSchema, ParkingSchema, UpdateParkingSchema
from user.models import User

from .crud import parking_crud

router = APIRouter()


@router.get("/", response_model=list[ParkingSchema], status_code=status.HTTP_200_OK)
async def get_all_parkings(
    pagination: PaginationQuery = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all user parkings"""
    parkings = parking_crud.get_by_owner(
        db, page=pagination.page, limit=pagination.limit, owner_id=current_user.id
    )
    return parkings


@router.post("/", response_model=str, status_code=status.HTTP_201_CREATED)
async def create_parking(
    new_parking: CreateParkingSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create new parking to current user"""
    parking_crud.create(db, obj_in=new_parking, user=current_user)
    return "Parking's been created"
