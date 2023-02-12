from pydantic import UUID4, BaseModel, EmailStr, Field


class BaseUserSchema(BaseModel):
    email: EmailStr


class UpdatePasswordSchema(BaseModel):
    password: str = Field(max_length=255)


class CreateUserSchema(BaseUserSchema):
    password: str = Field(max_length=255)


class UpdateUserSchema(BaseUserSchema):
    ...


class BaseUserInDB(BaseUserSchema):
    id: UUID4

    class Config:
        orm_mode = True


class UserSchema(BaseUserInDB):
    ...
