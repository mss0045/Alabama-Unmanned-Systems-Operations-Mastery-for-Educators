"""
This script uses the Tello's front camera to track a colored object of a certain size.
Based on the location of the object in relation to the center of the screen it will move the drone in different directions.
"""
from djitellopy import Tello#This imports the DJI module and Tello class
import cv2#This imports the cv2 module
import numpy as np#This imports the numpy module as num

width = 480#This sets the width of the image frame
height = 360#This sets the hight of the image frame
deadZone =80#This sets the size of the central square in the bottom left #######CHECK TO SEE IF THE LOCATION IS CORRECT

startCounter =0#This creates a varbible which is a flag to determine if weather the Tello has taken off yet

tello = Tello()#This assigns the object Tello() as tello
tello.connect()#This connects to the Tello
tello.for_back_velocity = 0#This sets the forward and backward velocities to 0
tello.left_right_velocity = 0#This sets the left and right velocities to 0
tello.up_down_velocity = 0#This sets the up and down velocities to 0
tello.yaw_velocity = 0#This sets the yaw velocity to 0
tello.speed = 0#This sets the speed velocity to 0
GoalArea = 400#This sets the goal area in pixels of the tracked object which corliates to the distance of the obkect
lastx = 0#This creates a variable which is used for numerial derivatives 
lasty = 0#This creates a variable which is used for numerial derivatives 
lastArea = 0#This creates a variable which is used for numerial derivatives 

dx=0#This variable store the differance in the x value from the center of the screen of the tracked object
dy=0#This variable store the differance in the y value from the center of the screen of the tracked object
dArea=0##This variable store the differance in the goal area value from the center of the screen of the tracked object
DYaw = 0.0#This variable stores the derivatie term value for the yaw velocity
DFor = 0.0#This variable stores the derivatie term value for the forward velocity
DVert= 0.0#This variable stores the derivatie term value for the virtical velocity
vx = 0#This variable stores the velocities of the Tello
vy = 0#This variable stores the velocities of the Tello
vArea = 0#This variable stores the rate of change of the area in pixels

PYaw=0.2#This sets the proportional gains for the yaw controler
PFor=0.1#This sets the proportional gains for the forward controler
PVert=-0.3#This sets the proportional gains for the virtical controler

print(tello.get_battery())#This prints the battery life of the Tello

tello.streamoff()#This turns the Tello video stream off
tello.streamon()#this turns the Tello video stream on

frameWidth = width#This renames the frameWidth variable to width
frameHeight = height#This renames the frameHeight variable to height
cap = cv2.VideoCapture(1)#This assines cap to a VideoCapture object
cap.set(3, frameWidth)#This sets the image frame width of the video capture
cap.set(4, frameHeight)#This sets the image frame height of the video capture
cap.set(10,200)#This sets the bightness 10 is the identifier and 200 is the brightness value  

global imgContour#This assigns imgContour as a variable so it can be used throught the whole script
global dir#This assigns dir as a variable so it can be used throught the whole script
def empty(a):#This an empty function that does nothing and used as the functions that is called when the track bar is moved
    pass#This acts as an identifier that does nothing

cv2.namedWindow("HSV")#This names a window to HSV
cv2.resizeWindow("HSV",640,240)#This resizes the window size to 640x240 pixels
cv2.createTrackbar("HUE Min","HSV",112,179,empty)#This creates a trackbar called HUE Min with the 112 and 179 being the lowest and highest numbers
cv2.createTrackbar("HUE Max","HSV",150,179,empty)#This creates a trackbar called HUE Max with the 150 and 179 being the lowest and highest numbers
cv2.createTrackbar("SAT Min","HSV",81,255,empty)#This creates a trackbar called SAT Min with the 81 and 255 being the lowest and highest numbers
cv2.createTrackbar("SAT Max","HSV",255,255,empty)#This creates a trackbar called SAT Man with the 255 and 255 being the lowest and highest numbers
cv2.createTrackbar("VALUE Min","HSV",81,255,empty)#This creates a trackbar called VALUE Min with the 81 and 255 being the lowest and highest numbers
cv2.createTrackbar("VALUE Max","HSV",255,255,empty)#This creates a trackbar called VALUE Man with the 255 and 255 being the lowest and highest numbers

cv2.namedWindow("Parameters")#This names a window to Parameters
cv2.resizeWindow("Parameters",640,240)#This resizes the window size to 640x240 pixels
cv2.createTrackbar("Threshold1","Parameters",118,255,empty)#This creates a trackbar called Threshold1 with the 118 and 225 being the lowest and highest numbers
cv2.createTrackbar("Threshold2","Parameters",95,255,empty)#This creates a trackbar called Threshold2 with the 95 and 225 being the lowest and highest numbers
cv2.createTrackbar("Area","Parameters",100,30000,empty)#This creates a trackbar called Area with the 100 and 30000 being the lowest and highest numbers


def stackImages(scale,imgArray):
    rows = len(imgArray)#This gets the number rows from the imagie
    cols = len(imgArray[0])#This gets the number of collums from the imagie
    rowsAvailable = isinstance(imgArray[0], list)#This makes sure that there are rows in the imaige
    width = imgArray[0][0].shape[1]#This checks width of the image 
    height = imgArray[0][0].shape[0]#This checks the height of the image
    if rowsAvailable:#This says that if there are rows in the image it iderates for the row and collum for next 3
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:#This is saying if it is the first image in the array to resize it to be 0
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:#This is saying that if it is not the first image to resize the image to the size of zero zero
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:#This changes it from a gray image to colored
                    imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)

        imageBlank = np.zeros((height, width, 3), np.uint8)#This gets the horizontal size of the blank image 
        hor = [imageBlank]*rows
        for x in range(0, rows):#This combines one row of data into a single number
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:#This runs if there are not rows in the image and is a repeat of what is above
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
    for cnt in contours:#This goes though each contor and calculates the area 
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

            ###This is where the calculations from the previous and current image happen 
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
            ###
            

def display(img):#THIS MAKES THE LINE THAT POINTS AT THE CENTER OF THE COLOR
    cv2.line(img,(int(frameWidth/2)-int(frameWidth/6),0),(int(frameWidth/2)-int(frameWidth/6),frameHeight),(255,255,0),3)
    cv2.line(img,(int(frameWidth/2)+int(frameWidth/6),0),(int(frameWidth/2)+int(frameWidth/6),frameHeight),(255,255,0),3)
    cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)),5,(0,0,255),5)
    cv2.line(img, (0,int(frameHeight / 2) - int(frameHeight/6)), (frameWidth,int(frameHeight / 2) - int(frameHeight/6)), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) + int(frameHeight/6)), (frameWidth, int(frameHeight / 2) + int(frameHeight/6)), (255, 255, 0), 3)

while True:#This is what actully runs the porgram

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