from uuid import UUID

from pydantic import BaseModel


class BaseParkingSchema(BaseModel):
    name: str


class CreateParkingSchema(BaseParkingSchema):
    pass


class UpdateParkingSchema(BaseParkingSchema):
    pass


class ParkingInDBSchema(BaseParkingSchema):
    id: UUID

    class Config:
        orm_mode = True


class ParkingSchema(ParkingInDBSchema):
    pass
