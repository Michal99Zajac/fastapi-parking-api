from pydantic import UUID4, BaseModel

from user.schemas import UserSchema

# PARKING ADDRESS SCHEMA


class ParkingAddressBaseSchema(BaseModel):
    street: str
    zip_code: str
    city: str
    country: str


class ParkingAddressCreateSchema(ParkingAddressBaseSchema):
    ...


class ParkingAddressUpdateSchema(ParkingAddressBaseSchema):
    ...


class ParkingAddressInDB(ParkingAddressBaseSchema):
    id: UUID4

    class Config:
        orm_mode = True


class ParkingAddressSchema(ParkingAddressInDB):
    ...


# PARKING SCHEMA


class ParkingBaseSchema(BaseModel):
    name: str
    address: ParkingAddressBaseSchema


class CreateParkingSchema(ParkingBaseSchema):
    ...


class UpdateParkingSchema(ParkingBaseSchema):
    ...


class ParkingInDBSchema(ParkingBaseSchema):
    id: UUID4
    address: ParkingAddressSchema
    owner: UserSchema

    class Config:
        orm_mode = True


class ParkingSchema(ParkingInDBSchema):
    ...
