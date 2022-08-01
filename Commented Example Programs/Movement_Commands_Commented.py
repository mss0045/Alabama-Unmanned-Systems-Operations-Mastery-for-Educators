"""
This script is the most basic form of sending movement commands to the Tello drone.
There is no automation in this script so every action that is preformed must be written.
"""
from djitellopy import Tello#This imports the DJI module and Tello class

tello = Tello()#This assigns the object Tello() as tello
tello.connect()#This allows the script to connect to the Tello to send commands

tello.takeoff()#This commands the Tello to take off

tello.move_left(50)#This moves the Tello to the left 50 centimeters
tello.move_right(50)#This moves the Tello to the right 50 centimeters
tello.rotate_counter_clockwise(360)#This rotates the Tello to the counter clockwise 360 degrees
tello.move_forward(50)#This moves the Tello forward 50 centimeters
tello.rotate_clockwise(180)#This rotates the Tello to the clockwise 180 degrees
tello.move_forward(50)#This moves the Tello forward 50 centimeters
tello.move_up(50)#This moves the Tello upward 50 centimeters
tello.move_down(50)#This moves the Tello downward 50 centimeters
tello.rotate_counter_clockwise(180)#This rotates the Tello to the counter clockwise 180 degrees
tello.flip_forward()#This flips the Tello forward

tello.land()#This commands the Tello to land
print("Battery Percintage:" + str(tello.get_battery()))#This has the Tello display its battery life to the terminal 
tello.end()#This disconnects the Tello ending the script