#!/usr/bin/env pybricks-micropython
import time
import math

# Import SPIKE Prime library (standard format for version 3.4.5)
import hub
import time
from spike import Motor, ColorSensor, PrimeHub

# Initialize the hub
prime_hub = PrimeHub()

# Define motor and sensor ports - adjusted based on user configuration
LEFT_MOTOR_PORT = 'E'  # Port for left motor
RIGHT_MOTOR_PORT = 'C'  # Port for right motor
COLOR_SENSOR_PORT = 'A'  # Port for color sensor

# Initialize motors and sensors
left_motor = Motor(LEFT_MOTOR_PORT)
right_motor = Motor(RIGHT_MOTOR_PORT)
line_sensor = ColorSensor(COLOR_SENSOR_PORT)

class PIDController:
    def __init__(self, Kp, Ki, Kd, target):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.target = target

        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()

    def update(self, current_value):
        """Calculates PID output based on the current sensor value."""
        current_time = time.time()
        dt = current_time - self.last_time

        # avoid division by zero and ensure dt is positive
        if dt <= 0:
            dt = 0.0000000000001  # set dt to a very small value instead of 0

        error = self.target - current_value

        # update the integral term, the accumulated error
        self.integral += error * dt

        # calculate the derivative term, the current rate of change of the error
        change_in_error = error - self.previous_error
        derivative = change_in_error / dt

        # calculate the PID output
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        # set the current time and error as the previous time and error for the next iteration
        self.previous_error = error
        self.last_time = current_time

        return output

# PID tuning values - these may need adjustment for your specific robot
Kp = 0.8     # proportional - increased for SPIKE
Ki = 0.0001  # integral - adjusted for SPIKE
Kd = 0.1     # derivative - adjusted for SPIKE

# Depending on your line color, you may need to adjust this
# For a black line on white surface, target would be low
# For a white line on black surface, target would be high
target_reflection = 50  # Middle value between black and white

# Base speed setting - adjust according to your robot's capabilities
base_speed = 20  # Increased for SPIKE motors which typically use 0-100 scale

# Create PID controller
line_pid = PIDController(Kp, Ki, Kd, target_reflection)

def follow_line():
    """
    Line follower using PID control for SPIKE Prime.
    """
    # Read reflection value from color sensor (0-100)
    reflection = line_sensor.get_reflected_light()
    
    # Print for debugging
    print(f"Reflection: {reflection}")

    # Calculate turn adjustment using PID
    turn_speed = line_pid.update(reflection)
    
    # Calculate motor speeds
    left_speed = base_speed + turn_speed
    right_speed = base_speed - turn_speed
    
    # Limit speeds to valid range for SPIKE motors (typically -100 to 100)
    left_speed = max(-100, min(100, left_speed))
    right_speed = max(-100, min(100, right_speed))
    
    # Print motor speeds for debugging
    print(f"Left: {left_speed}, Right: {right_speed}")

    # Run the motors
    left_motor.start(int(left_speed))
    right_motor.start(int(right_speed))

def main():
    """Main function that runs the program."""
    # Display a message on the hub's display
    prime_hub.light_matrix.write("Line")
    
    # Short delay to show the message
    time.sleep(1)
    
    # Main control loop
    while True:
        follow_line()
        time.sleep(0.01)  # Small delay between iterations

# Run the main function
if __name__ == "__main__":
    main() 