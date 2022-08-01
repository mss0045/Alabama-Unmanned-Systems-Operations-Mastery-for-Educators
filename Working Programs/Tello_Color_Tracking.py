"""
This script uses the Tello's front camera to track a colored object of a certain size.
Based on the location of the object in relation to the center of the screen it will move the drone in different directions.
"""
from djitellopy import Tello
import cv2
import numpy as np

######################################################################
width = 480  # WIDTH OF THE IMAGE
height = 360  # HEIGHT OF THE IMAGE
deadZone =80
######################################################################

startCounter =0
# CONNECT TO TELLO
tello = Tello()
tello.connect()
tello.for_back_velocity = 0
tello.left_right_velocity = 0
tello.up_down_velocity = 0
tello.yaw_velocity = 0
tello.speed = 0
GoalArea = 400
lastx = 0
lasty = 0
lastArea = 0

dx=0
dy=0
dArea=0
DYaw = 0.0
DFor = 0.0
DVert= 0.0
vx = 0
vy = 0
vArea = 0

PYaw=0.2
PFor=0.1
PVert=-0.3

print(tello.get_battery())

tello.streamoff()
tello.streamon()
######################## 

frameWidth = width
frameHeight = height
# cap = cv2.VideoCapture(1)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# cap.set(10,200)

global imgContour
global dir
def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,240)
cv2.createTrackbar("HUE Min","HSV",40,50,empty)#112 179
cv2.createTrackbar("HUE Max","HSV",50,60,empty)#150 179
cv2.createTrackbar("SAT Min","HSV",140,150,empty)#81 255
cv2.createTrackbar("SAT Max","HSV",245,255,empty)#255 255
cv2.createTrackbar("VALUE Min","HSV",90,100,empty)#81 255
cv2.createTrackbar("VALUE Max","HSV",212,222,empty)#255 255

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",118,255,empty)
cv2.createTrackbar("Threshold2","Parameters",95,255,empty)
cv2.createTrackbar("Area","Parameters",100,30000,empty)


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

# Computes area of the shape and calculates how to move drone based on that area
def getContours(img,imgContour):
    global dir
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    MaxAreaObject = []
    MaxArea = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > MaxArea:
            MaxAreaObject = cnt
            MaxArea = area

        

    if len(MaxAreaObject):
        area = cv2.contourArea(MaxAreaObject)
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        if area > areaMin:
            global dy
            global dx
            global dArea
            global lastx
            global lasty
            global lastArea
            global vx
            global vy
            global vArea

            
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            #print(len(approx))
            x , y , w, h = cv2.boundingRect(approx)
            cx = int(x + (w / 2))  # CENTER X OF THE OBJECT
            cy = int(y + (h / 2))  # CENTER X OF THE OBJECT
            dx = (cx-frameWidth/2)
            dy = (cy-frameHeight/2)
            dArea = (GoalArea-area)
            if lastArea != 0: 
                vx = dx-lastx
                vy = dy-lasty
                vArea = dArea - lastArea
            else:
                vx=0
                vy=0
                vArea=0
            lastx = dx
            lasty = dy
            lastArea = dArea
            cv2.line(imgContour, (int(frameWidth/2),int(frameHeight/2)), (cx,cy),(0, 0, 255), 3)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,(0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0, 255, 0), 2)
            cv2.putText(imgContour, " " + str(int(x)) + " " + str(int(y)), (x - 20, y - 45), cv2.FONT_HERSHEY_COMPLEX,0.7,(0, 255, 0), 2)
        else: 
            dx=0
            dy=0
            dArea=0
            lastArea = 0
            
            

def display(img):
    cv2.line(img,(int(frameWidth/2)-int(frameWidth/6),0),(int(frameWidth/2)-int(frameWidth/6),frameHeight),(255,255,0),3)
    cv2.line(img,(int(frameWidth/2)+int(frameWidth/6),0),(int(frameWidth/2)+int(frameWidth/6),frameHeight),(255,255,0),3)
    cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)
    cv2.line(img, (0,int(frameHeight / 2) - int(frameHeight/6)), (frameWidth,int(frameHeight / 2) - int(frameHeight/6)), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) + int(frameHeight/6)), (frameWidth, int(frameHeight / 2) + int(frameHeight/6)), (255, 255, 0), 3)

while True:

    # GET THE IMAGE FROM TELLO
    frame_read = tello.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))
    imgContour = img.copy()
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Get min and max Hue, Saturation, and Value values
    h_min = cv2.getTrackbarPos("HUE Min","HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    # Bitwise conjugates image with image and converts to grayscale
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHsv,lower,upper) # Mask is always true
    result = cv2.bitwise_and(img,img, mask = mask) 
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Blurs image, finds edges, makes edges bigger, runs getContours function
    imgBlur = cv2.GaussianBlur(result, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil, imgContour)
    display(imgContour)

    ################# FLIGHT
    #if startCounter == 0: g
    #   tello.takeoff()
    #   startCounter = 1

    #print("dx: " + str(dx) + "\t dy: " + str(dy) + "\t dA: " + str(dArea)+"\tvx: " + str(vx) + "\t vy: " + str(vy) + "\t vA: " + str(vArea))
    tello.yaw_velocity = int(PYaw*dx-DYaw*vx)
    tello.up_down_velocity = int(PVert*dy-DVert*vy)
    tello.for_back_velocity = int(PFor*dArea-DFor*vArea)
    tello.left_right_velocity = 0
   # SEND VELOCITY VALUES TO TELLO FOR MOVEMENT
   # if tello.send_rc_control:
   #    tello.send_rc_control(tello.left_right_velocity, tello.for_back_velocity, tello.up_down_velocity, tello.yaw_velocity)

    # Shows your 2x2 video 
    stack = stackImages(0.9, ([img, result], [imgDil, imgContour]))
    cv2.imshow('Horizontal Stacking', stack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Battery Percintage:" + str(tello.get_battery()))
        tello.land()
        break

# cap.release()
cv2.destroyAllWindows()