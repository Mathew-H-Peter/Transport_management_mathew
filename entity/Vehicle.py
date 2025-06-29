'''
Similar to Booking.py, this file defines the Vehicle class (Constructor), which 
represents a vehicle in the transport management system. It includes attributes such 
as vehicle ID, model, capacity, type, and status. It also includes getter and setter 
methods for each attribute.
'''

class Vehicle:
    def __init__(self, vehicle_id=None, model=None, capacity=None, type=None, status=None):
        self.__vehicle_id = vehicle_id
        self.__model = model
        self.__capacity = capacity
        self.__type = type
        self.__status = status

    # Getters
    @property
    def vehicle_id(self):
        return self.__vehicle_id

    @property
    def model(self):
        return self.__model

    @property
    def capacity(self):
        return self.__capacity

    @property
    def type(self):
        return self.__type

    @property
    def status(self):
        return self.__status

    # Setters
    @vehicle_id.setter
    def vehicle_id(self, value):
        self.__vehicle_id = value

    @model.setter
    def model(self, value):
        self.__model = value

    @capacity.setter
    def capacity(self, value):
        self.__capacity = value

    @type.setter
    def type(self, value):
        self.__type = value

    @status.setter
    def status(self, value):
        self.__status = value

        