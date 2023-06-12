import numpy
import cv2
import os 

def haar_cascades(face_image): # face_image must be in quotes and end in jpg. ex. "prom_facedetect".jpg
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #Created cascadeclassifier object
    img = cv2.imread(f'"{face_image}"') # Reads image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts to grayscale


    # ----- Multiscaling -----

    detected_faces = cascade.detectMultiScale(gray, 1.2, 6)

    for (top_xLeft,top_yLeft,w,h) in detected_faces:
        cv2.rectangle(img,(top_xLeft,top_yLeft),(top_xLeft+w,top_yLeft+h),(255,0,0),2) # Creates a random rectangle.
        #roi = rectangle[top_yLeft:top_yLeft+h ,top_xLeft:top_xLeft+w] # Slices image to only region of interest.

    #cv2.imshow("final_img", img) #Showcase the final image with rectangles around detected faces
    cv2.imwrite("final_image.jpg", img) # saving the final image as prom_final.jpg

    return img


def create_training_data(folder_dataPath):
    person_dir = os.listdir(folder_dataPath)

    faces = []
    labels = []

    for person in person_dir:
        person_label = int(person_dir.replace("p",""))
        person_dir_path = folder_dataPath + "/" + person_dir

        person_images = os.listdir(person_dir_path)

        for person_image in person_images:
            person_image_path = person_dir_path + "/" + person_image
        
            image = cv2.imread(person_image_path)

            face, rect = haar_cascades(person_image_path)