from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import UUID4
from sqlalchemy.orm import Session

from db.dependencies import get_db
from db.models import User
from exceptions import forbidden_exception
from settings import SECRET_KEY
from user.crud import user_crud
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
        id: Union[UUID4, None] = payload.get("sub")

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


class AuthGuard:
    """
    Authorization guard

    Class allows to check if user is an admin or has required permissions.
    """

    def __init__(self, permissions: list[str] = [], *, admin: bool = False) -> None:
        self.permissions = permissions
        self.admin = admin

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if self.admin:
            # check if user is admin
            if self._is_admin(current_user):
                # return the current user
                return current_user

            raise forbidden_exception()

        # forbidden if user doesn't have all permissions
        if not self._is_authorized(current_user):
            raise forbidden_exception()

        # return the current user
        return current_user

    def _is_admin(self, user: User) -> bool:
        """
        Check if user is an admin
        """
        # get user role names
        roles_names = map(lambda role: role.name, user.roles)

        # check if admin
        return "admin" in roles_names

    def _is_authorized(self, user: User) -> bool:
        """
        Check if user is authorized.
        """
        # pick out the permissions
        user_permissions = pick_out_permissions(user)

        # check if user has all required permissions
        authorized = all([permission in user_permissions for permission in self.permissions])

        return authorized
