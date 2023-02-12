from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.crud import CRUD
from src.db.models import Parking, ParkingAddress, User

from .schemas import CreateParkingSchema, UpdateParkingSchema


class ParkingCRUD(CRUD[Parking, CreateParkingSchema, UpdateParkingSchema]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: Any, limit: int = 50, page: int = 0
    ) -> list[Parking]:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner_id)
            .offset(page * limit)
            .limit(limit)
            .all()
        )

    def get_by_owner(self, db: Session, *, owner_id: Any, parking_id: Any) -> Parking | None:
        return (
            db.query(self.model)
            .filter(self.model.owner_id == owner_id and self.model.id == parking_id)
            .first()
        )

    def create(self, db: Session, *, obj_in: CreateParkingSchema, user: User) -> Parking:  # type: ignore[override]
        obj_in_data = jsonable_encoder(obj_in)  # transfer data to dict

        # create address model object
        address_data = obj_in_data.pop("address")
        db_parking_address = ParkingAddress(**address_data)

        # create parking
        db_obj: Parking = self.model(**obj_in_data, address=db_parking_address, owner=user)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


parking_crud = ParkingCRUD(Parking)
