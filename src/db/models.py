# Import all the models, so that Base has them before being
# imported by Alembic
from src.bookings.models import Booking  # noqa: F401
from src.db.base import Base  # noqa: F401
from src.parking.models import Parking, ParkingAddress  # noqa: F401
from src.user.models import Permission, Role, User  # noqa: F401
