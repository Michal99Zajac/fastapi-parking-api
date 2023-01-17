from uuid import uuid4
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db.dependencies import get_db
from parking.schemas import CreateParkingModel
from parking.models import Parking

router = APIRouter()


@router.get("/", description="get all parkings", status_code=status.HTTP_200_OK)
async def get_parkings(db: Session = Depends(get_db)):
    return db.query(Parking).all()


@router.post(
    "/",
    description="create new parking",
    status_code=status.HTTP_201_CREATED,
)
async def create_parking(parking: CreateParkingModel, db: Session = Depends(get_db)):
    db_parking = Parking(name=parking.name, id=str(uuid4()))
    db.add(db_parking)
    db.commit()
    return "Parking has been created"


@router.delete("/{id}", description="Delete parking", status_code=status.HTTP_200_OK)
async def delete_parking(id: str, db: Session = Depends(get_db)):
    # get parking to delete
    db_parking = db.get(Parking, {"id": id})

    # check if parking exists
    if not db_parking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parking not found"
        )

    # delete parking
    db.delete(db_parking)
    db.commit()

    return "Parking has been deleted"


@router.put("/{id}", description="Update parking", status_code=status.HTTP_200_OK)
async def update_parking(
    id: str, updated_parking: CreateParkingModel, db: Session = Depends(get_db)
):
    # get parking to update
    db_parking: Parking = db.get(Parking, {"id": id})

    if not db_parking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parking not found"
        )

    db_parking.name = updated_parking.name
    db.commit()
    return "Parking's updated"
