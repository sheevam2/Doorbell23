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
    image = cv2.flip(image, -1) #Vertical camera flip
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grayscale
    faces_detected = face_cascade.detectMultiScale(gray_img, 1.2, 5, minSize = (20,20))

    for (x,y,w,h) in faces_detected:
        cv2.rectangle(image,(x,y),(x+w, y+h),(255,0,0),2)
        count += 1

        cv2.imwrite("dataset/User." + str(id) + '.' + str(count) + ".jpg", gray_img[y:y+h,x:x+w])
        cv2.imshow('image', image)

    a = cv2.waitKey(100) & 0xff
    if a == 27: #Press escape to quit
        break
    elif count >= 30:
        break

print("Samples taken and exiting program")
capture.release()
cv2.destroyAllWindows()