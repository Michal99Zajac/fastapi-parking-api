from sqlalchemy.orm import Session
from uuid import uuid4

from .models import User, Role
from .schemas import CreateUserModel


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()


def create_user(db: Session, user: CreateUserModel):
    db_user_role = db.query(Role).filter(Role.name == "user").first()

    if not db_user_role:
        raise Exception("Role doesn't exist")

    id = str(uuid4())
    db_user = User(
        email=user.email, password=user.password, roles=[db_user_role], id=id
    )
    db.add(db_user)
    db.commit()
