from sqlalchemy.orm import Session

from crud import FullCRUD

from .models import Role, User
from .schemas import CreateUserSchema, UpdateUserSchema


class UserCRUD(FullCRUD[User, CreateUserSchema, UpdateUserSchema]):
    def create(self, db: Session, *, obj_in: CreateUserSchema) -> User:
        user_role = db.query(Role).filter(Role.name == "user").first()

        # check if role exists
        if not user_role:
            raise Exception("[UserCRUD] Error: role doesn't exist")

        # create user instance
        new_user = self.model(email=obj_in.email, password=obj_in.password, roles=[user_role])

        # add to the database
        db.add(new_user)
        db.commit()
        return new_user


user_crud = UserCRUD(User)
