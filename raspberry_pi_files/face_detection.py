import numpy
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml")
    
capture = cv2.VideoCapture(0)
capture.set(3, 640) #width
capture.set(4, 480) #height

while True:
    ret, image = capture.read()
    image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) #Vertical camera flip
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grayscale

    faces_detected = face_cascade.detectMultiScale(gray_img, 1.2, 5, minSize = (20,20))

    for (x,y,w,h) in faces_detected:
        cv2.rectangle(image,(x,y),(x+w, y+h),(255,0,0),2)
        gray_roi = gray_img[y:y+h, x:x+w]
        img_roi = image[y:y+h, x:x+w]

    cv2.imshow('video', image)
    a = cv2.waitKey(30) & 0xff
    if a == 27: #Press escape to quit
        break

capture.release()
cv2.destroyAllWindows()
