import paho.mqtt.client as mqtt
from time import *
from adafruit_servokit import ServoKit
import cv2
import numpy
import os
import sqlite3
import pickle
import threading
import concurrent.futures
import json
import base64

kit = ServoKit(channels=16)


servo_turned = False

username = "A"
ID = "A"

def define_credentials(client):
    global username, ID

    client.publish("test/app", "Please Enter User Information")

def sql_face_data_collection(client):
    global username, ID


    capture = cv2.VideoCapture(0)
    capture.set(3, 640) #width
    capture.set(4, 480) #height

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml")



    def changeDB(ID,Name,Photos):
        conn = sqlite3.connect("FaceBase.db")
        cursor = conn.execute("SELECT * FROM people WHERE PersonID = ?", (ID,))
            
        isRecordExist = cursor.fetchone()


        try:
            if(isRecordExist is not None):
                cmd="UPDATE people SET Name = ?,Photos = ? WHERE PersonID = ?"
                conn.execute(cmd, (str(Name), Photos, ID))
            else:
                cmd="INSERT INTO people(PersonID, Name, Photos) VALUES(?, ?, ?)"	 
                conn.execute(cmd, (ID, str(Name), Photos))

            conn.commit()
            print("UPDATED SUCCESFULLY")
        except:
            print("ERROR")

        conn.close()
            
    id=ID
    name=username

    print(ID)
    print(username)



    print("Please look at the camera. Capturing face samples...")
    client.publish("test/app","Please look at the camera. Capturing face samples...")
    
    photos_list = []


    count = 0
    while(True):
        ret, image = capture.read()
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) #Vertical camera flip
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grayscale
        faces_detected = face_cascade.detectMultiScale(gray_img, 1.2, 5, minSize = (20,20))

        for (x,y,w,h) in faces_detected:
            cv2.rectangle(image,(x,y),(x+w, y+h),(255,0,0),2)
            count += 1
            photos_list.append(gray_img[y:y+h,x:x+w])
            cv2.imshow('image', image)
        
        a = cv2.waitKey(100) & 0xff
        if a == 27: #Press escape to quit
            break
        elif count >= 5:
            break


    serialized_photos = pickle.dumps(photos_list)
    changeDB(id,name,serialized_photos)

    print("Samples taken and exiting program")
    capture.release()
    cv2.destroyAllWindows()
    connect_mqtt(1)

def sql_face_trainer(client):

    recognize_face = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml")

    client.publish("test/app", "Samples taken and exiting program")
    print("Face training in progress. This may take a few seconds...")
    client.publish("test/app","Face training in progress. This may take a few seconds...")
    client.publish("test/app", "TESTTT")
    
    all_photos = []

    def getImagesAndLabels(): 
        conn=sqlite3.connect("FaceBase.db")
        cmd="SELECT * FROM people"
        cursor=conn.execute(cmd)


        if cursor.fetchone() is None:
            print("No rows found in the database.")
            cursor.close()
            conn.close()
            return [],[]
        
        cursor.execute("SELECT PersonID, Photos FROM people")


        rows = cursor.fetchall()

        face_samples = []
        face_ids = []

        for row in rows:
            photo_value = row[1]  # Assuming the column is the first (index 0)
            id_value = row[0]
            photos_list = pickle.loads(photo_value)
            id_and_photos = []
            id_and_photos.append(photos_list)
            id_and_photos.append(id_value)
            all_photos.append(id_and_photos)
        for photos in all_photos:
            for photo in photos[0]:
                numpy_image = numpy.array(photo, 'uint8')

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
    client.publish("test/app", "[INFO] {0} Faces Trained. Program Exiting".format(len(numpy.unique(ids))))
    connect_mqtt(0)

