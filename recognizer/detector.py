import cv2
import numpy as np
import sqlite3


def getProfile(id):
    conn =sqlite3.connect("CMPE273DB")
    cmd = "SELECT * from Student where STUDENT_ID =" + str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile
# Load the classifier xml from open cv2
faceDetect = cv2.CascadeClassifier('/home/manish/PycharmProjects/ImageSearch/haarcascade_frontalface_default.xml')
# Start the web CAM and capture the image
webCam = cv2.VideoCapture(0)
rec = cv2.face.createLBPHFaceRecognizer()
rec.load("/home/manish/PycharmProjects/ImageSearch/recognizer/trainingData.yml")
id =0

while(True):
    # Read image
    ret, img = webCam.read()
    # Convert color image to Gray Scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Draw rectabgke around face
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id,conf = rec.predict(gray[y:y+h,x:x+w])
        if (conf > 50):
            id = "Unknown"
        if(id=="Unknown"):
            cv2.putText(img, "% Match: " + str(100 - conf), (x - 30, y + h), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
            cv2.putText(img, str(id), (x, y + h+30), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)

        else:
            profile = getProfile(id)
            if(profile!="None"):
                cv2.putText(img, "% Match: "+str(100 - conf), (x -30, y + h), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                cv2.putText(img, str(profile[1]), (x, y + h+30), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                cv2.putText(img, str(profile[2]), (x, y + h+60), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
    cv2.imshow("Face", img)
    if(cv2.waitKey(1) ==ord('q')):
        break
webCam.release()
cv2.destroyAllWindows()
