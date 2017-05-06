import tkinter as tk
import tkinter.messagebox
import PIL.Image
import PIL.ImageTk
import os
import cv2
import sqlite3

LARGE_FONT = ("Times", 20)

sjsu_id = ""
name = ""
email_id = ""

# Baseline code for adding pages
class MyTKClass(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.title(self, "Face Recognizer")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand="True")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, RegistrationPage, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

def qf(param):
    print "I did it..."

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        img = PIL.Image.open("FR_Logo.png")
        logo_img = PIL.ImageTk.PhotoImage(img)
        logo = tk.Label(self, image=logo_img)
        logo.image = logo_img
        # logo.place(x=0, y=0, relwidth=1, relheight=1)
        logo.pack(side="left")
        label = tk.Label(self, text="Face Recognizer", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        register_usr_btn = tk.Button(self, text="Register",
                                     command=lambda: controller.show_frame(RegistrationPage))
        register_usr_btn.pack(side="right")

        verify_usr_btn = tk.Button(self, text="Verify",
                                     command=lambda: controller.show_frame(PageTwo))
        verify_usr_btn.pack(side="right")

def upload_image():
    os.system('python faceImageDatasetCreator.py')

class RegistrationPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        tk_name = tk.StringVar()
        tk_sjsu_id = tk.StringVar()
        tk_email_id = tk.StringVar()

        label = tk.Label(self, text="Create a new User", font=LARGE_FONT)

        """home_btn = tk.Button(self, text="Home",
                                     command=lambda: controller.show_frame(StartPage)) """

        name = tk.Label(self, text="Name:")
        name_entry = tk.Entry(self, textvariable = tk_name)

        sjsu_id = tk.Label(self, text="SJSU ID:")
        sjsu_id_entry = tk.Entry(self, textvariable = tk_sjsu_id)

        email_id = tk.Label(self, text="Email ID:")
        email_id_entry = tk.Entry(self, textvariable = tk_email_id)

        label.grid(row=0, columnspan=2)

        #home_btn.grid(row=1)

        name.grid(row=2, sticky="e")
        name_entry.grid(row=2,column=1)
        email_id.grid(row=3, sticky="e")
        email_id_entry.grid(row=3, column=1)
        sjsu_id.grid(row=4, sticky="e")
        sjsu_id_entry.grid(row=4, column=1)

        capture_btn = tk.Button(self, text="Capture Image",
                                     command=lambda: capture_image())
        capture_btn.grid(row=5,columnspan=2)

        or_msg = tk.Label(self, text="OR")
        or_msg.grid(row=6, columnspan=2)

        upload_img_btn = tk.Button(self, text="Upload Image",
                                   command=lambda: upload_image())
        upload_img_btn.grid(row=7, columnspan=2)

        def insertOrUpdate(name, sjsu_id, email_id):

            # Connect to the database
            conn = sqlite3.connect("CMPE273DB.DB")

            # Query the database tables to check if the student already registered.
            cmd = "SELECT sjsu_id FROM Student WHERE sjsu_id = '" + sjsu_id + "'"

            # Execute the select query
            cursor = conn.execute(cmd)

            # Variable to check if student is present
            isStudentPresent = 0

            for row in cursor:
                """ If row is returned by the select query indicating that the student is already present in database then
                set the 'isStudentPresent variable to 1. """
                isStudentPresent = 1

            # If student record is already present in the database then ask the user if he wants to update the existing record.
            if (isStudentPresent == 1):

                # Prompt the user to ask if he wants to update the existing record in the database.

                choice = tkinter.messagebox.askquestion("Warning!",
                                                        "A student with SJSU ID - " + sjsu_id + " is already present in the database. " \
                                                                                                "Do you want to update this record?")
                if choice == "yes":
                    # If user wants to update the record then
                    cmd = "UPDATE Student SET name = '" + name + "' , email_id = '" + email_id + \
                          "' Where sjsu_id = '" + sjsu_id + "'"

                    tkinter.messagebox.showinfo("Success", "User details were updated successfully!")

            else:
                # There is no record for the user in database hence insert new record in Student table.
                cmd = "INSERT INTO Student(sjsu_id,name, email_id) VALUES('" + sjsu_id + "','" + name + "','" + email_id + "')"

            conn.execute(cmd)
            conn.commit()
            conn.close()

        def capture_image():
            global sjsu_id
            sjsu_id = tk_sjsu_id.get()
            global name
            name = tk_name.get()
            global email_id
            email_id = tk_email_id.get()

            # Load the classifier xml from open cv2
            faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

            # Start the web CAM and capture the image
            webCam = cv2.VideoCapture(0)

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
                        cv2.imwrite("dataset/studentId." + sjsu_id + ".jpg", gray[y:y + h, x:x + w])

                        # Draw a rectangle to display which portion of the face was saved.
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                        # Display the image to user
                        cv2.imshow("Captured Face", img)
                        #cv2.waitKey(0)

                        # Display text to user to confirm if the image is to be saved?
                        choice = tkinter.messagebox.showinfo("Success", "This image has been captured successfully.")

                    break
            insertOrUpdate(name, sjsu_id, email_id)
            webCam.release()
            cv2.destroyAllWindows()

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Verify User", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        home_btn = tk.Button(self, text="Home",
                                     command=lambda: controller.show_frame(StartPage))
        home_btn.pack()

app = MyTKClass()
#app.resizable(width=False, height=False)
app.mainloop()