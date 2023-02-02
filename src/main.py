from fastapi import FastAPI

from auth.router import router as auth_router
from parking.router import router as parking_router
from user.router import router as user_router

app = FastAPI()

app.include_router(parking_router, prefix="/parkings", tags=["Parking"])
app.include_router(user_router, prefix="/users", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
