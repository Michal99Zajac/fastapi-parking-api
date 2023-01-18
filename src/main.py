from fastapi import FastAPI

from parking.router import router as parking_router
from auth.routers.user import router as user_router
from db.base import Base
from db.session import engine

# Temporarily init database in code instead of alembic
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(parking_router, prefix="/parkings", tags=["Parking"])
app.include_router(user_router, prefix="/users", tags=["User"])


@app.get("/")
async def root():
    return {"hello": "world"}
