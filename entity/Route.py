'''
Similar to Booking.py, this file defines the Route class (Constructor), which 
represents a route in the transport management system.
'''

class Route:
    def __init__(self, route_id, start_destination, end_destination, distance):
        self.route_id = route_id
        self.start_destination = start_destination
        self.end_destination = end_destination
        self.distance = distance