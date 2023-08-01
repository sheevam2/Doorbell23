#All libraries to import
#Must install oprn-cv (cv2), numpy, adafruit_servokit, and paho-mqtt on raspberry pi
import paho.mqtt.client as mqtt
from time import *
from adafruit_servokit import ServoKit
import cv2
import numpy
import os
import sqlite3
import pickle
import json
import base64

# Servo Variables 
kit = ServoKit(channels=16) # allows for servo to be turned
servo_turned = False # status for the app to determine whether servo is turned or not. 

# Global variables
username = "A" # placeholder value for username in SQL database
ID = "A" # placeholder value for username in SQL database

#Function to prompt the popup for user info on the app
def define_credentials(client):
    global username, ID
    
    client.publish("test/app", "Please Enter User Information") # Tells user on app popup to enter username and ID.

 # Collects Face data by taking a series of pictures of the user.
def sql_face_data_collection(client):
    global username, ID

    capture = cv2.VideoCapture(0) # Turns camera on 
    capture.set(3, 640) #width
    capture.set(4, 480) #height

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml") #Uses the open-cv provided xml file for frontal face features to create a cascade object

    # Inserts username and ID into SQL database
    def changeDB(ID,Name,Photos):
        conn = sqlite3.connect("FaceBase.db") # Connects to database
        cursor = conn.execute("SELECT * FROM people WHERE PersonID = ?", (ID,)) # Selects every column in given personID
            
        isRecordExist = cursor.fetchone() # Checks if person is already in database.


        try:
            if(isRecordExist is not None): # If ID is already in the database, it updates it with a new name, photos and ID. 
                cmd="UPDATE people SET Name = ?,Photos = ? WHERE PersonID = ?"
                conn.execute(cmd, (str(Name), Photos, ID)) # Executes the changes to be commited later on.
            else: # If person is not already in  the database, this adds them to it. 
                cmd="INSERT INTO people(PersonID, Name, Photos) VALUES(?, ?, ?)"	 
                conn.execute(cmd, (ID, str(Name), Photos)) # Executes the changes to be commited later on.

            conn.commit() # Commits the changes to the database.
            print("UPDATED SUCCESFULLY") #Prints message if database is updated successfully
        except:
            print("ERROR") # Prints message if database has an error updating

        conn.close() # Closes the connection to the database
        
    # Updates the variables od id and name based on the nput from the user through the app popup        
    id=ID
    name=username

    # Debug statements
        #print(ID)
        #print(username)

    print("Please look at the camera. Capturing face samples...") # Print statement for raspberry pi console log
    client.publish("test/app","Please look at the camera. Capturing face samples...") # Sends a message to the app's message log so the user knows to look at the camera
    
    
    photos_list = [] # empty list that will contain all photos of the specific user
    
    count = 0  # Counter to determine how many images the data collection code takes.
    while(True):
        ret, image = capture.read()
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) #Vertical camera flip
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grayscale
        faces_detected = face_cascade.detectMultiScale(gray_img, 1.2, 5, minSize = (20,20)) #Recognizes faces and stores the faces in the list faces detected

        for (x,y,w,h) in faces_detected:
            cv2.rectangle(image,(x,y),(x+w, y+h),(255,0,0),2) # Puts a rectangle around the face of the user. 
            count += 1 # Image counter
            photos_list.append(gray_img[y:y+h,x:x+w]) # appends each photo to the list defined outside the while loop.
            cv2.imshow('image', image) #Opens a camera livestream window on the raspberry pi
        
        a = cv2.waitKey(100) & 0xff # Defines which key to press to exit cv2.
        if a == 27: # Press escape on raspberry pi to forcequit.
            break
        elif count >= 30: #Waits until 30 images are taken, then ends the data cillection process
            break


    serialized_photos = pickle.dumps(photos_list) # Converts the image list into a binary string (BLOB). 
    changeDB(id,name,serialized_photos) # Adds the id, name and binary string to the database.

    print("Samples taken and exiting program") #Print statement to signify end of program

    # Closes all windows
    capture.release()
    cv2.destroyAllWindows()

    connect_mqtt(1) # Reconnects to the MQTT broker and starts the face trainer.

