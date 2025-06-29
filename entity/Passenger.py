'''
Similar to Booking.py, this file defines the Passenger class (Constructor), which 
represents a passenger in the transport management system.
'''

class Passenger:
    def __init__(self, passenger_id, first_name, gender, age, email, phone_number):
        self.passenger_id = passenger_id
        self.first_name = first_name
        self.gender = gender
        self.age = age
        self.email = email
        self.phone_number = phone_number