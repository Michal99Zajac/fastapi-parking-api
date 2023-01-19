from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from db.dependencies import get_db
from auth.models import Role
from parking.router import router as parking_router
from auth.routers.user import router as user_router

app = FastAPI()

app.include_router(parking_router, prefix="/parkings", tags=["Parking"])
app.include_router(user_router, prefix="/users", tags=["User"])


@app.get("/")
async def root():
    return {"hello": "world"}


@app.get("/roles")
async def get_roles_with_permissions(db: Session = Depends(get_db)):
    role = db.query(Role).first()

    print(jsonable_encoder(role.permissions))

    return role