def sql_face_recognizer(client):

    global servo_turned

    current_angle = kit.servo[8].angle

    client.publish("test/app", "Facial Recognition Started")

    recognize_face = cv2.face.LBPHFaceRecognizer_create()
    recognize_face.read('trainer_sql/trainer_sql.yml')
    cascade_filepath = "haarcascade_frontalface_default1.xml"


    face_cascade = cv2.CascadeClassifier(cascade_filepath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    id = 0

    capture = cv2.VideoCapture(0)
    capture.set(3, 640) #width
    capture.set(4, 480) #height

    min_w = 0.1*capture.get(3)
    min_h = 0.1*capture.get(4)

    conn = sqlite3.connect("FaceBase.db")
    cursor = conn.cursor()

    def get_name_by_id(person_id):
        cmd = "SELECT Name FROM people WHERE PersonID = ?"
        cursor.execute(cmd, (person_id,))
        row = cursor.fetchone()
        if row is not None:
            return row[0]
        return "Unknown"
    
    start_time = time()
    elapsed_time = 0
    timeout = 15

    while (elapsed_time < timeout):
        ret, image = capture.read()
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) #Vertical camera flip



        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grayscale
        faces_detected = face_cascade.detectMultiScale(gray_img, 1.2, 5, minSize = (int(min_w),int(min_h)))

        

        for (x,y,w,h) in faces_detected:
            cv2.rectangle(image,(x,y),(x+w, y+h),(0,255,0),2)
            id, confidence_lvl = recognize_face.predict(gray_img[y:y+h,x:x+w])

            if confidence_lvl < 70:
                name_ = get_name_by_id(id)
                confidence_lvl = " {0}%".format(round(100-confidence_lvl))
                #kit.servo[8].angle = 180

                if not servo_turned:
                    if (current_angle < 180):
                        kit.servo[8].angle = 180
                        servo_turned = True
                    else:
                        kit.servo[8].angle = 0
                        servo_turned = True
            else: 
                name_ = "unknown"
                confidence_lvl = " {0}%".format(round(100 - confidence_lvl))

            cv2.putText(image, str(name_), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(image, str(confidence_lvl), (x+5,y+h-5), font, 1, (255,255,255), 1)

        _, buffer = cv2.imencode('.jpg', image)
        frame_base64 = base64.b64encode(buffer)

        # Publish the fsrame as an MQTT message
        client.publish("test/video", payload=frame_base64, qos=0)
        sleep(0.1)

        cv2.imshow('camera', image)
        a = cv2.waitKey(10) & 0xff
        if a == 27: #Press escape to quit
            break
        
        elapsed_time = time() - start_time

    print("Exiting Program")
    client.publish("test/app", "Facial Recognition is finished!")
    
    cursor.close()
    conn.close()

    capture.release()
    cv2.destroyAllWindows()
    connect_mqtt(0)


def connect_mqtt(num):
    global servo_turned
    
    client = mqtt.Client(transport="websockets")
    client.on_connect = on_connect
    client.on_message = on_message

    global servo_turned

    broker_address = "192.168.1.220"
    broker_port = 1884

    # Set the MQTT broker's WebSocket URI
    websocket_uri = f"ws://{broker_address}:{broker_port}/mqtt"

    # Connect to the MQTT broker over WebSocket
    client.ws_set_options(path="/mqtt")  # Set the WebSocket path
    client.connect(broker_address, broker_port, 60)

    angle = kit.servo[8].angle
    print(angle)
    if angle < 180:
        client.publish("test/status", "Unlocked")
        print("Unlocked")
    elif angle >= 180:
        client.publish("test/status", "Locked")
        print("Locked")

    if (num == 1):
        sql_face_trainer(client)
    if (num == 2):
        servo_turned = False
        sql_face_recognizer(client)
    if (num == 3):
        sql_face_data_collection(client)
    if (num == 4):
        define_credentials(client)

        
    client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe("test/servo")
    client.subscribe("test/app")
    client.subscribe("test/popup")
    client.subscribe("test/video")
    client.subscribe("test/status")

def on_message(client, userdata, msg):
    global username, ID

    print(msg.topic + " " + str(msg.payload))
    # Perform desired action based on the received message
    topic = msg.topic
    if (topic == "test/popup"):
        payload = msg.payload.decode("utf-8")
        try:
            data = json.loads(payload)
            username = data.get("username")
            ID = data.get("inputNumber")
            print("Received username:", username)
            print("Received ID:", ID)
        except json.JSONDecodeError:
            print("Error decoding JSON data")
    if msg.payload.decode() == 'This is lock':
        # Trigger the lock action on the Raspberry Pi
        print("Lock action triggered")
        kit.servo[8].angle = 180
        connect_mqtt(0)
    elif msg.payload.decode() == 'This is unlock':
        # Trigger the unlock action on the Raspberry Pi
        print("Unlock action triggered")
        kit.servo[8].angle = 0
        connect_mqtt(0)

    elif msg.payload.decode() == 'This is Facial Recognition':
        connect_mqtt(2)
   
    elif msg.payload.decode() == 'This is New Face':
        connect_mqtt(4)

    elif msg.payload.decode() == "This is connected":
        print ("Connecting to MQTT")
        connect_mqtt(0)
        
    elif msg.payload.decode() == "Start Data Collection":
        print("Info Submitted")
        connect_mqtt(3)


connect_mqtt(0)

