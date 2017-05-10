import cv2
import MySQLdb
import smtplib
from twilio.rest import Client


mailSentList = {}

def getProfile(id):
    db = MySQLdb.connect(host="localhost", user="root", passwd="manish",
                         db="CMPE273")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cmd = "SELECT sjsu_id,name,email_id FROM student where sjsu_id = '" + id + "'"
    profile =None
    try:
        cursor.execute(cmd)
        numrows = cursor.fetchall()
        for row in numrows:
            profile=row
        db.close()
    except:
        print "Error: unable to fecth data"
    return profile

def sendAttendancerecord(toEmail,students):
    studentList='';
    for key in students:
        studentList = studentList+"     " + str(key)
    fromaddr = 'cmpe273.sjsuproject@gmail.com'
    # Create the message
    content = 'Student with Student ID %s are present.' %studentList
    message = 'Subject: %s\n%s' % ("Attendance record for Class 273", content)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login("cmpe273.sjsuproject@gmail.com", "cmpe273@2017")
    #server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail('cmpe273.sjsuproject@gmail.com', toEmail,message )
        #client = Client("ACa849a726136e5f820facb11184d9d0de", "43ef7096906dfa3d94126afea4c013b3")
        #body = content
        #client.messages.create(to="+16692121549",from_="+13343848263",body = content)
    finally:
        server.quit()


# Load the classifier xml from open cv2
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# Start the web CAM and capture the image
webCam = cv2.VideoCapture(-1)
rec = cv2.face.createLBPHFaceRecognizer()
rec.load("recognizer/trainingData.yml")
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
            profile = getProfile(str(id))
            if(profile!="None"):
                cv2.putText(img, "% Match: "+str(100 - conf), (x -30, y + h), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                cv2.putText(img, str(profile[1]), (x, y + h+30), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                cv2.putText(img, str(profile[2]), (x, y + h+60), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
                if(id in mailSentList):
                    if(mailSentList[id]==
                           'false'):
                        mailSentList[id]='true'
                        break
                else:
                    mailSentList[id]='false'
                    break

    cv2.imshow("Face", img)
    if(cv2.waitKey(1) ==ord('q')):
        webCam.release()
        cv2.destroyAllWindows()
        sendAttendancerecord('manish.pandey@sjsu.edu', mailSentList)
        break

webCam.release()
cv2.destroyAllWindows()

