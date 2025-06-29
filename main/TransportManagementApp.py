from dao.TransportManagementServiceImpl import TransportManagementServiceImpl
from entity.Vehicle import Vehicle
from exception.CustomExceptions import (
    VehicleNotFoundException,
    BookingNotFoundException,
    TripNotFoundException,
    RouteNotFoundException,
    InvalidVehicleDataException,
    InvalidTripDataException,
    InvalidBookingDataException,
    InvalidDriverDataException
)

class TransportManagementApp:
    def __init__(self):
        self.service = TransportManagementServiceImpl()
        self.service.start_auto_status_updater()  # Starts background auto-update every 5 mins

    def main_menu(self):
        while True:
            print("\nTransport Management System")
            print("1. Add Vehicle")
            print("2. Update Vehicle")
            print("3. Delete Vehicle")
            print("4. Schedule Trip")
            print("5. Cancel Trip")
            print("6. Book Trip")
            print("7. Cancel Booking")
            print("8. Allocate Driver")
            print("9. Deallocate Driver")
            print("10. Get Bookings by Passenger")
            print("11. Get Bookings by Trip")
            print("12. Get Available Drivers")
            print("0. Exit")

            choice = input("Enter your choice: ")
            
            try:
                if choice == "1":
                    self.add_vehicle_menu()
                elif choice == "2":
                    self.update_vehicle_menu()
                elif choice == "3":
                    self.delete_vehicle_menu()
                elif choice == "4":
                    self.schedule_trip_menu()
                elif choice == "5":
                    self.cancel_trip_menu()
                elif choice == "6":
                    self.book_trip_menu()
                elif choice == "7":
                    self.cancel_booking_menu()
                elif choice == "8":
                    self.allocate_driver_menu()
                elif choice == "9":
                    self.deallocate_driver_menu()
                elif choice == "10":
                    self.get_bookings_by_passenger_menu()
                elif choice == "11":
                    self.get_bookings_by_trip_menu()
                elif choice == "12":
                    self.get_available_drivers_menu()
                elif choice == "0":
                    print("Exiting application. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except (VehicleNotFoundException, BookingNotFoundException, TripNotFoundException,
                    RouteNotFoundException) as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def add_vehicle_menu(self):
        try:
            model = input("Enter vehicle model: ").strip()
            capacity_input = input("Enter vehicle capacity: ").strip()
            type = input("Enter vehicle type (Truck/Van/Bus): ").strip()
            status = input("Enter vehicle status (Available/On Trip/Maintenance): ").strip()

            if not model or not capacity_input or not type or not status:
                raise InvalidVehicleDataException("All fields are required and cannot be empty.")

            try:
                capacity = float(capacity_input)
                if capacity <= 0:
                    raise InvalidVehicleDataException("Capacity must be greater than 0.")
            except ValueError:
                raise InvalidVehicleDataException("Capacity must be a valid number.")

            vehicle = Vehicle(None, model, capacity, type, status)
            if self.service.add_vehicle(vehicle):
                print("Vehicle added successfully!")
            else:
                print("Failed to add vehicle.")
        except InvalidVehicleDataException as e:
            print(f"Error: {e}")

    def update_vehicle_menu(self):
        try:
            vehicle_id = int(input("Enter Vehicle ID to update: "))
            vehicle = Vehicle(vehicle_id, None, None, None, None)
            if self.service.update_vehicle(vehicle):
                print("Vehicle updated successfully!")
            else:
                print("Failed to update vehicle.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def delete_vehicle_menu(self):
        try:
            vehicle_id = int(input("Enter Vehicle ID to delete: "))
            if self.service.delete_vehicle(vehicle_id):
                print("Vehicle deletion completed.")
            else:
                print("Vehicle deletion not completed.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def schedule_trip_menu(self):
        try:
            vehicle_id = input("Enter vehicle ID: ").strip()
            route_id = input("Enter route ID: ").strip()
            departure_date = input("Enter departure date (YYYY-MM-DD HH:MM:SS): ").strip()
            arrival_date = input("Enter arrival date (YYYY-MM-DD HH:MM:SS): ").strip()

            if not vehicle_id or not route_id or not departure_date or not arrival_date:
                raise InvalidTripDataException("All fields are required and cannot be empty.")

            try:
                vehicle_id = int(vehicle_id)
                route_id = int(route_id)
            except ValueError:
                raise InvalidTripDataException("Vehicle ID and Route ID must be integers.")

            if self.service.schedule_trip(vehicle_id, route_id, departure_date, arrival_date):
                print("Trip scheduled successfully!")
            else:
                print("Failed to schedule trip.")
        except InvalidTripDataException as e:
            print(f"Error: {e}")

    def cancel_trip_menu(self):
        try:
            trip_id = int(input("Enter Trip ID to cancel: "))
            if self.service.cancel_trip(trip_id):
                print("Trip cancelled successfully.")
            else:
                print("Trip cancellation failed.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def book_trip_menu(self):
        try:
            trip_id = input("Enter Trip ID to book: ").strip()
            num_people = input("Enter number of people to book: ").strip()

            if not trip_id or not num_people:
                raise InvalidBookingDataException("Trip ID and number of people are required.")

            try:
                trip_id = int(trip_id)
                num_people = int(num_people)
                if num_people <= 0:
                    raise InvalidBookingDataException("Number of people must be greater than 0.")
            except ValueError:
                raise InvalidBookingDataException("Trip ID and number of people must be integers.")

            # Continue with booking logic...
            # (You may want to validate passenger IDs similarly)
            result = self.service.book_trip()
            if result:
                print("Booking successful!")
            else:
                print("Booking failed.")
        except InvalidBookingDataException as e:
            print(f"Error: {e}")

    def cancel_booking_menu(self):
        try:
            booking_id = input("Enter Booking ID to cancel: ").strip()
            if not booking_id:
                raise InvalidBookingDataException("Booking ID is required.")
            try:
                booking_id = int(booking_id)
            except ValueError:
                raise InvalidBookingDataException("Booking ID must be an integer.")

            result = self.service.cancel_booking(booking_id)
            if result:
                print("Booking cancelled successfully!")
            else:
                print("Failed to cancel booking.")
        except InvalidBookingDataException as e:
            print(f"Error: {e}")

    def allocate_driver_menu(self):
        try:
            trip_id = input("Enter Trip ID: ").strip()
            driver_id = input("Enter Driver ID: ").strip()
            if not trip_id or not driver_id:
                raise InvalidDriverDataException("Trip ID and Driver ID are required.")
            try:
                trip_id = int(trip_id)
                driver_id = int(driver_id)
            except ValueError:
                raise InvalidDriverDataException("Trip ID and Driver ID must be integers.")

            result = self.service.allocate_driver(trip_id, driver_id)
            if result:
                print("Driver allocated successfully!")
            else:
                print("Failed to allocate driver.")
        except InvalidDriverDataException as e:
            print(f"Error: {e}")

    def deallocate_driver_menu(self):
        try:
            trip_id = input("Enter Trip ID: ").strip()
            if not trip_id:
                raise InvalidDriverDataException("Trip ID is required.")
            try:
                trip_id = int(trip_id)
            except ValueError:
                raise InvalidDriverDataException("Trip ID must be an integer.")

            result = self.service.deallocate_driver(trip_id)
            if result:
                print("Driver deallocated successfully!")
            else:
                print("Failed to deallocate driver.")
        except InvalidDriverDataException as e:
            print(f"Error: {e}")

    def get_bookings_by_passenger_menu(self):
        try:
            passenger_id = int(input("Enter Passenger ID: "))
            bookings = self.service.get_bookings_by_passenger(passenger_id)
            if bookings:
                print(f"Bookings for Passenger ID {passenger_id}:")
                for booking in bookings:
                    print(booking)
            else:
                print(f"No bookings found for Passenger ID {passenger_id}.")
        except ValueError:
            print("❌ Invalid input. Please enter a numeric value for Passenger ID.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def get_bookings_by_trip_menu(self):
        try:
            trip_id = int(input("Enter Trip ID: "))
            bookings = self.service.get_bookings_by_trip(trip_id)
            if bookings:
                print(f"Bookings for Trip ID {trip_id}:")
                for booking in bookings:
                    print(booking)
            else:
                print(f"No bookings found for Trip ID {trip_id}.")
        except ValueError:
            print("❌ Invalid input. Please enter a numeric value for Trip ID.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def get_available_drivers_menu(self):
        try:
            available_drivers = self.service.get_available_drivers()
            if available_drivers:
                print("Available Drivers:")
                for driver in available_drivers:
                    print(driver)
            else:
                print("No available drivers found.")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    

if __name__ == "__main__":
    app = TransportManagementApp()
    app.main_menu()
