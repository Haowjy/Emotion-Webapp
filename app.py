#Import necessary libraries
from flask import Flask, render_template, Response

import os

import cv2

from keras.models import load_model
from keras.preprocessing import image

#import matplotlib.pyplot as plt
import numpy as np
import operator

# load the kaggle emotions model
path = os.path.dirname(os.path.abspath(__file__))
#print(path)
model = load_model(path + "/kaggle_emotions_model.h5")

# detect the face area
face_cascade = cv2.CascadeClassifier(path+'/cascades/data/haarcascade_frontalface_default.xml')

#emotion predictions
def emotion_analysis(emotions):
    objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    #y_pos = np.arange(len(objects))
    #plt.bar(y_pos, emotions, align='center', alpha=0.5)

    # for ob in range(len(objects[:6])):
    #     print(objects[ob] + ' percentage: ' + str(emotions[ob]))

    index,max_val = max(enumerate(emotions[:6]), key=operator.itemgetter(1))
    max_percent = round(max_val*100,1)
    return objects[index] + ' ' + str(max_percent) + '%'

#Initialize the Flask app
app = Flask(__name__)

camera = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame

        if not success:
            break
        else:
            # flip frame for mirror like effect
            frame = cv2.flip(frame,1)

            # grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # draw rectange on faces
            faces = face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
            for (x,y,w,h) in faces:
                roi_gray = gray[y:y+h+10, x:x+w]
                #resize frame
                test_frame = cv2.resize(roi_gray,(48,48), interpolation = cv2.INTER_AREA)
                #pass through neural network
                test = image.img_to_array(test_frame)
                test = np.expand_dims(test, axis = 0)
                test /= 255
                custom = model.predict(test)

                emotion = emotion_analysis(custom[0])
                font = cv2.FONT_HERSHEY_PLAIN
                font_color = (255,255,255)
                box_color = (0,0,0)

                color = (255,0,0) #BGR 0-255
                stroke = 2
                end_cord_x = x+w
                end_cord_y = y+h+10
                cv2.rectangle(frame, (x,y), (end_cord_x,end_cord_y),color,stroke)
                cv2.rectangle(frame, (x-10,y-50),(end_cord_x,y),box_color,-1)
                cv2.putText(frame,emotion,(x+20,y-10), font, 3, font_color, 1, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html',title="Emotion Detection")

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)