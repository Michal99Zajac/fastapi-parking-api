from typing import List
from parking.schemas import ParkingModel


parkings: List[ParkingModel] = [
    ParkingModel(name="Parking 1", address="Address1", owner="Owner 1"),
    ParkingModel(name="Parking 2", address="Address2", owner="Owner 2"),
    ParkingModel(name="Parking 3", address="Address3", owner="Owner 3"),
]
