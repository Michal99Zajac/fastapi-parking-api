from uuid import UUID
from pydantic import BaseModel


class ParkingModel(BaseModel):
    id: UUID
    name: str


class CreateParkingModel(BaseModel):
    name: str
