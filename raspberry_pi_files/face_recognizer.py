import cv2
import numpy
import os
from time import *
from adafruit_servokit import ServoKit

recognize_face = cv2.face.LBPHFaceRecognizer_create()
recognize_face.read('trainer/trainer.yml')
cascade_filepath = "haarcascade_frontalface_default1.xml"

kit = ServoKit(channels=16)
kit.servo[8].angle = 0

face_cascade = cv2.CascadeClassifier(cascade_filepath)
font = cv2.FONT_HERSHEY_SIMPLEX

id = 0

name_list = ['None', 'Raahul Rajah', 'Josh Mekala', 'Vineeth Chandrapoo']

capture = cv2.VideoCapture(0)
capture.set(3, 640) #width
capture.set(4, 480) #height

min_w = 0.1*capture.get(3)
min_h = 0.1*capture.get(4)

while (True):
    ret, image = capture.read()
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) #Vertical camera flip
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grayscale
    faces_detected = face_cascade.detectMultiScale(gray_img, 1.2, 5, minSize = (int(min_w),int(min_h)))

    

    for (x,y,w,h) in faces_detected:
        cv2.rectangle(image,(x,y),(x+w, y+h),(0,255,0),2)
        id, confidence_lvl = recognize_face.predict(gray_img[y:y+h,x:x+w])

        if confidence_lvl < 70:
            id = name_list[id]
            confidence_lvl = " {0}%".format(round(100-confidence_lvl))
            kit.servo[8].angle = 180
        else: 
            id = "unknown"
            confidence_lvl = " {0}%".format(round(100 - confidence_lvl))
            kit.servo[8].angle = 0

        cv2.putText(image, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(image, str(confidence_lvl), (x+5,y+h-5), font, 1, (255,255,255), 1)
        #kit.servo[8].angle = 0

    cv2.imshow('camera', image)
    a = cv2.waitKey(10) & 0xff
    if a == 27: #Press escape to quit
        break

print("Exiting Program")

capture.release()
cv2.destroyAllWindows()
