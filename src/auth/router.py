from datetime import timedelta

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.dependencies import get_db

from .exceptions import invalid_credentials_exception
from .schemas import Token
from .settings import ACCESS_TOKEN_EXPIRE_MINUTES
from .utils import authenticate_user, create_access_token

router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
    description="get authentication token",
    status_code=status.HTTP_200_OK,
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    # auth user
    user = authenticate_user(db, form_data.username, form_data.password)

    # check if user is authenticated
    if not user:
        raise invalid_credentials_exception()

    # calculate token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # create token
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    # return new token
    return {"access_token": access_token, "token_type": "bearer"}
