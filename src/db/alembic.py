# Import all the models, so that Base has them before being
# imported by Alembic
from db.base import Base  # type: ignore
from parking.models import Parking, ParkingAddress  # type: ignore
from user.models import Permission, Role, User  # type: ignore
