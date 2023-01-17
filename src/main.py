from fastapi import FastAPI

from parking.router import router as parking_router
from db.base import Base
from db.session import engine

# Temporarily init database in code instead of alembic
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(parking_router, prefix="/parking", tags=["Parking"])


@app.get("/")
async def root():
    return {"hello": "world"}
