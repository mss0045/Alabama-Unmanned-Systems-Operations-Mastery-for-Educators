"""
This script is the most basic form of sending movement commands to the Tello drone.
There is no automation in this script so every action that is preformed must be written.
"""
from djitellopy import Tello

tello = Tello()
tello.connect()

tello.takeoff()

tello.move_left(50)
tello.move_right(50)
tello.rotate_counter_clockwise(360)
tello.move_forward(50)
tello.rotate_counter_clockwise(180)
tello.move_forward(50)
tello.move_up(50)
tello.move_down(50)
tello.rotate_counter_clockwise(180)
tello.flip_forward()

tello.land()
print("Battery Percintage:" + str(tello.get_battery()))
tello.end()