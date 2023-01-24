from fastapi import Depends, FastAPI
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from auth.router import router as auth_router
from db.dependencies import get_db
from parking.router import router as parking_router
from user.models import Role
from user.router import router as user_router

app = FastAPI()

app.include_router(parking_router, prefix="/parkings", tags=["Parking"])
app.include_router(user_router, prefix="/users", tags=["User"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])


@app.get("/")
async def root():
    return {"hello": "world"}


@app.get("/roles")
async def get_roles_with_permissions(db: Session = Depends(get_db)):
    role = db.query(Role).first()

    print(jsonable_encoder(role.permissions))

    return role