# Trains the images taken in the face data collection function
def sql_face_trainer(client):

    recognize_face = cv2.face.LBPHFaceRecognizer_create() # Uses a LBPH approach to recognize faces.
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml") # Uses Haar cascades to help recognize faces. 

    client.publish("test/app", "Samples taken and exiting program") # Sends a message to the apps message log to signify the end of the data collection program
    print("Face training in progress. This may take a few seconds...") # Sends a message to the app when the Face training begins.
    client.publish("test/app","Face training in progress. This may take a few seconds...") # Sends a message to the app's message log to show that the face training begins

    
    all_photos = [] # Empty list that will contain ID values and photos of each person in a tuple within all_photos. 

    # Function to grab images
    def getImagesAndLabels(): 
        conn=sqlite3.connect("FaceBase.db") # Connects to database
        cmd="SELECT * FROM people" # Selects the table "people" in the database
        cursor=conn.execute(cmd)


        if cursor.fetchone() is None: # Checks if database is empty
            print("No rows found in the database.") # prints message if it is empty
            cursor.close() # Closes out of the column.
            conn.close() # Closes out of the database.
            return [],[] # returns empty values for the ID and photos. 
        
        cursor.execute("SELECT PersonID, Photos FROM people") # Selects the columns "PersonId" and "Photos"


        rows = cursor.fetchall() # Fetches all the data from cursor column.

        face_samples = [] # Empty list of photos of each person/
        face_ids = [] # Empty list of ids of each person. 
        
        # For each person in the database
        for row in rows: 
            photo_value = row[1]  # Stores the BLOB version of the photos list into photo_value
            id_value = row[0] # Stores the ID into id_value.
            photos_list = pickle.loads(photo_value) # Converts BLOB version of photos beck to a list of images. 
            id_and_photos = [] # Creates empty list which contain both the photos list and the id value
            id_and_photos.append(photos_list) # Appends real images to id_and_photos. 
            id_and_photos.append(id_value) # Appends ids to id_and_photos. 
            all_photos.append(id_and_photos) # Appends the entire list containing both the id and photos to all_photos

        # For each element containin both the id and photos list in the all_photos list
        for photos in all_photos:
            # For each photo in the specific photos list in the element
            for photo in photos[0]: 
                numpy_image = numpy.array(photo, 'uint8') # Converts each image in the all_photos list into numpy array format

                faces_detected = face_cascade.detectMultiScale(numpy_image) # If detects a face, it is added to face_detected.
                for (x,y,w,h) in faces_detected: # Checks each face within faces_detected.
                    face_samples.append(numpy_image[y:y+h,x:x+w]) # Appends the image of the face detected to face_samples.
                    face_ids.append(photos[1]) # Appends the person's id to face_ids. 

        # Closes the connection in the database
        cursor.close()
        conn.close()
        
        return face_samples, face_ids # Returns the list of face samples and correspondinf face id's

    faces, ids = getImagesAndLabels() # Calls the function getImagesAndLabels to get the faces samples and face id's

    # Trains all the faces samples to their correct id's and then writes it to a yml file
    recognize_face.train(faces, numpy.array(ids)) 
    recognize_face.write('trainer_sql/trainer_sql.yml')


    print("\n [INFO] {0} Faces Trained. Program Exiting".format(len(numpy.unique(ids)))) # Prints how many faces have been trained on raspberry pi.
    client.publish("test/app", "[INFO] {0} Faces Trained. Program Exiting".format(len(numpy.unique(ids)))) # Prints how many faces have been trained on the app.
    connect_mqtt(0) # Reconnects to MQTT Broker

