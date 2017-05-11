# CMPE-273-Team-Project
Team Project: Project 1- Image recognition

Abstract

Checking a person against his or her picture ID is labor intensive. Despite machine learning is getting better and better, we want to use image recognition as much as possible and handle in-person check whenever the algorithm doesn't decide.

Requirements

implements the photo ID scan upload and saving it to a database.
implements the live image upload from a camera or mobile phone.
calculate the matching score for the live image photo against the original stored in the database.

Pre requisites:

Python 2.7 
Pip (~8.1.1) 
OpenCV2 
Opencv2_contrib 
Pillow 
Twilio 
MySQLdb 
smtplib 
Numpy

DATABASE:

Database Name: CMPE273 
DB User: root 
DB password: '' 
Create Table sql:

create table student sjsu_id varchar(9),name varchar(50),email_id varchar(50),image longblob


Installation Steps:

1. Download folder 'FaceRecognizer'.
2. Create folders dataset, recognizer and images.

    mkdir dataset, recognizer and images.
    
3. Browse to the current working directory.
4. Run 'python compareimage.py'.
5. Connect to the localhost in the browser.
