from abc import ABC, abstractmethod
from typing import List
from entity.Vehicle import Vehicle
from entity.Booking import Booking
from entity.Driver import Driver


class ITransportManagementService(ABC):
    @abstractmethod
    def add_vehicle(self, vehicle: Vehicle) -> bool:
        pass

    @abstractmethod
    def update_vehicle(self, vehicle: Vehicle) -> bool:
        pass

    @abstractmethod
    def delete_vehicle(self, vehicle_id: int) -> bool:
        pass

    @abstractmethod
    def schedule_trip(self, vehicle_id: int, route_id: int, departure_date: str, arrival_date: str) -> bool:
        pass

    @abstractmethod
    def cancel_trip(self, trip_id: int) -> bool:
        pass

    @abstractmethod
    def book_trip(self, trip_id: int, passenger_id: int, booking_date: str) -> bool:
        pass

    @abstractmethod
    def cancel_booking(self, booking_id: int) -> bool:
        pass

    @abstractmethod
    def allocate_driver(self, trip_id: int, driver_id: int) -> bool:
        pass

    @abstractmethod
    def deallocate_driver(self, trip_id: int) -> bool:
        pass

    @abstractmethod
    def get_bookings_by_passenger(self, passenger_id: int) -> List[Booking]:
        pass

    @abstractmethod
    def get_bookings_by_trip(self, trip_id: int) -> List[Booking]:
        pass

    @abstractmethod
    def get_available_drivers(self) -> List[Driver]:
        pass