# Import all the models, so that Base has them before being
# imported by Alembic
from bookings.models import Booking  # nowa: F401
from db.base import Base  # noqa: F401
from parking.models import Parking, ParkingAddress  # noqa: F401
from user.models import Permission, Role, User  # noqa: F401
