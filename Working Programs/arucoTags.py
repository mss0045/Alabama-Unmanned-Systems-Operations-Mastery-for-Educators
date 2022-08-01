import numpy as np
import cv2, PIL, os
from cv2 import aruco
import numpy as np
import imutils
import time
import math
from djitellopy import Tello

class PID:
    def __init__(self, Pgain, Igain, Dgain): 
        self.PriorVal = 0
        self.Accumulated = 0
        self.pGain = Pgain
        self.iGain = Igain
        self.dGain = Dgain
        self.AverageError =[]


    def update(self,error,dt):
        if (dt<0.001):
            self.Velocity = 0
        else:
            self.Velocity = (self.PriorVal-error)/dt

        self.Accumulated += (0.5*(error - self.PriorVal)+self.PriorVal)*dt

        self.PriorVal = error


        return self.pGain*error + self.iGain*self.Accumulated + self.dGain*self.Velocity 



aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

#--Calibration parameters for tello camera--

ret = 0.6848856450416407

mtx = np.array([[904.63125406,   0.        , 491.22878989],
       [  0.        , 904.63125406, 374.33796981],
       [  0.        ,   0.        ,   1.        ]])

dist = np.array([[ 2.78354755e+00],
       [-2.63908985e+01],
       [ 2.86804889e-03],
       [ 4.29507445e-03],
       [ 6.23304817e+01],
       [ 2.78046156e+00],
       [-2.61836276e+01],
       [ 6.18481595e+01],
       [ 0.00000000e+00],
       [ 0.00000000e+00],
       [ 0.00000000e+00],
       [ 0.00000000e+00],
       [ 0.00000000e+00],
       [ 0.00000000e+00]])

#Initialize connection with Tello 
tello = Tello()
tello.connect()

#Intial movement parameters
tello.for_back_velocity = 0
tello.left_right_velocity = 0
tello.up_down_velocity = 0
tello.yaw_velocity = 0
tello.speed = 0

started = False

# True if you want the tello to takeoff and fly
flightEnabled = True

#PID parameters
PIDLIST = [PID(150,0,-10),PID(-200,0,10),PID(100,0,-50),PID(100,0,-50)]
GoalDistance = 0.9


#Check battery percentage should not fly if under 50%
print(tello.get_battery())

# Start the video stream to the computer
tello.streamoff()
tello.streamon()

#Initializes a timer for rate determination
LastTime = time.time()
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
parameters =  aruco.DetectorParameters_create()


# Start the control loop
while True:


    # Calculate time differential for PID velocity calculations
    dt = time.time() - LastTime
    LastTime = time.time()
    # Read images from the tello drone
    frame_read = tello.get_frame_read()
    frame = frame_read.frame

    if flightEnabled:
        if not started: 
            tello.takeoff()
            started = True

    # Resize image, set to a lower value to possibly speed up refresh rate
    imaxis = imutils.resize(frame, width=960, height=720)
    gray = cv2.cvtColor(imaxis, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, 
                                                        parameters=parameters)
    # SUB PIXEL DETECTION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
    for corner in corners:
        cv2.cornerSubPix(gray, corner, winSize = (3,3), zeroZone = (-1,-1), criteria = criteria)
        
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    length_of_axis = 0.1 # length of the axis that is displayed on the screen
    size_of_marker =  0.19 # side lenght of the marker in meters
    if (len(corners)):
        rvecs,tvecs , _objPoints = aruco.estimatePoseSingleMarkers(corners, size_of_marker, mtx, dist)
        imaxis = aruco.drawDetectedMarkers(imaxis.copy(), corners, ids)

        for i in range(len(tvecs)):
            imaxis = cv2.drawFrameAxes(imaxis, mtx, dist, rvecs[i], tvecs[i], length_of_axis,1)
        if 15 not in ids:
            tello.yaw_velocity = 0
            tello.up_down_velocity = 0
            tello.for_back_velocity = 0
            tello.left_right_velocity = 0
        else:
            for i in range(len(ids)):
                if (ids[i]==15):
                    #cv2.putText(imaxis, text='TX: ' + str(tvecs[i][0]), org=(150, 250), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
                    cv2.putText(imaxis, text='RX: ' + str(rvecs[i][0]), org=(150, 250), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
                    
                    rmat, jacobian = cv2.Rodrigues(rvecs[i], np.zeros((3,3)))
                    WorldAngle = math.acos(rmat[i][2])-1.57
                    cv2.putText(imaxis, text='Yaw: ' + str(WorldAngle), org=(150, 300), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)
                    
                    tello.yaw_velocity = int(PIDLIST[0].update(WorldAngle,dt))
                    tello.up_down_velocity = int(PIDLIST[1].update(tvecs[i][0][1],dt))
                    tello.for_back_velocity = int(PIDLIST[2].update(tvecs[i][0][2] - GoalDistance,dt))
                    tello.left_right_velocity = int(PIDLIST[3].update(tvecs[i][0][0],dt))
    else:
        tello.yaw_velocity = 0
        tello.up_down_velocity = 0
        tello.for_back_velocity = 0
        tello.left_right_velocity = 0
    cv2.putText(imaxis, text='Y: '+str(tello.yaw_velocity), org=(150, 400), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)    
    cv2.putText(imaxis, text='Z: '+str(tello.up_down_velocity), org=(150, 450), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)    
    cv2.putText(imaxis, text='F: '+str(tello.for_back_velocity), org=(150, 500), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)    
    
    cv2.putText(imaxis, text='L: '+str(tello.left_right_velocity), org=(150, 550), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)    
    cv2.putText(imaxis, text='dt: '+str(dt), org=(150, 600), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 255, 0),thickness=3)    
    cv2.imshow("TelloView", imaxis)
   # SEND VELOCITY VALUES TO TELLO FOR MOVEMENT
    if flightEnabled:
        if tello.send_rc_control:
            tello.send_rc_control(tello.left_right_velocity, tello.for_back_velocity, tello.up_down_velocity, tello.yaw_velocity)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        tello.land()
        break
  
cv2.destroyAllWindows()