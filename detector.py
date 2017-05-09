import cv2
import MySQLdb
import smtplib

def getProfile(id):
    db = MySQLdb.connect(host="localhost", user="root", passwd="manish",
                         db="CMPE273")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cmd = "SELECT sjsu_id,name,email_id FROM student where sjsu_id = '" + id + "'"
    print cmd
    profile =None
    try:
        cursor.execute(cmd)
        numrows = cursor.fetchall()
        for row in numrows:
            profile=row
            print profile[0],profile[1],profile[2]
        db.close()
    except:
        print "Error: unable to fecth data"
    return profile

def sendAttendancerecord(toEmail,studentID,studentName):

    fromaddr = 'cmpe273.sjsuproject@gmail.com'
    # Create the message
    content = 'Student with Student ID %s and Name %s was present.' %(studentID,studentName)
    message = 'Subject: %s\n%s' % ("Attendance record for Class 273", content)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login("cmpe273.sjsuproject@gmail.com", "cmpe273@2017")
    server.set_debuglevel(True)  # show communication with the server
    try:
        server.sendmail('cmpe273.sjsuproject@gmail.com', toEmail,message )
    finally:
        server.quit()

# Load the classifier xml from open cv2
faceDetect = cv2.CascadeClassifier('/home/manish/PycharmProjects/CMPE-273-Team-Project/haarcascade_frontalface_alt.xml')
# Start the web CAM and capture the image
webCam = cv2.VideoCapture(0)
rec = cv2.face.createLBPHFaceRecognizer()
rec.load("/home/manish/PycharmProjects/CMPE-273-Team-Project/recognizer/trainingData.yml")
id =0
mailSent= False
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
                if(mailSent==False):
                    sendAttendancerecord('manish.pandey@sjsu.edu',profile[0],profile[1])
                    mailSent= True
    cv2.imshow("Face", img)
    if(cv2.waitKey(1) ==ord('q')):
        break
webCam.release()
cv2.destroyAllWindows()


