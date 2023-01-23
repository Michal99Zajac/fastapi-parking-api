from pydantic import UUID4, BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    email: EmailStr


class CreateUserSchema(BaseUserSchema):
    password: str


class UpdateUserSchema(BaseUserSchema):
    password: str


class BaseUserDB(BaseUserSchema):
    id: UUID4

    class Config:
        orm_mode = True


class UserSchema(BaseUserDB):
    pass
