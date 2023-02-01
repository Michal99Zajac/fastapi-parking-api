from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from db.dependencies import get_db
from exceptions import forbidden_exception
from settings import SECRET_KEY
from user.crud import user_crud
from user.models import User
from user.tools import pick_out_permissions

from .exceptions import unauthhorized_exception
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


def required_permission(permissions: list[str]):
    """return a dependency with a check of the given permissions

    Args:
        permissions (list[str]): required permissions
    """

    async def check_permissions(user: User = Depends(get_current_user)):
        # pick out the permissions
        user_permissions = pick_out_permissions(user)

        # check if user has all required permissions
        allow_to_pass = all([permission in user_permissions for permission in permissions])

        # forbidden if user doesn't have all permissions
        if not allow_to_pass:
            raise forbidden_exception()

        # return the user
        return user

    return check_permissions


async def only_admin(user: User = Depends(get_current_user)):
    # chisel out roles
    roles_names = map(lambda role: role.name, user.roles)

    # check if user has admin role
    if not "admin" in roles_names:
        raise forbidden_exception()

    return user
