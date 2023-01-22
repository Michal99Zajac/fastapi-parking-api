from pydantic import UUID4, BaseModel, EmailStr


class BaseUserModel(BaseModel):
    email: EmailStr


class CreateUserModel(BaseUserModel):
    password: str


class UpdateUserModel(BaseUserModel):
    password: str


class UserInDBModel(BaseUserModel):
    id: UUID4

    class Config:
        orm_mode = True


class UserModel(UserInDBModel):
    pass
