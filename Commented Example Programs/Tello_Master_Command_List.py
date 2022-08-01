#Introduction
"""
This is a list of every command is used in the example scripts for the Tello drone and explaing what they mean.
Because this whole script is a large comment it will not run it is purely a reference list. 
"""

#Importing modules
"""
Depending on what the script is doing diffrent modules  will need to be imported to allow for certain functions to run properly.
modules are python files that contains statements and definitions

from djitellopy import Tello
^This is the importing the Tello class from the djitellopy module and must be used in EVERY script using this drone

import time 
^This imports the module time function allowing for breaks to be taken between operations

import cv2
^This imports the module cv2 which is used for image processing

import numpy as np
^This imports the module numpy which is used for preforming a wide variety of mathematical operations

import pygame
^This imports the module pygame which is used to make games which is how the keyboard imports are read in
"""

#Tello Movement Commands
"""
tello.takeoff()
tello.land()
^These commands tell the Tello to take off or land respectively

tello.move_left(50)
tello.move_right(50)
tello.move_forward(50)
tello.move_backward(50)
^These commands move the Tello on the along the X and Y axis. 
The number inside the brackets () is the distance the drone will travel in centimeter.

tello.rotate_counter_clockwise(360)
tello.rotate_clockwise(180)
^These commands retoate the Tello.
The number inside the brackets () is the distance the drone will roatet in degrees.

tello.move_up(50)
tello.move_down(50)
^These commands move the Tello along the Z axis.
The number inside the brackets () is the distance the drone will travel in centimeter.

tello.flip_forward()
tello.flip_backward()
tello.flip_right()
tello.flip_left()
^These commands flip the tello in diffrent directions.
"""

#Tello Commands 
"""
tello = Tello()
^#This assigns the object Tello() as tello

tello.connect()
^This command connects to the Tello and should be the first line after the variables  

tello.end()
^This command disconnect the Tello and should be the last line of the script

tello.for_back_velocity = 0
tello.left_right_velocity = 0
tello.up_down_velocity = 0
tello.yaw_velocity = 0
tello.speed - 0
^These commands set the velocties of the Tello 

tello.speed = 0
^This command sets the speed of the Tello

tello.enable_mission_pads()
tello.disable_mission_pads()
^These commands enable and disable the ability to read the Tello EDU mission pads 

tello.set_mission_pad_detection_direction(2)
^This command sets which camera on the Tello is scanning the mission pad number
The number inside the brackets () detemines which camera is being used.
0 is only the bottom camera, 1 is only the front camera, 2 is both cameras

tello.get_mission_pad_id()
^This command will say which mission pad is being scanned
print(str(tello.get_mission_pad_id())) This will print the number of the mission pad that is being scanned. 
When nothing is being scanned it will display -1

tello.get_battery()
^This command will say what the battery life of the drone is
print("Battery Percintage:" + str(tello.get_battery())) This will print the battery life to the terminal at the end of the script

tello.streamon()
tello.streamoff()
^These commands turn the video steam of the Tello on and off respectively

tello.get_frame_read()
^This gets the image from the Tello camera
"""

#pygame Commands
"""
pygame.K_SPACE
^This command reads if the defined key has been pressed. The key after the underscore _ is what is being checked.

pygame.init()
^This command initializes all imported pygame modules

pygame.display.set_caption("Tello video stream")
^This command adds a label to the video display 

pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)
^This sets the command refresh rate by creating a repeating timer
This adds the specified event to the pygame event que when ever the specified time has passed. 
In this case the event being called is pygame.USEREVENT + 1 and the time is 1000/FPS which is the time between each frame.

pygame.display.set_caption("Tello video stream")
^This adds a caption to the video stream

pygame.event.get()
^This checks for events such as if any buttons have been pressed or released. These are called user events.
This checks for the most recent event in the que and returns the value.

pygame.USEREVENT
^This calls an event that does not have a key binding

pygame.KEYDOWN
^This is saying which key is being checked 

pygame.display.update()
^This updates the screen
pygame.surfarray.make_surface(frame)
^This converts image that has been processed to a pygame surface so that it can be displayed
"""

#time Commands
"""
time.sleep(5)
^This command adds a pause in between the code the number inside the brackets () is how many seconds it waits 
"""

#Open cv Commands 
"""
frameWidth = width
frameHeight = height
EXPAND THIS

cv2.putText(frame, text, (5, 720 - 5)
^This places the battery percentage text on the screen 
The first number is the thickness and the second number is the location of the text relitive to the bottom left of the screen in X Y values.

cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
^This font size and color of what is being displayed.
The first three values in the () brackets are the color values for the text. The last number is the line thickness. 

cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
^This is converting from the Blue Green Red Color ordering to Red Green Blue

np.rot90(frame)
^This rotates the image from the drone by 90 degrees

np.flipud(frame)
^This flips the image from the tello upside down

cv2.namedWindow("HSV")
^This names the window 

cv2.resizeWindow("HSV",640,240)
^This resizes the window with the 640 being height and 240 being the width

cv2.createTrackbar("HUE Min","HSV",112,179,empty)
^This creates a track bar called HUE Min. The 112 and 179 are the highest and lowest values allowed.

self.screen.blit(frame, (0, 0))
^This places the converted image onto the screen
The numbers in the () brackets are the hight and width

cv2.VideoCapture(1)
^This creates an object of VideoCapture
"""

#Useful Links
"""
https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode
^This is a list of all the pygame functions 

https://djitellopy.readthedocs.io/en/latest/tello/
^This is a list of all the Tello functions
"""