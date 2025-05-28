from robots import *
import time
from coppeliasim_zmqremoteapi_client import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

client = RemoteAPIClient()
sim = client.require("sim")

# HANDLES FOR ACTUATORS AND SENSORS
robot = Robot_OS(sim, DeviceNames.ROBOT_OS)

top_image_sensor = ImageSensor(sim, DeviceNames.TOP_IMAGE_SENSOR_OS)
red = top_image_sensor.rgb()[0]
green = top_image_sensor.rgb()[1]
blue = top_image_sensor.rgb()[2]

small_image_sensor = ImageSensor(sim, DeviceNames.SMALL_IMAGE_SENSOR_OS)
red_small = top_image_sensor.rgb()[0]
green_small = top_image_sensor.rgb()[1]
blue_small = top_image_sensor.rgb()[2]

left_motor = Motor(sim, DeviceNames.MOTOR_LEFT_OS, Direction.CLOCKWISE)
right_motor = Motor(sim, DeviceNames.MOTOR_RIGHT_OS, Direction.CLOCKWISE)

# HELPER FUNCTION
def show_image(image):
    plt.imshow(image)
    plt.show()

#Robot information
#If both red and green top image sensor > 73: It sees the charging station
#If red image top image sensor = 0: stop and turn around. Green block has fallen in blue bin and we can go on. 
#If both green and blue top image sensor = 0: turn around. Red block has fallen into storage bin. 

if red > 40 and green<23 and blue < 7:
    """It knows it has a red block"""


# Starts coppeliasim simulation if not done already
sim.startSimulation()

time.sleep(0.5)

# MAIN CONTROL LOOP
while True:
    def charge():
        """Has to find the charging station first, then has to bring the robot there and wait till battery is 1."""
        pass
    #Top image sensor
    """Has to search for the red or blue bin. Only used for this. We only use top 5 rows for this in the 64x64 matrix. 3rd step in subsumption architecture"""
    top_image_sensor._update_image()
    top_image_sensor.image = top_image_sensor.get_image()[:5,:,:]
    print(f"Red: {top_image_sensor.rgb()[0]}")
    print(f"Green: {top_image_sensor.rgb()[1]}")
    print(f"Blue: {top_image_sensor.rgb()[2]}\n")
    
    #Battery
    """Indicates when the robot has to charge. 1st step in subsumption architecture"""
    robot_battery = robot.get_battery()
    print(f"Battery: {robot_battery}\n")
    if robot_battery < 0.2:
        charge() 
    else:
        #Small image sensor
        """Use for finding and signaling when it has a block. Needs to distinguish between green, red and dark red blocks (compressed). 2nd step in subsumption architecture."""
        small_image_sensor._update_image()
        red, green, blue = small_image_sensor.rgb()
        print(f"Red: {red}")
        print(f"Green: {green}")
        print(f"Blue: {blue}\n")
        if red > 40:
            robot.compress()
        else:
            pass

    
    #Motor
    """Makes the robot move. Need to implement a random loop so it wanders around when nothing is matched on top. Only wanders when all other layers are not met."""
    left_motor.run(.5)
    right_motor.run(.5)
    
    #Timer
    """Used for input delay on the terminal"""
    time.sleep(5)