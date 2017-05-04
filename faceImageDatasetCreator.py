import cv2
import sqlite3

# Load the classifier xml from open cv2
faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

# Start the web CAM and capture the image
webCam = cv2.VideoCapture(0)

def insertOrUpdate(id,name,gender):

    # Connect to the database
    conn =sqlite3.connect("CMPE273DB.DB")

    # Query the database tables to check if the student already registered.
    cmd = "SELECT Student_id FROM Student WHERE Student_id = '" + id + "'"

    # Execute the select query
    cursor = conn.execute(cmd)

    # Variable to check if student is present
    isStudentPresent = 0

    for row in cursor:
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
            cmd= "UPDATE Student SET Student_Name= '" + name + "' , Gender = '" + gender + \
                 "' Where Student_id = '" + id +"'"
        else:
            print "No Changes made to the existing record."
    else:
        # There is no record for the user in database hence insert new record in Student table.
        cmd = "INSERT INTO Student(Student_ID,Student_Name,Gender) VALUES('" + id + "','" + name + "','"+ gender + "')"

    conn.execute(cmd)
    conn.commit()
    conn.close()

id = str(raw_input("  Please Enter User SJSU ID  "))
name = raw_input("  Please Enter your Full Name  ")
gender = raw_input("  Please Enter your Gender ")

while True:

    # Read image
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

            # Save the image of the face
            cv2.imwrite("dataset/studentId." + id + ".jpg", gray[y:y + h, x:x + w])

            # Draw a rectangle to display which portion of the face was saved.
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display text to user to confirm if the image is to be saved?
            cv2.putText(img,"Are you happy with this image?",(10, y+400),
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0))
            cv2.putText(img, "Press 'C' key again to save & quit.", (10, y+450),
                        cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0))

            # Display the image to user
            cv2.imshow("Captured Face", img)
            cv2.waitKey(0)
        break

insertOrUpdate(id, name, gender)

webCam.release()

cv2.destroyAllWindows()
