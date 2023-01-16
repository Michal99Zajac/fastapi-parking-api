from fastapi import FastAPI

from parking.router import router as parking_router

app = FastAPI()

app.include_router(parking_router)


@app.get("/")
async def root():
    return {"hello": "world"}
