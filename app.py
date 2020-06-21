from __future__ import division, print_function

# Import fast.ai Library
from fastai import *
from fastai.vision import *

# coding=utf-8
import sys
import os
import glob
import re
from pathlib import Path
import json

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename


# Define a flask app
app = Flask(__name__)



path = Path("path")
classes = ['sheep', 'goat']
# data2 = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)
# learn = create_cnn(data2, models.resnet34)
# learn.load('stage-2')
learn = load_learner(path/'models')



def model_predict(img_path):
    img = open_image(img_path)
    pred_class,pred_idx,outputs = learn.predict(img)
    return outputs


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)

        #Goat
        if(preds[0] > preds[1]):
            numStr = str(preds[0] * 100)
            numStr = numStr[numStr.index('(')+1 : numStr.index('.')]
            return numStr + "% Goat"
        else:
            #Sheep
            numStr = str(preds[1] * 100)
            numStr = numStr[numStr.index('(')+1 : numStr.index('.')]
            return numStr + "% Sheep"        

    return None


if __name__ == '__main__':    
    app.run()



# FOR DEVELOPMENT CACHING
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# @app.after_request
# def add_header(r):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     r.headers["Pragma"] = "no-cache"
#     r.headers["Expires"] = "0"
#     r.headers['Cache-Control'] = 'public, max-age=0'
#     return r