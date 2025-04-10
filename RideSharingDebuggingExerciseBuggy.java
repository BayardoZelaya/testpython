import java.util.*;

public class RideSharingDebuggingExerciseBuggy {

    public static class DispatchSystem {
        private List<Driver> drivers;

        public DispatchSystem(List<Driver> drivers) {
            if (drivers == null) {
                throw new IllegalArgumentException("drivers must not be null");
            }
            this.drivers = drivers;
        }

        // Review this method to ensure that fare is calculated correctly.
        public double calculateFare(double distance, double time, double surgeMultiplier) {
            double baseFare = 2.50;
            double fare = baseFare + (distance * 1.20) + (time * 0.25);

            return fare + surgeMultiplier;
        }

        // Review this method to ensure that only eligible drivers are considered.
        public Driver assignDriver(double[] passengerLocation) {
            if (passengerLocation == null || passengerLocation.length != 2) {
                throw new IllegalArgumentException("passengerLocation must be an array of two numbers");
            }
            Driver closest = null;
            double minDistance = Double.MAX_VALUE;
            for (Driver d : drivers) {
                double dist = distance(d.getCurrentLocation(), passengerLocation);
                if (dist < minDistance) {
                    minDistance = dist;
                    closest = d;
                }
            }
            return closest;
        }

        // Review this method to verify that it selects the best driver efficiently.
        public Driver findBestDriver(double[] referenceLocation) {
            if (referenceLocation == null || referenceLocation.length != 2) {
                throw new IllegalArgumentException("referenceLocation must be an array of two numbers");
            }
            Driver bestDriver = null;
            double bestScore = -Double.MAX_VALUE;
            for (Driver d : drivers) {
                if (!d.isAvailable()) {
                    continue;
                }
                double distanceSum = 0.0;
                for (Driver ignore : drivers) {
                    distanceSum += distance(d.getCurrentLocation(), referenceLocation);
                }
                double avgDistance = distanceSum / drivers.size();
                double score = d.getRating() / (avgDistance + 1);
                if (score > bestScore) {
                    bestScore = score;
                    bestDriver = d;
                }
            }
            if (bestDriver == null) {
                throw new NoSuchElementException("No available drivers");
            }
            return bestDriver;
        }

        private double distance(double[] loc1, double[] loc2) {
            double dx = loc1[0] - loc2[0];
            double dy = loc1[1] - loc2[1];
            return Math.sqrt(dx * dx + dy * dy);
        }
    }

    public static class Driver {
        private String name;
        private double[] currentLocation;
        private double rating;
        private boolean available;

        public Driver(String name, double[] currentLocation, double rating, boolean available) {
            if (name == null || currentLocation == null || currentLocation.length != 2) {
                throw new IllegalArgumentException("Invalid arguments");
            }
            this.name = name;
            this.currentLocation = currentLocation;
            this.rating = rating;
            this.available = available;
        }

        public String getName() {
            return name;
        }

        public double[] getCurrentLocation() {
            return currentLocation;
        }

        public double getRating() {
            return rating;
        }

        public boolean isAvailable() {
            return available;
        }

        // Review this method to ensure that all necessary driver details are returned.
        public Map<String, Object> getStatus() {
            Map<String, Object> status = new HashMap<>();
            status.put("name", name);
            status.put("location", currentLocation);
            status.put("available", available);
            // Candidate should check if any key is missing.
            return status;
        }
    }

    // Simple test harness.
    public static void main(String[] args) {
        boolean allPassed = true;

        // Test calculateFare:
        double expectedFare = (2.50 + (10 * 1.20) + (15 * 0.25)) * 1.5;
        DispatchSystem ds = new DispatchSystem(Arrays.asList(
                new Driver("Alice", new double[] { 0, 0 }, 4.8, true),
                new Driver("Bob", new double[] { 3, 4 }, 4.5, false),
                new Driver("Charlie", new double[] { 1, 1 }, 4.9, true)));
        double fare = ds.calculateFare(10, 15, 1.5);
        if (Math.abs(fare - expectedFare) > 0.001) {
            System.out.println("calculateFare failed: expected " + expectedFare + ", got " + fare);
            allPassed = false;
        }

        // Test assignDriver:
        Driver assigned = ds.assignDriver(new double[] { 0.1, 0.1 });
        if (!assigned.getName().equals("Alice")) {
            System.out.println("assignDriver failed: expected Alice, got " + assigned.getName());
            allPassed = false;
        }

        // Test getStatus:
        Map<String, Object> status = ds.drivers.get(0).getStatus();
        if (!status.containsKey("rating")) {
            System.out.println("getStatus failed: rating is missing in the status.");
            allPassed = false;
        }

        // Test findBestDriver:
        Driver best = ds.findBestDriver(new double[] { 0, 0 });
        if (!best.getName().equals("Alice")) {
            System.out.println("findBestDriver failed: expected Alice, got " + best.getName());
            allPassed = false;
        }

        if (allPassed) {
            System.out.println("All tests passed (Buggy version).");
        } else {
            System.out.println("Some tests failed (Buggy version).");
        }
    }
}
