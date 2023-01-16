from fastapi import APIRouter, status

from .data import parkings

router = APIRouter(prefix="/parking", tags=["parking"])


@router.get(
    "/",
    description="get all parkings",
    responses={status.HTTP_200_OK: {"description": "OK"}},
)
def get_parkings():
    return parkings
