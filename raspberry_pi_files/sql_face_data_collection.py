import cv2
import sqlite3
import pickle

capture = cv2.VideoCapture(0)
capture.set(3, 640) #width
capture.set(4, 480) #height

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default1.xml")

id = input('Enter User ID: ')


def changeDB(ID,Name,Photos):
	conn=sqlite3.connect("FaceBase.db")
	cmd="SELECT * FROM people"
	cursor=conn.execute(cmd)
        
	isRecordExist=0
	for row in cursor:
		isRecordExist=1

	if(isRecordExist==1):
		cmd="UPDATE people SET Name= "+str(Name)+","+Photos+" WHERE PersonID = "+str(ID)
	else:
		cmd="INSERT INTO people(PersonID,Name,Photos) Values("+str(ID)+","+str(Name)+","+Photos+")"	 
                
	conn.execute(cmd)  
	conn.commit()
	conn.close()
        
id=input('Enter user id : ')
name=input('Enter your name : ')

sampleNum=0 

print("Please look at the camera. Capturing face samples...")
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
        #cv2.imwrite("dataset/User." + str(id) + '.' + str(count) + ".jpg", gray_img[y:y+h,x:x+w])
        cv2.imshow('image', image)
    
    a = cv2.waitKey(100) & 0xff
    if a == 27: #Press escape to quit
        break
    elif count >= 30:
        break


serialized_photos = pickle.dumps(photos_list)
changeDB(id,name,serialized_photos)

print("Samples taken and exiting program")
capture.release()
cv2.destroyAllWindows()