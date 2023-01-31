from pydantic import UUID4, BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    email: EmailStr


class CreateUserSchema(BaseUserSchema):
    password: str


class UpdateUserSchema(BaseUserSchema):
    ...


class BaseUserInDB(BaseUserSchema):
    id: str

    class Config:
        orm_mode = True


class UserSchema(BaseUserInDB):
    ...
