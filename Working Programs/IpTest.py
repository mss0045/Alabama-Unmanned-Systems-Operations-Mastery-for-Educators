from djitellopy import Tello
import cv2
import numpy as np


######################################################################
width = 640  # WIDTH OF THE IMAGE
height = 480  # HEIGHT OF THE IMAGE
deadZone =100
######################################################################

startCounter =0

# CONNECT TO TELLO
tello = Tello()
tello.connect()