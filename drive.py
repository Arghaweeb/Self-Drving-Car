
import socketio
import eventlet
import numpy as np
from flask import Flask
from keras.models import load_model
import base64
from io import BytesIO
from PIL import Image
import cv2

sio = socketio.Server()

app = Flask(__name__) #'_main_'

def img_preprocess(img):
  img = img[60:140, :,:]
  img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)  #y- luminasity #UV Chromiance # Nvidia model uses YUV color spaces instead of RGB
  img = cv2.GaussianBlur(img, (3,3), 0)
  img = cv2.resize(img, (200, 66))
  img = img/255 #normalizing
  return img

@sio.on('telemetry')
def telemetry(sid, data):
    spped = float(data['speed'])
    image = Image.open(BytesI0(base64.b64decode(data['image'])))
    image = np.asarray(image)
    image = img_preprocess(image)
    image = np.array([image])
    steering_angle = float(model.predict(image))
    throttle = 1.0 - speed/spped_limit
    print('{} {} {}').format(steering_angle, throttle, speed))
    send_control(steering, 1.0)

@sio.on('connect')
def connect(sid, environ):
    print('Connected')
    send_control(0, 0)

def send_control(steering_angle, throttle):
    sio.emit('steer', data = {
          'steering_angle': steering_angle.__str__(),
          'throttle': throttle.__str__()
    })

if __name__ == '__main__':
    model = load_model('model.h5')
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('',4567)), app)
