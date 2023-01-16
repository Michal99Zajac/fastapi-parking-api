from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ParkingModel(BaseModel):
    id: UUID = Field(description="Parking ID", default_factory=uuid4)
    name: str = Field("", description="Parking name")
    address: str = Field("", description="Parking address")
    owner: str = Field("", description="Parking administrator")
