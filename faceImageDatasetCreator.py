import cv2
import numpy as np
import sqlite3
# Load the classifier xml from open cv2

faceDetect = cv2.CascadeClassifier('/home/manish/PycharmProjects/ImageSearch/haarcascade_frontalface_default.xml')
# Start the web CAM and capture the image
webCam = cv2.VideoCapture(0)

def insertOrUpdate(id,name,gender):
    conn =sqlite3.connect("CMPE273DB")
    cmd = "SELECT Student_id FROM Student WHERE STUDENT_ID =" + str(id)
    cursor = conn.execute(cmd)
    isStudentPresent = 0
    for row in cursor:
        isStudentPresent = 1
    if(isStudentPresent==1):
        print str(name)
        cmd= "UPDATE Student SET Student_Name= '" +str(name)+ "' , Gender = '"+str(gender)+"' Where Student_id = '"+str(id)+"'"
        print cmd
    else:
        print str(name)
        cmd = "INSERT INTO Student(Student_ID,Student_Name,Gender) VALUES('"+str(id)+"','"+str(name)+"','"+str(gender)+ "')"
        print cmd
    conn.execute(cmd)
    conn.commit()
    conn.close()

id = raw_input("  Please Enter User SJSU ID  ")
name = raw_input("  Please Enter your Full Name  ")
gender = raw_input("  Please Enter your Gender ")
insertOrUpdate(id,name,gender)
sampleNum = 0
while(True):
    # Read image
    ret, img = webCam.read()

    # Convert color image to Gray Scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Draw rectangle around face
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in faces:
        sampleNum = sampleNum + 1
        cv2.imwrite("dataset/User." + str(id) + "." +
                    str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.waitKey(100)
    cv2.imshow("Face", img)

    cv2.waitKey(1)
    if(sampleNum > 10):
        break
webCam.release()
cv2.destroyAllWindows()
