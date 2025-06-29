'''
Similar to Booking.py, this file defines the Driver class (Constructor), which represents 
a driver in the transport management system. 
'''

class Driver:
    def __init__(self, driver_id=None, name=None, age=None, gender=None,
                 license_number=None, contact_number=None, address=None, status=None):
        self.driver_id = driver_id
        self.name = name
        self.age = age
        self.gender = gender
        self.license_number = license_number
        self.contact_number = contact_number
        self.address = address
        self.status = status

    def __str__(self):
        return (f"DriverID: {self.driver_id}, Name: {self.name}, Age: {self.age}, "
                f"Gender: {self.gender}, License No: {self.license_number}, "
                f"Contact: {self.contact_number}, Status: {self.status}")
