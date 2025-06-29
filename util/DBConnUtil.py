import mysql.connector
from .DBPropertyUtil import DBPropertyUtil

class DBConnUtil:
    @staticmethod
    def get_connection(connection_string):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="transport_management"
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    @staticmethod
    def create_tables():
        table_queries = [
            """
            CREATE TABLE IF NOT EXISTS vehicles (
                VehicleID int NOT NULL AUTO_INCREMENT,
                Model varchar(255) DEFAULT NULL,
                Capacity decimal(10,2) DEFAULT NULL,
                Type varchar(50) DEFAULT NULL,
                Status varchar(50) DEFAULT NULL,
                PRIMARY KEY (VehicleID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS drivers (
                DriverID int NOT NULL AUTO_INCREMENT,
                Name varchar(100) DEFAULT NULL,
                Age int DEFAULT NULL,
                Gender varchar(10) DEFAULT NULL,
                LicenseNumber varchar(50) DEFAULT NULL,
                ContactNumber varchar(20) DEFAULT NULL,
                Address text,
                Status varchar(20) DEFAULT 'Available',
                PRIMARY KEY (DriverID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS routes (
                RouteID int NOT NULL AUTO_INCREMENT,
                StartDestination varchar(255) DEFAULT NULL,
                EndDestination varchar(255) DEFAULT NULL,
                Distance decimal(10,2) DEFAULT NULL,
                PRIMARY KEY (RouteID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS passengers (
                PassengerID int NOT NULL AUTO_INCREMENT,
                FirstName varchar(255) DEFAULT NULL,
                Gender varchar(255) DEFAULT NULL,
                Age int DEFAULT NULL,
                Email varchar(255) DEFAULT NULL,
                PhoneNumber varchar(50) DEFAULT NULL,
                PRIMARY KEY (PassengerID),
                UNIQUE KEY Email (Email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS trips (
                TripID int NOT NULL AUTO_INCREMENT,
                VehicleID int DEFAULT NULL,
                RouteID int DEFAULT NULL,
                DepartureDate datetime DEFAULT NULL,
                ArrivalDate datetime DEFAULT NULL,
                Status varchar(50) DEFAULT NULL,
                TripType varchar(50) DEFAULT 'Freight',
                MaxPassengers int DEFAULT NULL,
                DriverID int DEFAULT NULL,
                PRIMARY KEY (TripID),
                KEY VehicleID (VehicleID),
                KEY RouteID (RouteID),
                KEY FK_Trips_Driver (DriverID),
                CONSTRAINT FK_Trips_Driver FOREIGN KEY (DriverID) REFERENCES drivers (DriverID) ON DELETE SET NULL,
                CONSTRAINT trips_ibfk_1 FOREIGN KEY (VehicleID) REFERENCES vehicles (VehicleID),
                CONSTRAINT trips_ibfk_2 FOREIGN KEY (RouteID) REFERENCES routes (RouteID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """,
            """
            CREATE TABLE IF NOT EXISTS bookings (
                BookingID int NOT NULL AUTO_INCREMENT,
                TripID int DEFAULT NULL,
                PassengerID int DEFAULT NULL,
                BookingDate datetime DEFAULT NULL,
                Status varchar(50) DEFAULT NULL,
                PRIMARY KEY (BookingID),
                KEY TripID (TripID),
                KEY PassengerID (PassengerID),
                CONSTRAINT bookings_ibfk_1 FOREIGN KEY (TripID) REFERENCES trips (TripID),
                CONSTRAINT bookings_ibfk_2 FOREIGN KEY (PassengerID) REFERENCES passengers (PassengerID)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """
        ]
        conn = DBConnUtil.get_connection(None)
        if conn:
            cursor = conn.cursor()
            for query in table_queries:
                cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()