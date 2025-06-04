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
small_image_sensor = ImageSensor(sim, DeviceNames.SMALL_IMAGE_SENSOR_OS)

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


# Starts coppeliasim simulation if not done already
sim.startSimulation()

time.sleep(0.5)
# MAIN CONTROL LOOP
while True:
    battery_low = False
    green_block = False
    compressed = False
    #Battery
    """Indicates when the robot has to charge. 1st step in subsumption architecture"""
    robot_battery = robot.get_battery()
    print(f"Battery: {robot_battery}\n")
    if robot_battery < 0.2:
        """make it go to charger here."""
        battery_low = True
    else:
        #Small image sensor
        """Use for finding and signaling when it has a block. Needs to distinguish between green, red and dark red blocks (compressed). 2nd step in subsumption architecture."""
        small_image_sensor._update_image()
        rgb = small_image_sensor.rgb()
        red, green , blue  = rgb[0], rgb[1], rgb[2]
        print(f"Red: {red}")
        print(f"Green: {green}")
        print(f"Blue: {blue}\n")
        if red > 40 and blue < 10:
            print("RED")
            robot.compress()
        elif green > 55 and red < 25:
            green_block = True
            print("GREEN")
        elif red <10 and green < 10 and blue < 10:
            compressed = True
            print("COMPRESSED BLOCK")
        else:
            #Top image sensor
            """Has to search for the red or blue bin. Only used for this. We only use top 5 rows for this in the 64x64 matrix. 3rd step in subsumption architecture"""
            top_image_sensor._update_image()
            top_rows = top_image_sensor.get_image()[:5,:,:]
            rgb_values = np.mean(top_rows, axis=(0, 1))
            red_top, green_top, blue_top = rgb_values[0], rgb_values[1], rgb_values[2]
            print(f"Red: {red_top}")
            print(f"Green: {green_top}")
            print(f"Blue: {blue_top}\n")
            if compressed: #change two variables below to make it work
                print("COMPRESSED BLOCK DETECTED")
            elif green_block:
                print("GREEN BLOCK DETECTED")
            else:
                #Motor
                """Makes the robot move. Need to implement a random loop so it wanders around when nothing is matched on top. Only wanders when all other layers are not met."""
                left_motor.run(0)
                right_motor.run(0)
                time.sleep(2)
                

    
    
    
    