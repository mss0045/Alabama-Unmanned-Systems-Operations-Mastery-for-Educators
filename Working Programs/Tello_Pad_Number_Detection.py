from djitellopy import Tello

tello = Tello()
tello.connect()
tello.set_mission_pad_detection_direction(2)

tello.enable_mission_pads()
pad = tello.get_mission_pad_id()
print("Battery Percintage:" + str(tello.get_battery()))

while True:
    print(str(tello.get_mission_pad_id()))

tello.end()