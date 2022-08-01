"""
This script uses the Tello EDU's ability to read in the provided mission pads. 
Instead of explicitly commanding the drone to preform specific movemnts it will preform them based on which mission pad number is being scanned.
This adds a level of decision making to the drone and lessens the work load of the programmers.
"""
from djitellopy import Tello
import time 

# create and connect
tello = Tello()
tello.connect()

# configure drone
tello.enable_mission_pads()
tello.set_mission_pad_detection_direction(2)
# 0 means it is only the bottom camera, 1 is only the front camera, 2 is both cameras
tello.takeoff()

pad = tello.get_mission_pad_id()

# detect and react to pads until we see pad #1
while pad != 1:
    if pad == 3:
        print("Pad 3")
        tello.move_back(50)
        tello.rotate_clockwise(360)
        time.sleep(5)

    if pad == 4:
        print("Pad 4")
        tello.flip_forward()
        tello.move_up(50)
        time.sleep(5)

    pad = tello.get_mission_pad_id()
"""
can this pad = tello.get_mission_pad_id() be removed?
"""
# graceful termination
tello.disable_mission_pads()
tello.land()

#This prints out the Tello's battery percintage to the terminal
print("Battery Percintage:" + str(tello.get_battery()))
tello.end()