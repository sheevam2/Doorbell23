import cv2
import numpy
from PIL import Image
import os
# Path for face image databse

path = 'dataset'
recognize_face = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml")

#function for images and labels

def getImagesAndLabels(path):
    image_filepaths = [os.path.join(path,f) for f in os.listdir(path)]
    face_samples = []
    face_ids = []
    for image_filepath in image_filepaths:
        PIL_image = Image.open(image_filepath).convert('L') #grayscale conversion
        numpy_image = numpy.array(PIL_image, 'uint8')
        id = int(os.path.split(image_filepath)[-1].split(".")[1])
        faces_detected = face_cascade.detectMultiScale(numpy_image)

        for (x,y,w,h) in faces_detected:
            face_samples.append(numpy_image[y:y+h,x:x+w])
            face_ids.append(id)
    return face_samples, face_ids

print("Face training in progress. This may take a few seconds...")

faces, ids = getImagesAndLabels(path)
recognize_face.train(faces, numpy.array(ids))

recognize_face.write('trainer/trainer.yml')

print("\n [INFO] {0} Faces Trained. Program Exiting".format(len(numpy.unique(ids))))