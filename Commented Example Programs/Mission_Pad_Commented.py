"""
This script uses the Tello EDU's ability to read in the provided mission pads. 
Instead of explicitly commanding the drone to preform specific movemnts it will preform them based on which mission pad number is being scanned.
This adds a level of decision making to the drone and lessens the work load of the programmers.
"""
from djitellopy import Tello#This imports the DJI module and Tello class
import time#This imports the time module

tello = Tello()#This assigns the object Tello() as tello
tello.connect()#This allows the script to connect to the Tello to send commands

tello.enable_mission_pads()#This turns on the Tello's ability to scan the mission pads
tello.set_mission_pad_detection_direction(2)#This determines which camera the Tello uses to scan for the mission pads
tello.takeoff()#This commands the Tello to take off

pad = tello.get_mission_pad_id()#This renames the function tello.get_mission_pad_id() as pad to simplify the code 

while pad != 1:#This while loop will continue running until the #1 mission pad is scanned 
    if pad == 3:#If mission pad #3 is scanned this will run
        print("Pad 3")#This will print Pad 3 to the terminal
        tello.move_back(30)#This moves the Tello backwards 30 centimeters
        tello.rotate_clockwise(360)#This rotates the Tello to the clockwise 360 degrees
        time.sleep(5)#This adds a 5 second delay in the script before running the next line

    if pad == 4:#If mission pad #4 is scanned this will run
        print("Pad 4")#This will print Pad 3 to the terminal
        tello.flip_forward()#This flips the Tello forward
        time.sleep(5)#This adds a 5 second delay in the script before running the next line

    pad = tello.get_mission_pad_id()#This renames the function tello.get_mission_pad_id() as pad to simplify the code 

tello.disable_mission_pads()#This turns off the Tello's ability to scan the mission pads
tello.land()#This commands the Tello to land

print("Battery Percintage:" + str(tello.get_battery()))#This has the Tello display its battery life to the terminal 
tello.end()#This disconnects the Tello ending the script