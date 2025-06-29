'''
Similar to Booking.py, this file defines the Trip class (Constructor), which represents 
a trip in the transport management system.
'''

class Trip:
    def __init__(self, trip_id, vehicle_id, route_id, departure_date, arrival_date, 
                 status, trip_type, max_passengers):
        self.trip_id = trip_id
        self.vehicle_id = vehicle_id
        self.route_id = route_id
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.status = status
        self.trip_type = trip_type
        self.max_passengers = max_passengers