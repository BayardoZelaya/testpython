# Interviewer README: Ride-Sharing Dispatch System Debugging Exercise

## Purpose of the Exercise

This exercise is designed to assess the candidate’s ability to:
- **Debug Code:** Identify and resolve multiple issues in a moderately complex Python codebase.
- **Understand Object-Oriented Design:** Work with classes and methods in a realistic simulation.
- **Optimize Code:** Recognize inefficiencies and refactor code for better performance.
- **Maintain Test Integrity:** Fix the functionality without altering the provided unit tests.

## What the Code Is Looking For

The provided code simulates a ride-sharing dispatch system with two main classes: `DispatchSystem` and `Driver`. It intentionally contains several bugs and inefficiencies that the candidate needs to identify and fix. Specifically, the code tests the following:

1. **Fare Calculation (`calculate_fare`):**
   - **Issue:** The function is incorrectly adding the surge multiplier to the fare instead of applying it multiplicatively.
   - **Expectation:** The candidate should modify the computation so that the surge multiplier correctly scales the total fare.

2. **Driver Assignment (`assign_driver`):**
   - **Issue:** The function does not filter out drivers who are unavailable, potentially assigning a driver who cannot take a ride.
   - **Expectation:** The candidate must ensure that only drivers marked as available are considered when finding the closest driver to a given location.

3. **Driver Status Reporting (`Driver.get_status`):**
   - **Issue:** The driver's status dictionary is missing the `rating` key.
   - **Expectation:** The candidate should include the driver’s rating in the status report to provide a complete overview of the driver’s information.

4. **Best Driver Selection (`find_best_driver`):**
   - **Issue:** The function uses an unnecessary nested loop to calculate the Euclidean distance, leading to inefficient (O(n²)) performance.
   - **Expectation:** The candidate should optimize the function by computing the distance once per driver and then determining an efficiency score (defined as `score = rating / (distance + 1)`) to select the best driver.

## How the Candidate Will Work on the Exercise

- **Code Review:** The candidate is expected to review the code as a whole to understand the intended functionality.
- **Run Code:** Using the "Run Code" button on Codility, the candidate will see which unit tests fail and use that feedback to guide their debugging efforts.
- **Fix Issues:** The candidate must update the code to correct the bugs and improve performance, ensuring that all tests pass without modifying the test cases.
- **Optimization:** Where applicable, the candidate should refactor inefficient sections of the code for improved performance and clarity.

## Evaluation Criteria

The candidate’s submission will be evaluated based on:
- **Correctness:** All unit tests pass after debugging and refactoring.
- **Code Quality:** Code is readable, well-organized, and follows Python best practices.
- **Problem-Solving:** Effective identification and resolution of the bugs and inefficiencies.
- **Optimization:** Appropriate use of efficient algorithms and language features where necessary.

This exercise is intended to simulate a real-world debugging and optimization scenario, providing insight into the candidate’s technical skills and problem-solving approach.
