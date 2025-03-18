#!/usr/bin/env python3
"""
Debugging Exercise: Ride-Sharing Dispatch System - Fixed Version

Story:
You are part of a ride-sharing company operating in a busy city.
Your system comprises a DispatchSystem that manages a fleet of drivers and a Driver class
that represents each driver’s status.

The fixes include:
  1. calculate_fare: Surge multiplier is now correctly applied multiplicatively.
  2. assign_driver: Only available drivers are considered when assigning a driver.
  3. get_status: The driver's rating is now included in the returned dictionary.
  4. find_best_driver: The inefficient nested loop is replaced with a single loop that calculates distance once per driver.
"""

class DispatchSystem:
    def __init__(self, drivers):
        # drivers should be a list of Driver instances.
        if not isinstance(drivers, list):
            raise TypeError("drivers must be a list")
        self.drivers = drivers

    def calculate_fare(self, distance, time, surge_multiplier):
        """
        Calculate the ride fare using the formula:
          fare = (base_fare + (distance * per_mile_rate) + (time * per_minute_rate)) * surge_multiplier
        Fixed: Surge multiplier is applied multiplicatively.
        """
        if not (isinstance(distance, (int, float)) and isinstance(time, (int, float)) and isinstance(surge_multiplier, (int, float))):
            raise TypeError("distance, time, and surge_multiplier must be numbers")
        base_fare = 2.50
        fare = base_fare + (distance * 1.20) + (time * 0.25)
        return fare * surge_multiplier

    def assign_driver(self, passenger_location):
        """
        Assigns the closest available driver to the passenger using Euclidean distance.
        Fixed: Filters out drivers who are not available.
        """
        if not (isinstance(passenger_location, tuple) and len(passenger_location) == 2):
            raise TypeError("passenger_location must be a tuple of two numbers")
        
        available_drivers = [driver for driver in self.drivers if driver.available]
        if not available_drivers:
            raise ValueError("No available drivers")
        
        def distance(driver):
            return ((driver.current_location[0] - passenger_location[0]) ** 2 +
                    (driver.current_location[1] - passenger_location[1]) ** 2) ** 0.5
        
        return min(available_drivers, key=distance)

    def find_best_driver(self, reference_location):
        """
        Determines the best available driver based on an efficiency score:
            score = rating / (distance + 1)
        Fixed: Optimized implementation that calculates the distance only once per driver.
        """
        if not (isinstance(reference_location, tuple) and len(reference_location) == 2):
            raise TypeError("reference_location must be a tuple of two numbers")
        best_driver = None
        best_score = float('-inf')
        for driver in self.drivers:
            if not driver.available:
                continue
            # Compute Euclidean distance once per driver.
            distance = ((driver.current_location[0] - reference_location[0]) ** 2 +
                        (driver.current_location[1] - reference_location[1]) ** 2) ** 0.5
            score = driver.rating / (distance + 1)
            if score > best_score:
                best_score = score
                best_driver = driver
        if best_driver is None:
            raise ValueError("No available drivers")
        return best_driver


class Driver:
    def __init__(self, name, current_location, rating, available=True):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not (isinstance(current_location, tuple) and len(current_location) == 2):
            raise TypeError("current_location must be a tuple of two numbers")
        if not isinstance(rating, (int, float)):
            raise TypeError("rating must be a number")
        if not isinstance(available, bool):
            raise TypeError("available must be a boolean")
        self.name = name
        self.current_location = current_location
        self.rating = rating
        self.available = available

    def get_status(self):
        """
        Returns a dictionary with the driver's current status.
        Fixed: Includes the 'rating' key.
        """
        return {
            "name": self.name,
            "location": self.current_location,
            "rating": self.rating,
            "available": self.available
        }


# ===========================
# Unit tests for the exercise
# ===========================
import unittest

class TestDispatchSystem(unittest.TestCase):
    def setUp(self):
        self.driver1 = Driver("Alice", (0, 0), 4.8, available=True)
        self.driver2 = Driver("Bob", (3, 4), 4.5, available=False)
        self.driver3 = Driver("Charlie", (1, 1), 4.9, available=True)
        self.system = DispatchSystem([self.driver1, self.driver2, self.driver3])

    def test_calculate_fare_valid(self):
        # For a ride of 10 miles and 15 minutes, with a surge_multiplier of 1.5:
        # Expected fare = (2.50 + (10*1.20) + (15*0.25)) * 1.5
        expected = (2.50 + (10 * 1.20) + (15 * 0.25)) * 1.5
        result = self.system.calculate_fare(10, 15, 1.5)
        self.assertAlmostEqual(result, expected, places=2, msg="Fare calculation is incorrect.")

    def test_calculate_fare_type_error(self):
        with self.assertRaises(TypeError):
            self.system.calculate_fare("10", 15, 1.5)

    def test_assign_driver_valid(self):
        # Passenger at location (0.1, 0.1) should be assigned to Alice as she is the closest available.
        assigned_driver = self.system.assign_driver((0.1, 0.1))
        self.assertEqual(assigned_driver.name, "Alice", "Assigned driver is not the closest available.")

    def test_assign_driver_type_error(self):
        with self.assertRaises(TypeError):
            self.system.assign_driver("0.1, 0.1")

    def test_driver_get_status(self):
        status = self.driver1.get_status()
        self.assertIn("name", status, "Status missing name key.")
        self.assertIn("location", status, "Status missing location key.")
        self.assertIn("rating", status, "Status missing rating key.")
        self.assertIn("available", status, "Status missing available key.")
        self.assertEqual(status["rating"], 4.8, "Driver rating is incorrect.")

    def test_find_best_driver_valid(self):
        # For reference location (0,0), available drivers are Alice and Charlie.
        # Alice is at (0,0): distance = 0 so score = 4.8 / (0+1) = 4.8.
        # Charlie is at (1,1): distance ≈ 1.414 so score = 4.9 / (1.414+1) ≈ 2.03.
        # Therefore, the best driver should be Alice.
        best_driver = self.system.find_best_driver((0, 0))
        self.assertEqual(best_driver.name, "Alice", "Best driver calculation is incorrect.")

    def test_find_best_driver_no_available(self):
        # Make all drivers unavailable and ensure ValueError is raised.
        for driver in self.system.drivers:
            driver.available = False
        with self.assertRaises(ValueError):
            self.system.find_best_driver((0, 0))

    def test_find_best_driver_type_error(self):
        with self.assertRaises(TypeError):
            self.system.find_best_driver("0, 0")


if __name__ == "__main__":
    unittest.main()
