"""
This script uses keyboard inputs as movement commands allowing for manlue control of the drone using a laptop or computer.
By using keyboard inputs it allows for an infinite amount of movement commands to be sent to the drone making the program more condensed. 
"""
from djitellopy import Tello#This imports the DJI module and Tello class
import time#This imports the time module
import cv2#This imports the cv2 module
import numpy as np#This imports the numpy module as num
import pygame#This imports the pygame module

S = 60#This sets the speed of the Tello
FPS = 120#This determines how many frames per second will be displayed

UP = pygame.K_SPACE#This renames the SPACE key function as UP
DOWN = pygame.K_c#This renames the c key function as DOWN
TURNLEFT = pygame.K_q#This renames the q key function as TURNLEFT
TURNRIGHT = pygame.K_e#This renames the e key function as TURNRIGHT
MOVELEFT = pygame.K_a#This renames the a key function as MOVELEFT
MOVERIGHT = pygame.K_d#This renames the d key function as MOVERIGHT
MOVEFORWARD = pygame.K_w#This renames the w key function as MOVEFORWARD
MOVEBACK = pygame.K_s#This renames the s key function as MOVEBACK

class FrontEnd(object):#This is the class definition of an object
    def __init__(self):#upon creation of a front end object the init function will be called.
        #The reason for calling this function is to initilize all the values needed to run the program
        pygame.init()#This initializes the imported pygame modules
        pygame.display.set_caption("Tello video stream")#This adds a caption to the Tello video stream
        self.screen = pygame.display.set_mode([960, 720])#This set the screen size to be 960 by 720 pixels
        self.tello = Tello()#This assigns the object Tello() as self.tello

        self.for_back_velocity = 0#This sets the forward and backward velocities 
        self.left_right_velocity = 0#This sets the left and right velocities 
        self.up_down_velocity = 0#This sets the upward and downward velocities 
        self.yaw_velocity = 0#This sets the yaw velocity
        self.speed = 10#This sets the movement speed

        self.send_rc_control = False#This sets the variable self.send_rc_control to be false.
        #this is done so that no movement commands are sent until the Tello is started

        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)#This sets the command refresh rate by creating a repeating timer
        #This adds the specified event to the pygame event que when ever the specified time has passed. 
        #In this case the event being called is pygame.USEREVENT + 1 and the time is 1000/FPS which is the time between each frame.

    def run(self):#The run function connects to the Tello and contains the loop that executes commands
        self.tello.connect()#This allows the script to connect to the Tello to send commands
        self.tello.set_speed(self.speed)#This sets the speed of the Tello
        self.tello.streamoff()#This turns the Tello stream off
        self.tello.streamon()#This turns the Tello stream on

        frame_read = self.tello.get_frame_read()#This gets the image from the Tello camera 

        should_stop = False #This variable flags that the while loop should run, when it is true the command loop ends.

        while not should_stop:#This while loop runs the commands, while the should stop variable is false

            for event in pygame.event.get(): #This checks to see if any buttons have been pressed
                if event.type == pygame.USEREVENT + 1: #This checks to see if it should send a command to the Tello
                    self.update()  #This sends the command to the Tello
                elif event.type == pygame.QUIT: #This checks to see if the x button in the top right has been pressed
                    should_stop = True #This sets should stop to true, ending the loop
                elif event.type == pygame.KEYDOWN: #This checks to see if a key on the keyboard has been pressed
                    if event.key == pygame.K_ESCAPE: #This checks if the key pressed was escape
                        should_stop = True #This sets should stop to true, ending the loop
                    else: #This runs if the key was not escape, then run the keydown function
                        self.keydown(event.key) #This runs the keydown function, passing the key that was pressed
                elif event.type == pygame.KEYUP: #This checks to see if a pressed key has been released
                    self.keyup(event.key) #This sends the released key to the keyup function
            if frame_read.stopped: #This checks if images are still being retrieved, if not, end the loop
                break

            self.screen.fill([0, 0, 0]) #This sets the whole screen to white

            frame = frame_read.frame #This tries to get an image from the tello camera

            text = "Battery: {}%".format(self.tello.get_battery()) #This gets the tello battery percentage and converts it to text
            cv2.putText(frame, text, (5, 720 - 5), #This places the battery percentage text on the screen 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2) #This sets the font, size, and color of the text being displayed
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #This is converting from the Blue Green Red Color ordering to Red Green Blue
            frame = np.rot90(frame) #This rotates the image from the drone by 90 degrees
            frame = np.flipud(frame) #This flips the image from the tello upside down
            frame = pygame.surfarray.make_surface(frame) #This converts the image that has been processed to a pygame surface so that it can be displayed
            self.screen.blit(frame, (0, 0)) #This places the converted image onto the screen
            pygame.display.update() #This updates the screen
            time.sleep(1 / FPS) #This waits for amount of time required to make the framerate equal to the FPS value
        self.tello.end()#This disconnects the Tello 



    def keydown(self, key):#This section inputs a key and based on the key modifies the movement variables
        if key == MOVEFORWARD:#This checks if the assined forward movement key had been pressed
            self.for_back_velocity = S#This sets the forward velocity to 5 cm/s
        elif key == MOVEBACK:#This checks if the assined moveforward movement key had been pressed
            self.for_back_velocity = -S#This sets the backwards velocity to 5 cm/s
        elif key == MOVELEFT:#This checks if the assined left movement key had been pressed
            self.left_right_velocity = -S#This sets the left velocity to 5 cm/s
        elif key == MOVERIGHT:#This checks if the assined right movement key had been pressed
            self.left_right_velocity = S#This sets the right velocity to 5 cm/s
        elif key == UP:#This checks if the assined up movement key had been pressed
            self.up_down_velocity = S#This sets the up velocity to 5 cm/s
        elif key == DOWN:#This checks if the assined down movement key had been pressed
            self.up_down_velocity = -S#This sets the down velocity to 5 cm/s
        elif key == TURNLEFT:#This checks if the assined rotate left movement key had been pressed
            self.yaw_velocity = -S#This sets the rotate left velocity to 5 cm/s
        elif key == TURNRIGHT:#This checks if the assined rotate right movement key had been pressed
            self.yaw_velocity = S#This sets the rotate right velocity to 5 cm/s

    def keyup(self, key):#This detects if the keys have been released 
        if key == MOVEFORWARD or key == MOVEBACK:#This checks if the forward or backward movement key has been released
            self.for_back_velocity =#This sets the forward and backward velocity to 0 cm/s
        elif key == MOVELEFT or key == MOVERIGHT:#This checks if the left or right movement key has been released 
            self.left_right_velocity = 0#This sets the left and right velocity to 0 cm/s
        elif key == UP or key == DOWN:#This checks if the up or down movement key has been released
            self.up_down_velocity = 0#This sets the up and down velocity to 0 cm/s
        elif key == TURNLEFT or key == TURNRIGHT:#This checks if the rotate left or right movement key has been released
            self.yaw_velocity = 0#This sets the rotate left and right velocity to 0 cm/s
        elif key == pygame.K_t:#This checks if the takeoff key has been released it commands the Tello to take off
            self.tello.takeoff()#This commands the Tello to take off
            self.send_rc_control = True#This turns on rc control to allow for keyboard inputs
        elif key == pygame.K_l:#This checks if the landing key has been released
            not self.tello.land()#This commands the Tello to land
            self.send_rc_control = False#This sets the rc conttol to flase turing it off

    def update(self):#This is calling the function whenever the userevent timer is triggered
        if self.send_rc_control:#This checks for if rc control is active
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)#If rc control is active it sends the movement commands

def main():#This runs at the begining of the program
    frontend = FrontEnd()#This intiolizes the fron end object
    frontend.run()#This enters the run loop


if __name__ == '__main__':#This runs at the start of the program
    main()#This is the main functions