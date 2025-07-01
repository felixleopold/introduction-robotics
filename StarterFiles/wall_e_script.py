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

last_image_update_time = 0
interval = 0.005
green_block = False
compressed = False

def update_image(interval=interval):
    global last_image_update_time
    
    current_time = time.time()

    if current_time - last_image_update_time >= interval:
        small_image_sensor._update_image()
        top_image_sensor._update_image()
        last_image_update_time = current_time
        
    middle_camera = small_image_sensor.get_image()[28:36,28:36,:]
    rgb = np.mean(middle_camera,axis=(0,1))
    red, green , blue  = rgb[0], rgb[1], rgb[2]

    top_rows = top_image_sensor.get_image()[:5,28:36,:]
    rgb_values = np.mean(top_rows, axis=(0, 1))
    red_top, green_top, blue_top = rgb_values[0], rgb_values[1], rgb_values[2]
    
    return red, green, blue, red_top, green_top, blue_top

def update_image_bottom():
    small_image_sensor._update_image()
    bottom_rows = small_image_sensor.get_image()[60:64,:,:]
    rgb_values_bottom = np.mean(bottom_rows, axis=(0,1))
    red_bottom, green_bottom, blue_bottom = rgb_values_bottom[0], rgb_values_bottom[1], rgb_values_bottom[2]
    return red_bottom, green_bottom, blue_bottom

def straight(speed=3.0):
    left_motor.run(speed)
    right_motor.run(speed)

def turning(first=.5, second=-.5, scaling=1.0):
    left_motor.run(first*scaling)
    right_motor.run(second*scaling)
    
def wandering():
    rng = np.random.rand()
    if rng <= 0.98:
        turning()
    else:
        straight()
        time.sleep(1)

def turn_when_stuck():
    if red_top == 0 and green_top == 0 and blue_top == 0:
        return True
    return False

def search_bin(is_green_block=False, interval=0.01):
    global green_block,compressed
    print("SEARCHING BIN")

    _,_,_,red_top, green_top, blue_top = update_image(interval)

    if turn_when_stuck():
        print("turning")
        turning()
    else:
    
        if is_green_block:
            if look_for_green():
                if red_top == 0:
                    print("BLUE BIN FOUND")
                    straight(3)
                    return True
                else:
                    print("Blue bin not found, wandering")
                    wandering()
                    return False
            else:
                print("LOST GREEN BLOCK, TURNING AND WANDERING AGAIN")
                green_block=False
                return True
        if not is_green_block:
            if look_for_compressed():
                if green_top <= 2 and blue_top <= 2 and abs(red_top-123) <= 10:
                    print("RED BIN FOUND")
                    straight(3)
                    return True
                else:
                    print("Red bin not found, wandering")
                    wandering()
                    return False
            else:
                print("LOST COMPRESSED BLOCK, TURNING WANDER AGAIN")
                compressed = False
                return True
        else:
            return False

def check_block_dropped(is_compressed_block=True):
    red, green, blue,red_top,green_top,blue_top = update_image(interval)
    
    #checks if we are not stuck on wall.
    if turn_when_stuck():
        print("turning")
        turning()
    
    else:
        if is_compressed_block:
            if abs(red-123) <= 2 and abs(green-2) <=2 and abs(blue-2) <= 2:
                return True
            else:
                return False
        if not is_compressed_block:
            if red <= 2 and abs(green-113) <= 2:
                return True
            else:
                return False

def dont_drop_in_bins():
    if abs(red-123) <= 2 and abs(green-2) <=2 and abs(blue-2) <= 2:
            print("Red bin found without block, turning")
            return True
    elif red <= 2 and abs(green-113) <= 2:
            print("blue bin found without block, turning")
            return True
    print("No bins found, continue wandering")
    return False

def look_for_compressed():
    red, green, blue,_,_,_ = update_image(interval)
    if abs(red-5) <= 25 and abs(green-5) <= 25 and abs(blue-5) <= 25:
        return True
    return False

def look_for_green():
    red, green, blue,_,_,_ = update_image(interval)
    if abs(red-50) <= 10 and abs(green - 155) <= 15 and abs(blue-13) <= 10:
        return True
    print("Stop looking for green")
    return False



# Starts coppeliasim simulation if not done already
sim.startSimulation()

time.sleep(0.5)
# MAIN CONTROL LOOP
while True:
    """Trial runs"""
    #Print the robots battery
    robot_battery = robot.get_battery()
    print(f"Battery: {robot_battery}\n")

    #Updates the image at every interval (set to t=0.005 now)
    red, green, blue, red_top, green_top, blue_top = update_image(interval)

    print(f"Red: {red}")
    print(f"Green: {green}")
    print(f"Blue: {blue}\n")

    print("MIDDLE TOP:")
    print(f"Red: {red_top}")
    print(f"Green: {green_top}")
    print(f"Blue: {blue_top}\n")

    #Make sure the robot turns when it's stuck, most important in the architecture because a robot thats stuck cant 
    #gather any points. Gets checked at every interval
    if turn_when_stuck():
        print("turning")
        turning()
        continue

    #Make sure the robot doesnt drive into one of the bins, second step because falling in bin ends the simulation:
    if not (green_block or compressed):
        if dont_drop_in_bins():
            turning()
            continue

    #Make sure the robot charges at low battery
    if robot_battery < 0.2:
        while robot_battery < 1:
            red, green, blue,_,_,_ = update_image(interval)
            if red > 85 and blue > 20 and green > 60:
                print("CHARGING STATION FOUND")
                robot_recharge = robot.get_battery()
                if robot_recharge == 1:
                    robot_battery = 1
                    break
                else:
                    red_bottom, green_bottom, blue_bottom = update_image_bottom()
                    if abs(red_bottom-242) < 5 and abs(green_bottom-242) < 5 and abs(blue_bottom-5) <= 5:
                        time.sleep(2)
                        straight(0)
                    else:
                        straight(3)
            else:
                wandering()     
            continue

    #If we have a green block caught, ignore all else and start searching for red bin
    if green_block:
        while not search_bin(is_green_block=True):
            print("Blue bin not found.")
            wandering()
        else:
            if check_block_dropped(is_compressed_block=False):
                print("Block is dropped")
                straight(-3)
                time.sleep(1)
                turning()
                time.sleep(1.5)
            else:
                print("Blue bin found, driving over there")
                straight(3)
        continue

    #if we have a compressed block, ignore all else and search for red bin
    if compressed: 
        print("ENTERED COMPRESSED CODEBLOCK")
        while not search_bin():
            print("Red bin not found")
            wandering()
        else:
            if check_block_dropped():
                print("Block is dropped")
                straight(-3)
                time.sleep(1)
                turning()
                time.sleep(1.5)
            else:
                print("Red bin found, driving over there")
                straight(3)
        continue


    #Checks if it sees a green block
    if abs(red-50) <= 10 and abs(green - 155) <= 15 and abs(blue-13) <= 10:
        green_block = True
        print("GREEN BLOCK FOUND")
        straight(3)
        time.sleep(.5)
        continue

    #Looks for compressed block
    if abs(red-5) <= 25 and abs(green-5) <= 25 and abs(blue-5) <=25:
        print("COMPRESSED BLOCK FOUND")
        compressed = True
        straight(0)
        time.sleep(1)
        continue
    
    #Checks for red blocks
    if abs(red-110) < 20 and abs(green-60) < 25:
        print("RED")
        straight(3)
        time.sleep(.5)
        robot.compress()
        continue
    
    #Wandering when none of the statements above is matched
    wandering()
    # left_motor.run(0)
    # right_motor.run(0)
    # time.sleep(1)

    