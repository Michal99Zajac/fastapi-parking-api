from datetime import datetime, timedelta
from typing import Literal

from jose import jwt
from sqlalchemy.orm import Session

from settings import SECRET_KEY
from user.crud import user_crud
from user.models import User

from .cryptography import verify_password
from .settings import HASH_ALGORITHM


def authenticate_user(db: Session, email: str, password: str) -> Literal[False] | User:
    user = user_crud.get_by_email(db, email=email)

    # check if user exists
    if not user:
        return False

    # verify password
    if not verify_password(password, user.password):
        return False

    # user is authenticated, return user
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    # copy data to encode
    to_encode = data.copy()

    # calculate expire token time
    # default: 15 minutes
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # insert expire time into data to encode
    to_encode.update({"exp": expire})

    # create token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)

    return encoded_jwt
