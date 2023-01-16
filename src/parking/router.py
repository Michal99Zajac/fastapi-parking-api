from fastapi import APIRouter, status

from parking.schemas import ParkingModel

from .data import parkings

router = APIRouter(prefix="/parking", tags=["parking"])


@router.get(
    "/",
    description="get all parkings",
)
def get_parkings():
    return parkings


@router.post(
    "/",
    description="create new parking",
    status_code=201,
)
def create_parking(parking: ParkingModel):
    parkings.append(parking)
    return "Parking has been created"


@router.delete("/{id}", description="Delete parking", status_code=200)
def delete_parking(id: int):
    global parkings
    parkings = [parking for parking in parkings if parking.id != id]
    return "Parking has been deleted"


@router.put("/{id}", description="Update parking", status_code=200)
def update_parking(id: int, updated_parking: ParkingModel):
    global parkings
    index = [parking.id for parking in parkings].index(id)
    parkings[index] = updated_parking
    return parkings[index]
