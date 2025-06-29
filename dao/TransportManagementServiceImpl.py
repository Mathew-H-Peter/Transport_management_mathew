from typing import List
from .ITransportManagementService import ITransportManagementService
from entity.Vehicle import Vehicle
from entity.Booking import Booking
from entity.Driver import Driver
from exception.CustomExceptions import VehicleNotFoundException, InvalidVehicleStatusException, BookingNotFoundException,TripNotFoundException, BookingNotFoundException, InvalidVehicleDataException
from util.DBConnUtil import DBConnUtil
import mysql.connector
from datetime import datetime, timedelta
import threading

class TransportManagementServiceImpl(ITransportManagementService):
    def __init__(self):
        self.conn = DBConnUtil.get_connection("connection_string")
        self.cursor = self.conn.cursor()

    def add_vehicle(self, vehicle: Vehicle) -> bool:
        try:
            # Validate required fields
            if not vehicle.model or not str(vehicle.model).strip():
                raise InvalidVehicleDataException("Model is required and cannot be empty.")
            if vehicle.capacity is None or str(vehicle.capacity).strip() == "" or float(vehicle.capacity) <= 0:
                raise InvalidVehicleDataException("Capacity is required and must be greater than 0.")
            if not vehicle.type or not str(vehicle.type).strip():
                raise InvalidVehicleDataException("Type is required and cannot be empty.")
            allowed_statuses = ["Available", "On Trip", "Maintenance"]
            while vehicle.status not in allowed_statuses:
                print(f"Invalid status: '{vehicle.status}'")
                print("Allowed values: Available, On Trip, Maintenance")
                vehicle.status = input("Please re-enter valid status: ").strip()
                if vehicle.status not in allowed_statuses:
                    raise InvalidVehicleStatusException()

            query = "INSERT INTO Vehicles (Model, Capacity, Type, Status) VALUES (%s, %s, %s, %s)"
            values = (vehicle.model, vehicle.capacity, vehicle.type, vehicle.status)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except (InvalidVehicleDataException, InvalidVehicleStatusException) as e:
            print(f"Error adding vehicle: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def update_vehicle(self, vehicle: Vehicle) -> bool:
        try:
            # Step 1: Check if vehicle exists
            select_query = "SELECT * FROM Vehicles WHERE VehicleID = %s"
            self.cursor.execute(select_query, (vehicle.vehicle_id,))
            result = self.cursor.fetchone()

            if not result:
                raise VehicleNotFoundException()

            print("\nCurrent Vehicle Details:")
            print(f"Vehicle ID: {result[0]}")
            print(f"Model: {result[1]}")
            print(f"Capacity: {result[2]}")
            print(f"Type: {result[3]}")
            print(f"Status: {result[4]} (Note: Status cannot be updated here)")

            # Step 2: Ask which fields to update
            updates = {}
            print("\nLeave input blank if you don't want to update that field.")

            new_model = input("Enter new Model: ")
            if new_model.strip():
                updates['Model'] = new_model.strip()

            new_capacity = input("Enter new Capacity: ")
            if new_capacity.strip():
                try:
                    updates['Capacity'] = float(new_capacity)
                except ValueError:
                    print("Invalid capacity entered. Skipping.")

            new_type = input("Enter new Type (Truck/Van/Bus): ")
            if new_type.strip():
                updates['Type'] = new_type.strip()

            # Step 3: If no updates, skip
            if not updates:
                print("No updates provided.")
                return False

            # Step 4: Construct dynamic update query
            set_clause = ", ".join(f"{column} = %s" for column in updates.keys())
            values = list(updates.values()) + [vehicle.vehicle_id]

            update_query = f"UPDATE Vehicles SET {set_clause} WHERE VehicleID = %s"
            self.cursor.execute(update_query, values)
            self.conn.commit()

            print("Vehicle updated successfully with selected fields.")
            return True

        except VehicleNotFoundException:
            raise VehicleNotFoundException("Vehicle not found in the database.")
        except InvalidVehicleDataException as e:
            print(f"Error updating vehicle: {e}")
            return False
        except InvalidVehicleStatusException as e:
            print(f"Error updating vehicle status: {e}")
            return False
        except Exception as e:
            print(f"Error updating vehicle: {e}")
            return False


    def delete_vehicle(self, vehicle_id: int) -> bool:
        try:
            # Check if vehicle exists
            select_query = "SELECT * FROM Vehicles WHERE VehicleID = %s"
            self.cursor.execute(select_query, (vehicle_id,))
            result = self.cursor.fetchone()

            if not result:
                raise VehicleNotFoundException(f"Vehicle with ID {vehicle_id} not found.")

            print("\nVehicle found:")
            print(f"Vehicle ID: {result[0]}")
            print(f"Model: {result[1]}")
            print(f"Capacity: {result[2]}")
            print(f"Type: {result[3]}")
            print(f"Status: {result[4]}")

            confirm = input("\nAre you sure you want to delete this vehicle and deallocate all related trips and bookings? (Y/N): ")
            if confirm.strip().upper() != "Y":
                print("Delete operation terminated.")
                return False

            # 1. Set VehicleID to NULL in Trips (deallocate vehicle from trips)
            self.cursor.execute("""
                UPDATE Trips SET VehicleID = NULL WHERE VehicleID = %s
            """, (vehicle_id,))

            # 4. Delete the vehicle
            delete_query = "DELETE FROM Vehicles WHERE VehicleID = %s"
            self.cursor.execute(delete_query, (vehicle_id,))
            self.conn.commit()
            print(f"Vehicle with ID {vehicle_id} and all related trips/bookings have been deallocated and deleted.")
            return True

        except VehicleNotFoundException as ve:
            print(f"Error: {ve}")
            raise
        except Exception as e:
            print(f"An error occurred during deletion: {e}")
            return False


    def schedule_trip(self, vehicle_id: int, route_id: int, departure_date: str, arrival_date: str) -> bool:
        try:
            new_dep = datetime.strptime(departure_date, "%Y-%m-%d %H:%M:%S")
            new_arr = datetime.strptime(arrival_date, "%Y-%m-%d %H:%M:%S")

            if new_arr <= new_dep:
                print("Arrival must be after departure.")
                return False

            # Check if vehicle exists
            self.cursor.execute("SELECT Capacity FROM Vehicles WHERE VehicleID = %s", (vehicle_id,))
            result = self.cursor.fetchone()
            if not result:
                raise VehicleNotFoundException(f"Vehicle with ID {vehicle_id} not found.")
            capacity = result[0]

            # Fetch scheduled trips for this vehicle
            self.cursor.execute("""
                SELECT DepartureDate, ArrivalDate
                FROM Trips
                WHERE VehicleID = %s AND Status = 'Scheduled'
            """, (vehicle_id,))
            existing_trips = self.cursor.fetchall()

            for existing_dep, existing_arr in existing_trips:
                rest_buffer = existing_arr + timedelta(days=3)
                if (new_dep <= rest_buffer and new_arr >= existing_dep):
                    print(f"Vehicle is not available between {existing_dep} and {rest_buffer} due to another scheduled trip.")
                    return False

            # Insert new trip
            self.cursor.execute("""
                INSERT INTO Trips (VehicleID, RouteID, DepartureDate, ArrivalDate, Status, TripType, MaxPassengers)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (vehicle_id, route_id, departure_date, arrival_date, "Scheduled", "Freight", capacity))

            self.conn.commit()
            print(f"Trip scheduled successfully for Vehicle ID {vehicle_id}.")
            return True

        except VehicleNotFoundException as ve:
            print(f"Error: {ve}")
            return False
        except Exception as e:
            print(f"Error scheduling trip: {e}")
            return False

    def cancel_trip(self, trip_id: int) -> bool:
        try:
            # 1. Check if trip exists and fetch vehicle_id
            self.cursor.execute("SELECT VehicleID FROM Trips WHERE TripID = %s", (trip_id,))
            trip = self.cursor.fetchone()

            if not trip:
                raise Exception(f"No trip found with ID {trip_id}.")

            vehicle_id = trip[0]  # Extract VehicleID from result

            # 2. Update trip status to CANCELLED
            update_query = "UPDATE Trips SET Status = %s WHERE TripID = %s"
            self.cursor.execute(update_query, ("CANCELLED", trip_id))

            # 3. Update vehicle status to Available
            vehicle_update_query = "UPDATE Vehicles SET Status = %s WHERE VehicleID = %s"
            self.cursor.execute(vehicle_update_query, ("Available", vehicle_id))

            self.conn.commit()

            print(f"Trip ID {trip_id} has been successfully cancelled.")
            print(f"Vehicle ID {vehicle_id} status set to 'Available'.")
            return True

        except Exception as e:
            print(f"Error cancelling trip: {e}")
            return False


    def book_trip(self) -> bool:
        try:
            # Step 1: Ask for trip ID
            trip_id = int(input("Enter Trip ID to book: "))

            # Step 2: Fetch trip details
            self.cursor.execute("""
                SELECT T.TripID, T.Status, T.DepartureDate, V.Capacity,
                    (SELECT COUNT(*) FROM Bookings WHERE TripID = T.TripID AND Status = 'BOOKED') AS BookedSeats
                FROM Trips T
                JOIN Vehicles V ON T.VehicleID = V.VehicleID
                WHERE T.TripID = %s
            """, (trip_id,))
            trip_data = self.cursor.fetchone()

            if not trip_data:
                raise TripNotFoundException(f"Trip ID {trip_id} not found.")

            trip_id, status, departure_date, capacity, booked_seats = trip_data
            booking_date = datetime.now()

            # Step 3: Validate trip status
            if status.upper() == "CANCELLED":
                print("Sorry, the trip was cancelled due to certain circumstances.")
                return False

            # Step 4: Validate booking cutoff
            if booking_date > departure_date - timedelta(days=1):
                print("Sorry, bookings are closed.")
                return False

            # Step 5: Ask for number of people
            num_people = int(input("Enter number of people to book: "))

            # Check availability
            available_seats = capacity - booked_seats
            if num_people > available_seats:
                print(f"Only {available_seats} seats are available. Cannot book {num_people} seats.")
                return False

            passenger_ids = []
            for i in range(num_people):
                pid = int(input(f"Enter Passenger ID for person {i+1}: "))

                # Validate passenger ID
                self.cursor.execute("SELECT * FROM Passengers WHERE PassengerID = %s", (pid,))
                if not self.cursor.fetchone():
                    print(f"Passenger ID {pid} not found. Skipping this ID.")
                    continue

                # Check for duplicate active booking
                self.cursor.execute("""
                    SELECT PassengerID, TripID, BookingDate 
                    FROM Bookings 
                    WHERE PassengerID = %s AND TripID = %s AND Status = 'BOOKED'
                """, (pid, trip_id))
                existing = self.cursor.fetchone()

                if existing:
                    print(f"Passenger ID {pid} is already booked on Trip {trip_id}.")
                    print(f"Existing Booking - PassengerID: {existing[0]}, TripID: {existing[1]}, BookingDate: {existing[2]}")
                    continue

                passenger_ids.append(pid)

            # Final confirmation
            if not passenger_ids:
                print("No valid passengers to book.")
                return False

            # Step 6: Insert all bookings
            for pid in passenger_ids:
                self.cursor.execute("""
                    INSERT INTO Bookings (PassengerID, TripID, BookingDate, Status)
                    VALUES (%s, %s, %s, %s)
                """, (pid, trip_id, booking_date, "BOOKED"))

            self.conn.commit()
            print(f"[Booking] Successfully booked {len(passenger_ids)} passenger(s) on Trip {trip_id}.")
            return True

        except (TripNotFoundException, BookingNotFoundException) as e:
            print(f"[Booking Error] {e}")
            raise
        except Exception as e:
            print(f"[Booking Error] Unexpected error: {e}")
            return False

    def cancel_booking(self, booking_id: int) -> bool:
        try:
            # 1. Check if booking exists
            self.cursor.execute("SELECT * FROM Bookings WHERE BookingID = %s", (booking_id,))
            existing_booking = self.cursor.fetchone()

            if not existing_booking:
                raise BookingNotFoundException(f"Booking with ID {booking_id} not found.")

            # 2. Update the booking status to CANCELLED
            self.cursor.execute("UPDATE Bookings SET Status = %s WHERE BookingID = %s", ("CANCELLED", booking_id))
            self.conn.commit()

            print(f"[Cancellation] Booking ID {booking_id} has been successfully cancelled.")
            return True
        except BookingNotFoundException as e:
            print(f"[Cancellation Error] {e}")
            raise
        except Exception as e:
            print(f"[Cancellation Error] Unexpected error: {e}")
            return False

    def allocate_driver(self, trip_id: int, driver_id: int) -> bool:
        try:
            # Step 1: Fetch trip details
            self.cursor.execute("""
                SELECT DepartureDate, ArrivalDate, Status, DriverID
                FROM Trips
                WHERE TripID = %s
            """, (trip_id,))
            trip = self.cursor.fetchone()

            if not trip:
                print(f"No trip found with ID {trip_id}")
                return False

            new_dep, new_arr, status, existing_driver_id = trip

            if status.upper() == "CANCELLED":
                print("Cannot allocate a driver to a CANCELLED trip.")
                return False

            if existing_driver_id:
                print(f"ℹTrip ID {trip_id} already has Driver ID {existing_driver_id} assigned.")
                choice = input("Do you want to replace the existing driver? (Y/N): ").strip().upper()
                if choice != 'Y':
                    print(" Driver allocation skipped. Existing driver retained.")
                    return False

            # Step 2: Check if driver exists
            self.cursor.execute("SELECT * FROM Drivers WHERE DriverID = %s", (driver_id,))
            driver = self.cursor.fetchone()
            if not driver:
                print(f"No driver found with ID {driver_id}")
                return False

            # Step 3: Check for conflicting scheduled trips
            self.cursor.execute("""
                SELECT DepartureDate, ArrivalDate
                FROM Trips
                WHERE DriverID = %s AND Status = 'Scheduled'
            """, (driver_id,))
            trips = self.cursor.fetchall()

            for dep, arr in trips:
                rest_buffer = arr + timedelta(days=3)
                if new_dep <= rest_buffer and new_arr >= dep:
                    print(" Driver is not available for the selected trip due to overlap or rest buffer.")
                    return False

            # Step 4: Allocate driver
            self.cursor.execute("UPDATE Trips SET DriverID = %s WHERE TripID = %s", (driver_id, trip_id))
            self.conn.commit()
            print(f" Driver ID {driver_id} successfully allocated to Trip ID {trip_id}")
            return True

        except Exception as e:
            print(f"[Allocation Error] {e}")
            return False

    def deallocate_driver(self, trip_id: int) -> bool:
        try:
            # Step 1: Fetch current driver assigned to the trip
            self.cursor.execute("""
                SELECT DriverID, Status
                FROM Trips
                WHERE TripID = %s
            """, (trip_id,))
            trip = self.cursor.fetchone()

            if not trip:
                print(f" No trip found with ID {trip_id}")
                return False

            current_driver_id, status = trip

            # Step 2: If trip is CANCELLED, skip deallocation
            if status.upper() == "CANCELLED":
                print(" Cannot deallocate driver from a CANCELLED trip.")
                return False

            # Step 3: If no driver is assigned
            if not current_driver_id:
                print(f"No driver is currently assigned to Trip ID {trip_id}")
                return False

            # Step 4: Ask for confirmation
            confirm = input(f"Driver ID {current_driver_id} is currently assigned to Trip ID {trip_id}. Do you want to deallocate? (Y/N): ").strip().upper()
            if confirm != 'Y':
                print(" Driver deallocation cancelled.")
                return False

            # Step 5: Set DriverID to NULL
            self.cursor.execute("UPDATE Trips SET DriverID = NULL WHERE TripID = %s", (trip_id,))
            self.conn.commit()
            print(f"Driver ID {current_driver_id} successfully deallocated from Trip ID {trip_id}")
            return True

        except Exception as e:
            print(f"[Deallocation Error] {e}")
            return False


    def get_bookings_by_passenger(self, passenger_id: int) -> List[Booking]:
        try:
            self.cursor.execute("""
                SELECT BookingID, PassengerID, TripID, BookingDate, Status
                FROM Bookings
                WHERE PassengerID = %s
            """, (passenger_id,))
            rows = self.cursor.fetchall()

            bookings = [Booking(*row) for row in rows]
            return bookings

        except Exception as e:
            print(f"[Error] Failed to fetch bookings for Passenger ID {passenger_id}: {e}")
            return []



    def get_bookings_by_trip(self, trip_id: int) -> List[Booking]:
        try:
            self.cursor.execute("""
                SELECT BookingID, PassengerID, TripID, BookingDate, Status
                FROM Bookings
                WHERE TripID = %s
            """, (trip_id,))
            rows = self.cursor.fetchall()

            bookings = [Booking(*row) for row in rows]
            return bookings

        except Exception as e:
            print(f"[Error] Failed to fetch bookings for Trip ID {trip_id}: {e}")
            return []



    def get_available_drivers(self) -> List[Driver]:
        try:
            self.cursor.execute("""
                SELECT DriverID, Name, Age, Gender, LicenseNumber, ContactNumber, Address, Status
                FROM Drivers
                WHERE Status = 'Available'
            """)
            rows = self.cursor.fetchall()

            drivers = [Driver(*row) for row in rows]
            return drivers

        except Exception as e:
            print(f"[Error] Failed to fetch available drivers: {e}")
            return []


    def auto_update_vehicle_statuses(self) -> None:
        try:
            if not self.conn.is_connected():
                self.conn = DBConnUtil.get_connection("connection_string")
                self.cursor = self.conn.cursor()

            current_date = datetime.now()

            # Step 1: Fetch all vehicles
            self.cursor.execute("SELECT VehicleID FROM Vehicles")
            vehicles = self.cursor.fetchall()

            for (vehicle_id,) in vehicles:
                new_status = "Available"

                # Step 2: Get all non-cancelled scheduled trips for this vehicle
                self.cursor.execute("""
                    SELECT DepartureDate, ArrivalDate 
                    FROM Trips 
                    WHERE VehicleID = %s AND Status = 'Scheduled'
                """, (vehicle_id,))
                trips = self.cursor.fetchall()

                for dep_date, arr_date in trips:
                    buffer_end = arr_date + timedelta(days=3)

                    if dep_date <= current_date <= arr_date:
                        new_status = "On Trip"
                        break  # Highest priority
                    elif arr_date < current_date <= buffer_end:
                        new_status = "Maintenance"
                        # Continue checking in case an active trip exists

                # Step 3: Update vehicle status
                self.cursor.execute(
                    "UPDATE Vehicles SET Status = %s WHERE VehicleID = %s",
                    (new_status, vehicle_id)
                )

            self.conn.commit()
            print("[Auto-Update] Vehicle statuses updated successfully.")

        except Exception as e:
            print(f"[Auto-Update] Error auto-updating vehicle statuses: {e}")

    def auto_update_driver_statuses(self) -> None:
        try:
            if not self.conn.is_connected():
                self.conn = DBConnUtil.get_connection("connection_string")
                self.cursor = self.conn.cursor()

            current_time = datetime.now()

            # Fetch all drivers
            self.cursor.execute("SELECT DriverID FROM Drivers")
            drivers = self.cursor.fetchall()

            for (driver_id,) in drivers:
                new_status = "Available"

                # Get all non-cancelled scheduled trips for this driver
                self.cursor.execute("""
                    SELECT DepartureDate, ArrivalDate
                    FROM Trips
                    WHERE DriverID = %s AND Status = 'Scheduled'
                """, (driver_id,))
                trips = self.cursor.fetchall()

                for dep_date, arr_date in trips:
                    rest_buffer = arr_date + timedelta(days=3)

                    if dep_date <= current_time <= arr_date:
                        new_status = "On Trip"
                        break  # Priority
                    elif arr_date < current_time <= rest_buffer:
                        new_status = "Resting"
                        # Continue checking if a new trip overrides this status

                # Update driver status
                self.cursor.execute(
                    "UPDATE Drivers SET Status = %s WHERE DriverID = %s",
                    (new_status, driver_id)
                )

            self.conn.commit()
            print("[Driver Auto-Update] Driver statuses updated successfully.")
        except Exception as e:
            print(f"[Driver Auto-Update] Error: {e}")


    def start_auto_status_updater(self):
        """Start background thread to update vehicle status every 5 minutes."""
        def update_and_reschedule():
            self.auto_update_vehicle_statuses()
            self.auto_update_driver_statuses()
            threading.Timer(300, update_and_reschedule).start()  # 300 seconds = 5 minutes

        update_and_reschedule()  # initial call