def sql_face_recognizer(client): # Recognizes the faces, and if it recognizes a users face it will turn the servo a certain distance. 

    global servo_turned # Declares that the servo is not turned.

    current_angle = kit.servo[8].angle # Checks the angle of the servo. 

    client.publish("test/app", "Facial Recognition Started") # Prints that facial recognition has been started  in the app's message log. 

    recognize_face = cv2.face.LBPHFaceRecognizer_create() # Uses the LBPH method to recognize faces. 
    recognize_face.read('trainer_sql/trainer_sql.yml') # Reads the face data from the yml file written earlier. 
    cascade_filepath = "haarcascade_frontalface_default1.xml" # Makes cascade_filepath a cascade object. 


    face_cascade = cv2.CascadeClassifier(cascade_filepath) # Uses the earlier haar cascade object to detect faces. 
    font = cv2.FONT_HERSHEY_SIMPLEX # Sets font.

    id = 0 # Placeholder id value. 

    capture = cv2.VideoCapture(0) # Starts video capture.
    capture.set(3, 640) #width
    capture.set(4, 480) #height

    # Getting minimum width and height to use as a parameter in the detectMultiScale function
    min_w = 0.1*capture.get(3)
    min_h = 0.1*capture.get(4)

    # Connects to the database
    conn = sqlite3.connect("FaceBase.db") 
    cursor = conn.cursor()
    
    # Gets the corresponding person's name from the id number
    def get_name_by_id(person_id): 
        # Selects the name column from the row containing the given person id
        cmd = "SELECT Name FROM people WHERE PersonID = ?"
        cursor.execute(cmd, (person_id,)) 
        row = cursor.fetchone()

        # If a person found, return the name, if not return "Unknown"
        if row is not None:
            return row[0]
        return "Unknown"
    
    start_time = time() # Start time to help determine how long the livestream facial recognizer in the app runs for.
    elapsed_time = 0 # Elapsed time to help determine how long the livestream facial recognizer in the app runs for.
    timeout = 15 # How long before the app stops livestreaming the face recognizer. 

    while (elapsed_time < timeout): # Runs until it reaches the desired number of seconds before stopping
        ret, image = capture.read()
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE) # Rotates the video camera



        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Converts the image to grayscale
        faces_detected = face_cascade.detectMultiScale(gray_img, 1.2, 5, minSize = (int(min_w),int(min_h))) # Detects faces from the camera and stores it in faces detected

        
        #For every face in the faces_detected list
        for (x,y,w,h) in faces_detected:
            cv2.rectangle(image,(x,y),(x+w, y+h),(0,255,0),2) # Creates a rectangle around the face
            id, confidence_lvl = recognize_face.predict(gray_img[y:y+h,x:x+w]) #Uses the open-cv predict function to get the corresponding id number from the face and the confidence level

            #If the confidence level is above the 30 then it recognizes the face
            if confidence_lvl < 70:
                name_ = get_name_by_id(id) # takes the id of the user
                confidence_lvl = " {0}%".format(round(100-confidence_lvl)) # Inverts the confidence interval, because higher usually means worse but for users to understand we make it the opposite. 

                if not servo_turned: # If the servo hasn't been turned yet it will unlock the lock if the servo is closed, and lock it if the lock is unlocked. 
                    if (current_angle < 180): # checks if the servo angle is in the unlocked position.
                        kit.servo[8].angle = 180 # Changes the angle to locked
                        servo_turned = True
                    else:
                        kit.servo[8].angle = 0 # Changes the angle to  unlocked.
                        servo_turned = True

            # Else the user is not recognized
            else: 
                name_ = "unknown" # Text "Unknown" is shown instead of the user's name
                confidence_lvl = " {0}%".format(round(100 - confidence_lvl)) # Inverts the confidence interval, because higher usually means worse but for users to understand we make it the opposite. 
            
            #Both the users name and the confidence leve is displayed on the video livestream
            cv2.putText(image, str(name_), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(image, str(confidence_lvl), (x+5,y+h-5), font, 1, (255,255,255), 1)

        #Converts the video livestream as frames so that the video livestream could be sent to the app
        _, buffer = cv2.imencode('.jpg', image)
        frame_base64 = base64.b64encode(buffer)

        # Publish the frames as an MQTT message and send it to the app
        client.publish("test/video", payload=frame_base64, qos=0) 
        sleep(0.1)

        # Opens a video livestream window on the raspberry pi
        cv2.imshow('camera', image)
        a = cv2.waitKey(10) & 0xff
        if a == 27: # Press escape to Force Quit
            break
        
        elapsed_time = time() - start_time # The Program will exit the while loop and end once the desired number of seconds (set before) is reached

    print("Exiting Program") # Prints exiting program to raspberry pi console log
    client.publish("test/app", "Facial Recognition is finished!") #Sens a message to the app's message log indicating the program to recognize faces is complete
    
    # Closes the connection to the database
    cursor.close()
    conn.close()

    # Closes all windows
    capture.release()
    cv2.destroyAllWindows()

    connect_mqtt(0) # Reconnects to MQTT Broker

# Connects to MQTT Broker and runs certain programs based on an input number 
def connect_mqtt(num):
    global servo_turned # Defines variable as global

    client = mqtt.Client(transport="websockets") # Sets the client to make sure that we are connecting to the MQTT broker through WebSockets
    client.on_connect = on_connect # Runs the on_connect function once connected to a MQTT Broker
    client.on_message = on_message # Runs the on_message function once a message is received from the app

    global servo_turned

    #MQTT Broker is run on the raspberry pi using mosquitto
    broker_address = "192.168.1.220" # IP address from raspberry pi
    broker_port = 1884 #Listening port

    # Set the MQTT broker's WebSocket URI
    websocket_uri = f"ws://{broker_address}:{broker_port}/mqtt"

    # Connect to the MQTT broker over WebSockets
    client.ws_set_options(path="/mqtt")  # Set the WebSocket path
    client.connect(broker_address, broker_port, 60) #Connects to the MQTT Broker

    angle = kit.servo[8].angle # Obtains the current angle of the servo motor

    # Sends the lock status of the lock (whether its currently locked or unlocked) to the app 
    if angle < 180:
        client.publish("test/status", "Unlocked")
        print("Unlocked")
    elif angle >= 180:
        client.publish("test/status", "Locked")
        print("Locked")

    # Runs certain programs depedning on the input number given
    if (num == 1):
        sql_face_trainer(client)
    if (num == 2):
        servo_turned = False
        sql_face_recognizer(client)
    if (num == 3):
        sql_face_data_collection(client)
    if (num == 4):
        define_credentials(client)

    # Makes ure the function runs forever so that there is enough time to establish a connection to the MQTT Broker   
    client.loop_forever()

# Function runs when MQTT broker connects
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc)) #Debug Statement

    #Subscribes to topics for message communication to and from the app
    client.subscribe("test/servo")
    client.subscribe("test/app")
    client.subscribe("test/popup")
    client.subscribe("test/video")
    client.subscribe("test/status")

