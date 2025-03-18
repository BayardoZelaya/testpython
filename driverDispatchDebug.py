#!/usr/bin/env python3
"""
Debugging Exercise: Ride-Sharing Dispatch System

Story:
You are part of a ride-sharing company operating in a busy city.
Your system comprises a DispatchSystem that manages a fleet of drivers and a Driver class
that represents each driver’s status.

The tasks include:
  - Calculating the ride fare using distance, ride time, and surge pricing.
  - Assigning the closest driver to a passenger.
  - Reporting accurate driver statuses.
  - Determining the "best" available driver based on an efficiency score.
  
Each function contains an intentional bug or inefficiency:
  1. In calculate_fare, the surge multiplier is added instead of being multiplied.
  2. In assign_driver, drivers that are not available are not filtered out.
  3. In Driver.get_status, the driver's rating is missing.
  4. In find_best_driver, an unnecessary nested loop is used to calculate the distance,
     resulting in O(n²) performance.
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
        Where:
          base_fare = 2.50, per_mile_rate = 1.20, per_minute_rate = 0.25

        TASK: Find why the test is failing and fix the bug.
        """
        if not (isinstance(distance, (int, float)) and isinstance(time, (int, float)) and isinstance(surge_multiplier, (int, float))):
            raise TypeError("distance, time, and surge_multiplier must be numbers")
        base_fare = 2.50
        fare = base_fare + (distance * 1.20) + (time * 0.25)
        return fare + surge_multiplier

    def assign_driver(self, passenger_location):
        """
        Assigns the closest driver to the passenger using Euclidean distance.

        TASK: Make the function return the closest driver, only if they are available.
        """
        if not (isinstance(passenger_location, tuple) and len(passenger_location) == 2):
            raise TypeError("passenger_location must be a tuple of two numbers")
        
        def distance(driver):
            return ((driver.current_location[0] - passenger_location[0]) ** 2 +
                    (driver.current_location[1] - passenger_location[1]) ** 2) ** 0.5
        
        # BUG: Does not filter based on driver availability.
        return min(self.drivers, key=distance)

    def find_best_driver(self, reference_location):
        """
        Determines the best available driver based on an efficiency score:
            score = rating / (distance + 1)
        where distance is the Euclidean distance from the reference_location.
-       The driver with the highest score is considered the best.

        TASK: What is the complexity of this function? Can you make it more efficient?
        """
        if not (isinstance(reference_location, tuple) and len(reference_location) == 2):
            raise TypeError("reference_location must be a tuple of two numbers")
        best_driver = None
        best_score = float('-inf')
        for driver in self.drivers:
            if not driver.available:
                continue
            # Inefficient nested loop to compute the distance.
            distance_sum = 0
            for _ in self.drivers:
                distance_sum += ((driver.current_location[0] - reference_location[0]) ** 2 +
                                 (driver.current_location[1] - reference_location[1]) ** 2) ** 0.5
            # Average distance (this redundant computation is the bug)
            avg_distance = distance_sum / len(self.drivers)
            score = driver.rating / (avg_distance + 1)
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
        TASK: Find why the test is failing and fix the bug.
        """
        return {
            "name": self.name,
            "location": self.current_location,
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
        # Passenger at location (0.1, 0.1) should be assigned to the closest driver,
        # even if that driver is unavailable (bug in filtering).
        assigned_driver = self.system.assign_driver((0.1, 0.1))
        self.assertEqual(assigned_driver.name, "Alice", "Assigned driver is not the closest available.")
