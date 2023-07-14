import cv2
import numpy
import sqlite3
import pickle
from PIL import Image

recognize_face = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml")

print("Face training in progress. This may take a few seconds...")

all_photos = []

def getImagesAndLabels(): 
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM people"
    cursor=conn.execute(cmd)

    cursor.execute("SELECT PersonID, Photos, FROM people")

    rows = cursor.fetchall()

    face_samples = []
    face_ids = []

    for row in cursor.fetchall():
        photo_value = row[1]  # Assuming the column is the first (index 0)
        id_value = row[0]
        photos_list = pickle.loads(photo_value)
        id_and_photos = []
        id_and_photos.append(photos_list)
        id_and_photos.append(id_value)
        all_photos.append(id_and_photos)
    
    for photos in all_photos:
        for photo in photos[0]:
            PIL_image = Image.open(photo).convert("L")
            numpy_image = numpy.array(PIL_image, 'uint8')

            faces_detected = face_cascade.detectMultiScale(numpy_image)
            for (x,y,w,h) in faces_detected:
                face_samples.append(numpy_image[y:y+h,x:x+w])
                face_ids.append(photos[1])

    cursor.close()
    conn.close()
    
    return face_samples, face_ids

faces, ids = getImagesAndLabels()
recognize_face.train(faces, numpy.array(ids))

recognize_face.write('trainer_sql/trainer_sql.yml')


print("\n [INFO] {0} Faces Trained. Program Exiting".format(len(numpy.unique(ids))))