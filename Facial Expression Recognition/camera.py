from cv2 import cv2
from model import FacialExpressionModel
import numpy as np
#import time

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")  # change model file here
font = cv2.FONT_HERSHEY_SIMPLEX


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        #deallocate resources before starting camera again
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, frame = self.video.read()
        gray_fr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y + h, x:x + w]

            # if float("%s" % (time.time() - st)) > 0.3:
            #     emotion = predict(model, roi_gray)
            #     st = time.time()

            roi = cv2.resize(fc, (48, 48))
            # start_time = time.time()
            # pred = None
            # if float("%s" % (time.time() - start_time)) > 0.3:
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            cv2.putText(frame, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        #encode image to memory buffer
        _, jpeg = cv2.imencode('.jpg', frame)
        #encode to bytes for sending video stream to HTML page
        return jpeg.tobytes()
