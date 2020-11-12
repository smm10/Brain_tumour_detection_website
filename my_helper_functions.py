import cv2
import tensorflow as tf
from tensorflow.keras.models import Model, load_model
import imutils


from flask import flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os

from settings import *


def crop_brain_contour(image, plot=False):
    #import imutils
    #import cv2
    #from matplotlib import pyplot as plt
    
    # Convert the image to grayscale, and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours in thresholded image, then grab the largest one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    

    # Find the extreme points
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    
    # crop new image out of the original image using the four extreme points (left, right, top, bottom)
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]           
    
    return new_image

'''
def prepare(img):
    IMG_SIZE = 70  # 50 in txt-based
    img_array = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
'''

def make_prediction(img):
    print("make prediction")
    #print(img)
    model = tf.keras.models.load_model(filepath='models/cnn-parameters-improvement-23-0.91.model')
    '''
    cropped_image = crop_brain_contour(img)
    image = cv2.resize(cropped_image, dsize=(240, 240), interpolation=cv2.INTER_CUBIC)
    image = image / 255
    '''

    prediction = model.predict(img)  # REMEMBER YOU'RE PASSING A LIST OF THINGS YOU WISH TO PREDICT

    return prediction[0][0]

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(request):
  if 'file' not in request.files:
    flash('No file!')
    return redirect(request.url)

  file = request.files['file']
  
  if file.filename == '':
    flash('No selected file')
    return redirect(request.url)

  if file and allowed_file(file.filename):
    filename = secure_filename(file.filename)
    filename = os.path.join(app.config['STATIC_FOLDER'], filename)
    file.save(filename)
    data = request.files['file']
    return data, filename


def open_image(path):
    image = cv2.imread(path)
    image = crop_brain_contour(image)
    image = cv2.resize(image, dsize=(240, 240), interpolation=cv2.INTER_CUBIC)
    image = image / 255
    image = image.reshape(-1, 240, 240, 3)
    return image


    #prediction = model.predict([cropped_image])
    