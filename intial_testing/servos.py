

from time import *
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[8].angle = 0

while True:
    sleep(3)
    kit.servo[8].angle = 180
    sleep(3) 
    kit.servo[8].angle = 0
    

