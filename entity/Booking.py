'''
This file defines the Booking class (Constructor), which represents a booking in the transport management system.
It includes attributes such as booking ID, trip ID, passenger ID, booking date, and status.
'''

class Booking:
    def __init__(self, booking_id, trip_id, passenger_id, booking_date, status):
        self.booking_id = booking_id
        self.trip_id = trip_id
        self.passenger_id = passenger_id
        self.booking_date = booking_date
        self.status = status

    def __str__(self):
        return (f"BookingID: {self.booking_id}, "
                f"PassengerID: {self.passenger_id}, "
                f"TripID: {self.trip_id}, "
                f"BookingDate: {self.booking_date}, "
                f"Status: {self.status}")