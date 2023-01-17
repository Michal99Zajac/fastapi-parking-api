from sqlalchemy.orm import Session

from parking.models import Parking


def get_parking_by_id(db: Session, id: str):
    return db.query(Parking).filter(Parking.id == id).first()
