"""
This script uses keyboard inputs as movement commands allowing for manlue control of the drone using a laptop or computer.
By using keyboard inputs it allows for an infinite amount of movement commands to be sent to the drone making the program more condensed. 
"""
from djitellopy import Tello
import time
import cv2
import numpy as np
import pygame

# Speed of the drone
S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
FPS = 120

UP = pygame.K_SPACE
DOWN = pygame.K_c
TURNLEFT = pygame.K_q
TURNRIGHT = pygame.K_e
MOVELEFT = pygame.K_a
MOVERIGHT = pygame.K_d
MOVEFORWARD = pygame.K_w
MOVEBACK = pygame.K_s

class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - W: Forward, S: backward, A: left and D: right.
            - Q and E: Counter clockwise and clockwise rotations (yaw)
            - SPACE and C: Up and down.
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    def run(self):

        self.tello.connect()
        self.tello.set_speed(self.speed)
        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()

        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])

            frame = frame_read.frame
            # battery n.
            text = "Battery: {}%".format(self.tello.get_battery())
            cv2.putText(frame, text, (5, 720 - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)

            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            time.sleep(1 / FPS)

        # Call it always before finishing. To deallocate resources.
        self.tello.end()



    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
            key：pygame
        """
        if key == MOVEFORWARD:  # set forward velocity
            self.for_back_velocity = S
        elif key == MOVEBACK:  # set backward velocity
            self.for_back_velocity = -S
        elif key == MOVELEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == MOVERIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == UP:  # set up velocity
            self.up_down_velocity = S
        elif key == DOWN:  # set down velocity
            self.up_down_velocity = -S
        elif key == TURNLEFT:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == TURNRIGHT:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
            key：pygame
        """
        if key == MOVEFORWARD or key == MOVEBACK:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == MOVELEFT or key == MOVERIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == UP or key == DOWN:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == TURNLEFT or key == TURNRIGHT:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ 
        Update routine. Send velocities to Tello.
        """
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)


def main():
    frontend = FrontEnd()
    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()