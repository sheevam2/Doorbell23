import numpy
import cv2

capture = cv2.VideoCapture(0)
capture.set(3, 640) #width
capture.set(4, 480) #height

while(True):
    ret, frame = capture.read()
    frame = cv2.flip(frame, -1) #Vertical camera flip
    gray_vid = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #grayscale

    cv2.imshow('frame', frame)
    cv2.imshow('gray_vid', gray_vid)

    a = cv2.waitKey(30) & 0xff
    if a == 27: #Escape button to quit
        break

capture.release()
cv2.destroyAllWindows()

