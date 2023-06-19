import numpy
import cv2
import os

capture = cv2.VideoCapture(0)
capture.set(3, 640) #width
capture.set(4, 480) #height

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml")

id = input('Enter User ID: ')
print("Please look at the camera. Capturing face samples...")

count = 0

while(True):
    ret, image = capture.read()