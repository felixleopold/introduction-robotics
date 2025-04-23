from robots import *
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import time

client = RemoteAPIClient()
sim = client.require("sim")

# HANDLES FOR ACTUATORS AND SENSORS
left_motor = Motor(sim, DeviceNames.MOTOR_LEFT_LINE, Direction.CLOCKWISE)
right_motor = Motor(sim, DeviceNames.MOTOR_RIGHT_LINE, Direction.CLOCKWISE)
color_sensor = ImageSensor(sim, DeviceNames.IMAGE_SENSOR_LINE)


class PIDController:
    def __init__(self, Kp, Ki, Kd, target):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.target = target

        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time() # Initialize last_time here

    def update(self, current_value):
        """Calculates PID output based on the current sensor value."""
        current_time = time.time()
        dt = current_time - self.last_time

        # avoid division by zero and ensure dt is positive
        if dt <= 0:
            dt = 0.0000000000001 # set dt to a very small value instead of 0

        error = self.target - current_value

        # update the integral term, the accumulated error
        # this needs to be weighted by the time difference (dt)
        # so multiply the error by dt which gives an estimation of the area under the curve
        # and then add it to the previous integral
        self.integral += error * dt


        # calculate the derivative term, the current rate of change of the error
        change_in_error = error - self.previous_error # how much the error has changed since the last iteration
        derivative = change_in_error / dt # divide by dt to get the rate of change

        # calculate the PID output
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative # combine the terms

        # set the current time and error as the previous time and error for the next iteration
        self.previous_error = error
        self.last_time = current_time

        return output


def is_red_detected(color_sensor):
    """
    Calculates the relative intensity of the red channel compared to
    other channels
    """
    red_ratio_threshold = 1.5
    red, green, blue = color_sensor.rgb()
    print(red, green, blue)
    red_intensity = red / (green + blue)

    return red_intensity > red_ratio_threshold


def is_blue_detected(color_sensor):
    """
       Calculates the relative intensity of the blue channel compared to
       other channels
       """
    blue_ratio_threshold = 1.5
    red, green, blue = color_sensor.rgb()
    blue_intensity = blue / (red + green)

    return blue_intensity > blue_ratio_threshold

# PID Constants:

# We need to tune these values
Kp = 0.08 # proportional
Ki = 0.0000001 # integral
Kd = 0.0001 # derivative

target_reflection = 50 # we don't know this yet
base_speed = 2

line_pid = PIDController(Kp, Ki, Kd, target_reflection)


def follow_line(base_speed):
    """
    A very simple line follower that should be improved.
    """
    color_sensor._update_image() # Updates the internal image
    reflection = color_sensor.reflection() # Gets the reflection from the image
    print(reflection)

    turn_speed = line_pid.update(reflection)

    left_speed = base_speed + turn_speed
    right_speed = base_speed - turn_speed

    # actually run the motors
    left_motor.run(speed=left_speed) # Runs the left motor at speed=5
    right_motor.run(speed=right_speed) # Runs the right motor at speed=5

# Starts coppeliasim simulation if not done already
sim.startSimulation()

# MAIN CONTROL LOOP
while True:
	follow_line(base_speed)
	time.sleep(0.02) # small delay to avoid overwhelming my poor mac

