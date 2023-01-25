from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db.dependencies import get_db
from settings import SECRET_KEY
from user.crud import user_crud
from user.models import Role, User

from .exceptions import forbidden_exception, unauthhorized_exception
from .schemas import TokenData
from .settings import HASH_ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token/")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    try:
        # decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        id: str = payload.get("sub")

        # token doesn't have encoded user id
        if id is None:
            raise unauthhorized_exception()

        # transform to pydantic model
        token_data = TokenData(id=id)
    except JWTError:
        raise unauthhorized_exception()

    # get full user from database
    user = user_crud.get(db, id=token_data.id)

    # user doesn't exist
    if user is None:
        raise unauthhorized_exception()

    return user


async def for_user(user: User = Depends(get_current_user)):
    # chisel out roles
    roles_names = map(lambda role: role.name, user.roles)

    # check if user has user role
    if not "user" in roles_names:
        raise forbidden_exception()

    return user


async def only_admin(user: User = Depends(get_current_user)):
    # chisel out roles
    roles_names = map(lambda role: role.name, user.roles)

    # check if user has admin role
    if not "admin" in roles_names:
        raise forbidden_exception()

    return user