# Function runs when a message is received from the app
def on_message(client, userdata, msg):
    global username, ID # Defins variable in global scope

    print(msg.topic + " " + str(msg.payload)) #Debug statement
    # Perform desired action based on the received message
    topic = msg.topic # Saves the topic from the received message

    # If topic is "test/popup", we take the message and decode it from json format
    if (topic == "test/popup"):
        payload = msg.payload.decode("utf-8") # Decodes message
        try:
            # Loads messag eand sets the username and ID variables based on the message which is the user's info from a popup
            data = json.loads(payload) 
            username = data.get("username")
            ID = data.get("inputNumber")
            print("Received username:", username) # Debug Statement 
            print("Received ID:", ID) # Debug Statement
        except json.JSONDecodeError:
            print("Error decoding JSON data") # Prints an error statement is message could not be decoded

    # If the message received is "This is lock" then the lock becomes locked
    if msg.payload.decode() == 'This is lock':
        # Trigger the lock action on the Raspberry Pi
        print("Lock action triggered")
        kit.servo[8].angle = 180 # Turns the servo
        connect_mqtt(0) # Reconnects to the MQTT Broker

    # If the message received is "This is unlock" then the lock becomes unlocked
    elif msg.payload.decode() == 'This is unlock':
        # Trigger the unlock action on the Raspberry Pi
        print("Unlock action triggered")
        kit.servo[8].angle = 0 # Turns the servo
        connect_mqtt(0) # Reconnects to the MQTT boker

    # If the message received is "This is Facial Recognition" then the facial recognition program runs
    elif msg.payload.decode() == 'This is Facial Recognition':
        connect_mqtt(2) # Reconnects to the MQTT Broker and runs the face recognizer program
   
    # If the message received is "This is New Face" then the face data collection and face trainer programs run
    elif msg.payload.decode() == 'This is New Face':
        connect_mqtt(4)  # Reconnects to the MQTT Broker and runs the face data collection and face trainer program

    # If the message received is "This is connected" then the connection to the MQTT Broker is re-established
    elif msg.payload.decode() == "This is connected":
        print ("Connecting to MQTT")
        connect_mqtt(0) # Reconnects to the MQTT Broker 

    # If the message received is "This is Start Data Cllection" then define credentials program is run
    elif msg.payload.decode() == "Start Data Collection":
        print("Info Submitted")
        connect_mqtt(3)  # Reconnects to the MQTT Broker and runs the define credentials program


connect_mqtt(0) #Connects to MQTT Broker

