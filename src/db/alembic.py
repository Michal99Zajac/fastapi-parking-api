# Import all the models, so that Base has them before being
# imported by Alembic
from db.base import Base
from models import Address
from parking.models import Parking
from user.models import Permission, Role, User
