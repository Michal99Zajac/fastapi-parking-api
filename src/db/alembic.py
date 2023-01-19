# Import all the models, so that Base has them before being
# imported by Alembic
from db.base import Base
from auth.models import User, Role, Permission
from parking.models import Parking
