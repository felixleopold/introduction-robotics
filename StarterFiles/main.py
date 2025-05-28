from hub import light_matrix
from hub import port
import time
import motor
import color_sensor

# Define motor and sensor ports
LEFT_MOTOR_PORT = port.E  # Port for left motor
RIGHT_MOTOR_PORT = port.C  # Port for right motor
COLOR_SENSOR_PORT = port.A  # Port for color sensor

# Initialize sensor
line_sensor = color_sensor.reflection(COLOR_SENSOR_PORT)

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

        # For white line on black background, we invert the error calculation
        # because higher values mean we're on the line
        error = current_value - self.target  # Inverted from (target - current_value)

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
Kp = 0.8     # proportional
Ki = 0.0001  # integral
Kd = 0.1     # derivative

# Target reflection value - for white line on black surface, target is higher
# Typical white line might be around 70-90% reflection, black might be 5-15%
target_reflection = 75  # Adjust based on your actual sensor readings of the white line

# Base speed setting
base_speed = 20

# Create PID controller
line_pid = PIDController(Kp, Ki, Kd, target_reflection)

def follow_line():
    """Line follower using PID control for white line on black background."""
    # Read reflection value from color sensor (0-100)
    # In MicroPython, line_sensor is the direct reading, not an object with methods
    reflection = line_sensor

    # Calculate turn adjustment using PID
    turn_speed = line_pid.update(reflection)

    # Calculate motor speeds
    left_speed = base_speed + turn_speed
    right_speed = base_speed - turn_speed

    # Limit speeds to valid range for motors (typically -100 to 100)
    left_speed = max(-100, min(100, int(left_speed)))
    right_speed = max(-100, min(100, int(right_speed)))

    # Run the motors
    motor.run(LEFT_MOTOR_PORT, left_speed)
    motor.run(RIGHT_MOTOR_PORT, right_speed)

def main():
    """Main function that runs the program."""
    # Display a message on the hub's display
    light_matrix.write("Line")
    
    # Short delay to show the message
    time.sleep(1)
    
    # Main control loop
    while True:
        follow_line()
        time.sleep(0.01)  # Small delay between iterations

# Run the main function
main() 