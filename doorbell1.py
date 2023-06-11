import numpy
import cv2

# ---- Vineeth Rizz Test ----

'''rizz_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #Created cascadeclassifier object
img = cv2.imread("vineethrizz.jpg") # Reads image
rizz_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts to grayscale


# ----- Multiscaling -----

detected_faces = rizz_cascade.detectMultiScale(rizz_gray, 1.3, 5)

for (top_xLeft,top_yLeft,w,h) in detected_faces:
    rectangle = cv2.rectangle(img,(top_xLeft,top_yLeft),(top_xLeft+w,top_yLeft+h),(255,0,0),2) # Creates a random rectangle.
    #roi = rectangle[top_yLeft:top_yLeft+h ,top_xLeft:top_xLeft+w] # Slices image to only region of interest.

cv2.imshow("final_img", img) #Showcase the final image with rectangles around detected faces
cv2.imwrite("rizz.jpg", img) # saving the final image as rizz.jpg
#cv2.waitKey(0)
#cv2.destroyAllWindows()'''

# ---- Prom multiple face test ----


prom_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #Created cascadeclassifier object
img = cv2.imread("prom_facedetect.jpg") # Reads image
prom_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts to grayscale


# ----- Multiscaling -----

detected_faces = prom_cascade.detectMultiScale(prom_gray, 1.2, 6)

for (top_xLeft,top_yLeft,w,h) in detected_faces:
    rectangle = cv2.rectangle(img,(top_xLeft,top_yLeft),(top_xLeft+w,top_yLeft+h),(255,0,0),2) # Creates a random rectangle.
    #roi = rectangle[top_yLeft:top_yLeft+h ,top_xLeft:top_xLeft+w] # Slices image to only region of interest.

cv2.imshow("final_img", img) #Showcase the final image with rectangles around detected faces
cv2.imwrite("prom_final.jpg", img) # saving the final image as prom_final.jpg


# a = numpy.array([1, 2, 3]) #testing accessing numpy
# img = cv2.imread("vineethrizz.jpg") #testing accessing cv2

