import cv2
import MySQLdb as mdb
import sys


# Load the classifier xml from open cv2
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

#Load the classifier xml for Eye
eyeDetect = cv2.CascadeClassifier('haarcascade_eye.xml')

# Start the web CAM and capture the image
webCam = cv2.VideoCapture(-1)


def insertOrUpdate(id, name, email_id,servername,username,password,DBName):

    # Connect to the database
    con = mdb.connect(servername, username,
                      password, DBName);

    # Query the database tables to check if the student already registered.
    cmd = "select sjsu_id from student WHERE sjsu_id = '" + id + "'"

    # Execute the select query

    cur = con.cursor()
    cur.execute(cmd)
    rows = cur.fetchall()
    #make blob object to save color image in DB
    #pick the color image from dataset

    print "dataset/studentId." + id + ".jpg"
    blob_value = open("dataset/studentId." + id + ".jpg","rb").read()

    # Variable to check if student is present
    isStudentPresent = 0
    for row in rows:
        """ If row is returned by the select query indicating that the student is already present in database then
        set the 'isStudentPresent variable to 1. """
        isStudentPresent = 1

    # If student record is already present in the database then ask the user if he wants to update the existing record.
    if(isStudentPresent==1):
        # Prompt the user to ask if he wants to update the existing record in the database.
        choice = raw_input("A student with SJSU ID - " + id + " is already present in the database. " \
                                                 "Do you want to update this record? (Y/N)").lower()
        if choice == "y":
            # If user wants to update the record then
            cmd= "UPDATE student SET name= %s ,image= %s , email_id = %s Where sjsu_id = %s "
            print cmd
            cur.execute(cmd,(name,blob_value,email_id,id))
        else:
            print "No Changes made to the existing record."
    else:
        # There is no record for the user in database hence insert new record in Student table.
        #cmd = "INSERT INTO student(sjsu_id,name,image,email_id) VALUES('" + id + "','" + name + "','" + blob_value + "','" + email_id + "')"
        cmd = "INSERT INTO student(sjsu_id,name,image,email_id) VALUES(%s,%s,%s,%s)"
        cur.execute(cmd,(id,name,blob_value,email_id))
    print cmd
    con.commit()

def saveImageFromCam(id, name, email_id):
    while True:
        #read Image
        ret, img = webCam.read()
    # Capture Image Window
        cv2.imshow("Face", img)

        if not ret:
            break
    # Convert color image to Gray Scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Draw rectangle around face
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    # Store the key pressed by user in variable
        k = cv2.waitKey(1)
    # if C key is pressed then capture and save the image
        if k == ord('c'):
        # Destroy the previously shown window
            cv2.destroyWindow("Face")

        # Loop over the coordinates
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
                # Draw a rectangle to display which portion of the face was saved.
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Save the image of the face
                cv2.imwrite("dataset/studentId." + id + ".jpg", roi_gray)

                eyes = eyeDetect.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                # Display text to user to confirm if the image is to be saved?
                cv2.putText(img,"Are you happy with this image?",(10, y+400),
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0))
                cv2.putText(img, "Press 'C' key again to save & quit.", (10, y+450),
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0))
            # Display the image to user
                cv2.imshow("Captured Face", img)
                cv2.waitKey(0)
            break
    try:
        insertOrUpdate(id, name, email_id,'localhost','root', 'manish','CMPE273')
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        webCam.release()

    cv2.destroyAllWindows()
id = str(int(str(raw_input("  Please Enter User SJSU ID  "))))
name = raw_input("  Please Enter your Full Name  ")
email_id = raw_input("  Please Enter your Email ")

saveImageFromCam(id,name,email_id)