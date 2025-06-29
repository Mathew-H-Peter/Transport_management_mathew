class VehicleNotFoundException(Exception):
    def __init__(self, message="Vehicle not found in the database"):
        self.message = message
        super().__init__(self.message)


class BookingNotFoundException(Exception):
    def __init__(self, message="Booking not found in the database"):
        self.message = message
        super().__init__(self.message)

class TripNotFoundException(Exception):
    def __init__(self, message="Trip not found in the database"):
        self.message = message
        super().__init__(self.message)


class RouteNotFoundException(Exception):
    def __init__(self, message="Route not found in the database"):
        self.message = message
        super().__init__(self.message)

class VehicleNotAvailableException(Exception):
    def __init__(self, message="Vehicle is not available for scheduling."):
        self.message = message
        super().__init__(self.message)

class InvalidVehicleDataException(Exception):
    def __init__(self, message="Invalid or missing vehicle data. All fields are required."):
        self.message = message
        super().__init__(self.message)

class InvalidTripDataException(Exception):
    def __init__(self, message="Invalid or missing trip data. All fields are required."):
        self.message = message
        super().__init__(self.message)

class InvalidBookingDataException(Exception):
    def __init__(self, message="Invalid or missing booking data. All fields are required."):
        self.message = message
        super().__init__(self.message)

class InvalidDriverDataException(Exception):
    def __init__(self, message="Invalid or missing driver data. All fields are required."):
        self.message = message
        super().__init__(self.message)

class InvalidPassengerDataException(Exception):
    def __init__(self, message="Invalid or missing passenger data. All fields are required."):
        self.message = message
        super().__init__(self.message)

class InvalidVehicleStatusException(Exception):
    def __init__(self, message="Invalid vehicle status. Must be one of: Available, On Trip, Maintenance."):
        super().__init__(message)

