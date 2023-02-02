from sqlalchemy.orm import Session

from auth.cryptography import hash_password
from crud import CRUD

from .models import Role, User
from .schemas import CreateUserSchema, UpdateUserSchema


class UserCRUD(CRUD[User, CreateUserSchema, UpdateUserSchema]):
    def create(self, db: Session, *, obj_in: CreateUserSchema) -> User:
        user_role = db.query(Role).filter(Role.name == "user").first()

        # check if role exists
        if not user_role:
            raise Exception("[UserCRUD] Error: role doesn't exist")

        # hash password
        hashed_password = hash_password(obj_in.password)

        # create user instance
        new_user = self.model(email=obj_in.email, password=hashed_password, roles=[user_role])

        # add to the database
        db.add(new_user)
        db.commit()
        return new_user

    def update_password(self, db: Session, *, db_obj: User, new_password: str) -> User:
        # hash new password
        hashed_new_password = hash_password(new_password)

        # set new password
        setattr(db_obj, "password", hashed_new_password)

        # commit changes
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def create_admin(self, db: Session, *, obj_in: CreateUserSchema) -> User:
        all_roles = db.query(Role).all()

        # hash password
        hashed_password = hash_password(obj_in.password)

        # create user instance
        new_admin = self.model(email=obj_in.email, password=hashed_password, roles=all_roles)

        # add to the database
        db.add(new_admin)
        db.commit()
        return new_admin

    def get_by_email(self, db: Session, *, email: str) -> User | None:
        return db.query(self.model).filter(self.model.email == email).first()


user_crud = UserCRUD(User)
