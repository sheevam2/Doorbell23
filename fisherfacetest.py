import numpy
import cv2
import os 

def haar_cascades(face_image): # face_image must be in quotes and end in jpg. ex. "prom_facedetect".jpg
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") #Created cascadeclassifier object
    img = face_image # Reads image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts to grayscale


    # ----- Multiscaling -----

    detected_faces = cascade.detectMultiScale(gray, 1.2, 6)

    for (top_xLeft,top_yLeft,w,h) in detected_faces:
        cv2.rectangle(img,(top_xLeft,top_yLeft),(top_xLeft+w,top_yLeft+h),(255,0,0),2) # Creates a random rectangle.
        #roi = rectangle[top_yLeft:top_yLeft+h ,top_xLeft:top_xLeft+w] # Slices image to only region of interest.

    #cv2.imshow("final_img", img) #Showcase the final image with rectangles around detected faces
    #cv2.imwrite("final_image.jpg", img) # saving the final image as prom_final.jpg

    if len(detected_faces) == 0:
        return None, None

    return gray[top_yLeft:top_yLeft+h ,top_xLeft:top_xLeft+w], detected_faces[0]

def create_training_data(folder_dataPath):
    person_dir = os.listdir(folder_dataPath)

    faces = []
    labels = []
    #print(person_dir)
    for person in person_dir:

        if not person.startswith("p"):
            continue

        person_label = int(person.replace("p",""))
        #print(person_label)
        person_dir_path = folder_dataPath + "/" + person

        person_images = os.listdir(person_dir_path)

        for person_image in person_images:
            if person_image.startswith("."):
                continue
            
            person_image_path = person_dir_path + "/" + person_image
        
            image = cv2.imread(person_image_path)

            face, rect = haar_cascades(image) 

            if face is not None:
                faces.append(face)
                labels.append(person_label)
    return faces, labels

people = ["Vineeth Chandrapu","error", "Tom Cruise", "error"]

print("Loading Data . . . ")
faces,labels = create_training_data("image_training")
print("Completed Loading Data")

#print total faces and labels
# print("# of faces: ", len(faces) + 1)
# print("# of labels: ", len(labels) + 1)

recognize_face = cv2.face.LBPHFaceRecognizer_create() # had to do the following command to get it to work: pip install opencv-contrib-python

recognize_face.train(faces, numpy.array(labels)) #[1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2]
print(numpy.array(labels))

def create_rectangle(image, rect):
    (x, y, w, h) = rect
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

def create_textbox(image, text, x, y):
    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def recognize(image_test):
    #make a copy of the image as we don't want to change original image
    image = image_test.copy()

    #detect face from the image
    face, rect = haar_cascades(image)
    #print(face)
    #face = cv2.equalizeHist(face1)
    #predict the image using our face recognizer 
    label = recognize_face.predict(face)[0]
    
    #print(recognize_face.predict(face))
    #get name of respective label returned by face recognizer
    label_text = people[label]
    
    #draw a rectangle around face detected
    create_rectangle(image, rect)
    #draw name of predicted person
    create_textbox(image, label_text, rect[0], rect[1]-5)
    
    return image

print("Recognition in Progress . . .")

test_img1 = cv2.imread("cruise_test.jpg")
test_img2 = cv2.imread("vineethtest.png")

#vineeth_img = cv2.imread("vineethtest.png")
img_final1 = recognize(test_img1)
img_final2 = recognize(test_img2)

print("Recognition Complete")

cv2.imwrite("fisherTestImg.jpg", img_final1)
cv2.imwrite("fisherTestImg2.jpg", img_final2) # saving the final image
