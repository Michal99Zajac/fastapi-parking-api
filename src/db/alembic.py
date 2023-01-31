# Import all the models, so that Base has them before being
# imported by Alembic
from db.base import Base
from parking.models import Parking, ParkingAddress
from user.models import Permission, Role, User
