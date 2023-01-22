from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.dependencies import get_db
from parking.crud import get_parking_by_id
from parking.models import Parking
from parking.schemas import CreateParkingSchema, ParkingSchema, UpdateParkingSchema

router = APIRouter()


@router.get(
    "/",
    description="get all parkings",
    status_code=status.HTTP_200_OK,
    response_model=list[ParkingSchema],
)
async def get_parkings(db: Session = Depends(get_db)) -> list[ParkingSchema]:
    return db.query(Parking).all()


@router.get(
    "/{id}",
    description="get parking by id",
    status_code=status.HTTP_200_OK,
    response_model=ParkingSchema,
)
async def get_parking(id: str, db: Session = Depends(get_db)):
    db_parking = get_parking_by_id(db, id)

    # check if parking exists
    if not db_parking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking not found")

    return db_parking


@router.post(
    "/",
    description="create new parking",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
)
async def create_parking(parking: CreateParkingSchema, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking not found")

    # delete parking
    db.delete(db_parking)
    db.commit()

    return "Parking has been deleted"


@router.put(
    "/{id}",
    description="Update parking",
    status_code=status.HTTP_200_OK,
    response_model=ParkingSchema,
)
async def update_parking(
    id: str, updated_parking: UpdateParkingSchema, db: Session = Depends(get_db)
):
    # get parking to update
    db_parking = get_parking_by_id(db, id)

    if not db_parking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parking not found")

    db_parking.name = updated_parking.name
    db.commit()
    return db_parking
