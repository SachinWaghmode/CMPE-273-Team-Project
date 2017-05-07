
from flask import Flask,render_template
app = Flask(__name__)
import os
import cv2
import numpy as np
from PIL import Image, ImagePath

recognizer = cv2.face.createLBPHFaceRecognizer()
path = '/Users/sachinwaghmode/CMPE273/CMPE273-teamproject/images/'

@app.route('/')
def index():
   return render_template('matchimage.html')

@app.route('/matchimage.html')
def getImagesWithID(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    print imagePaths
    faces = []
    IDs=[]
    for imagePath in imagePaths:
        print imagePath
        faceImg=Image.open(imagePath).convert('L')
        faceNp=np.array(faceImg,'uint8')
        ID= int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        print ID
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)
    return np.array(IDs), faces
if __name__ == '__main__':
    app.run(debug = True)
    Ids,faces = getImagesWithID(path)
    recognizer.train(faces,Ids)
    recognizer.save('CMPE273-teamproject/trainingData.yml')
    cv2.destroyAllWindows()