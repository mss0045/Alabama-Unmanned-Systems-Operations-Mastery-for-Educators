from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

tello.flip("f")
tello.flip("b")
tello.flip("r")
tello.flip("l")

tello.land()