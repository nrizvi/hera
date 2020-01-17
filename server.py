#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import cherrypy

config = {
    'global' : {
        'server.socket_host' : '127.0.0.1',
        'server.socket_port' : 8080
    }
}

import keras
from keras.models import model_from_json

model = model_from_json(open('model.json').read())
model._make_predict_function()

import cv2
import imageio
import numpy as np
import PIL
from PIL import Image

CORR = {
    0: 'an Atrial Arrhythmia',
    1: 'a Ventricular Escape',
    2: 'a Left Bundle Branch block',
    3: 'a normal',
    4: 'a paced ',
    5: 'a Right Bundle Branch block',
    6: 'a Ventricular Arrhythmia'
}

description = {
    0: 'Atrial arrhythmia, also called supraventricular arrhythmia, begins in the upper chambers of the heart and includes: atrial fibrillation, atrial flutter, sick sinus syndrome, sinus tachycardia, sinus bradycardia. Abnormal electrical impulses in the upper chambers of the heart cause atrial arrhythmia. People with atrial arrhythmias often feel tired and sluggish, and may experience a flutter in their chest or throat. <p><i>This information was obtained from the Frankel Cardiovascular Center at the University of Michigan. <a href="https://www.umcvc.org/conditions-treatments/atrial-arrhythmia">Click here</a> to learn more.</p>',
    1: 'A ventricular escape beat is a self-generated electrical discharge initiated by, and causing contraction of, the ventricles of the heart; normally the heart rhythm is begun in the atria of the heart and is subsequently transmitted to the ventricles. The ventricular escape beat follows a long pause in ventricular rhythm and acts to prevent cardiac arrest. It indicates a failure of the electrical conduction system of the heart to stimulate the ventricles (which would lead to the absence of heartbeats, unless ventricular escape beats occur). An escape beat is a form of cardiac arrhythmia, in this case known as an ectopic beat. <a href="https://en.wikipedia.org/wiki/Ventricular_escape_beat">Click here</a> to learn more.',
    2: 'A left bundle branch block beat is a delay or blockage of electrical impulses to the left side of the heart. Left bundle branch block sometimes makes it harder for the heart to pump blood efficiently through the circulatory system. Most people do not have symptoms. If symptoms occur, they include fainting or a slow heart rate. If there is an underlying condition, such as heart disease, that condition needs treatment. In patients with heart failure, a pacemaker also can relieve symptoms as well as prevent death. <a href="https://www.cedars-sinai.org/health-library/diseases-and-conditions/l/left-bundle-branch-block.html">Click here </a> to learn more.',
    3: 'Our app has not identified any significant abnormalities in your ECG.',
    4: 'This ECG may be showing an abnormal pacemaker function. <a href="https://www.uptodate.com/contents/ecg-tutorial-pacemakers">Click here</a> to learn more about pacemaker rhythms.',
    5: 'Bundle branch blocks usually do not cause symptoms. They are not considered to be irregular heartbeats or arrhythmias. A block in the right bundle branch can occur in people who otherwise seem normal. If it happens with a heart attack, it can be a sign of serious heart muscle damage. <a href="https://www.ncbi.nlm.nih.gov/books/NBK507872/">Click here </a> to learn more.',
    6: 'Ventricular arrhythmias are abnormal heartbeats that originate in your lower heart chambers, called ventricles. These types of arrhythmias cause your heart to beat too fast, which prevents oxygen-rich blood from circulating to the brain and body and may result in cardiac arrest. <a href="https://stanfordhealthcare.org/medical-conditions/blood-heart-circulation/ventricular-arrhythmia/types.html">Click here </a> to learn more.'
}

class App:

    @cherrypy.expose
    def upload(self, ufile):
        # Either save the file to the directory where server.py is
        # or save the file to a given path:
        # upload_path = '/path/to/project/data/'
        upload_path = os.path.dirname(__file__)

        # Save the file to a predefined filename
        # or use the filename sent by the client:
        # upload_filename = ufile.filename
        upload_filename = 'image.jpg'

        upload_file = os.path.normpath(
            os.path.join(upload_path, upload_filename))
        size = 0

        im = imageio.imread(ufile.file.read())
        im = cv2.resize(im, (128, 128), interpolation = cv2.INTER_LANCZOS4)
        if len(im.shape) > 2 and im.shape[2] == 4:
            im = cv2.resize(im, (128, 128), interpolation = cv2.INTER_LANCZOS4)
            im = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)
        im = im.astype('float32')
        im/=255.0
        pred = model.predict(np.array([im]))

        pred_number = np.argmax(pred[0]) # Number can be 0,1,2,3,4,5,6
        pred_prob = pred[0][pred_number] # Probability of prediction
        pred_str = CORR[pred_number] # Label
        pred_desc = description[pred_number]

        with open(upload_file, 'wb') as out:
            while True:
                data = ufile.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        out = '''
<html lang="en">
<head>
  <title>Test Page</title>
  <meta charset="utf-8"/>
  <link href="https://fonts.googleapis.com/css?family=Montserrat:900|Open+Sans" rel="stylesheet">
  <style>
a {color:white;}
a:hover {color:peachpuff;}
</style>
</head>
  <body id="body" style="background-color:#ff914d; max-width:75%; margin:auto;">
    <div class="center" style="margin-top:20%;">
        <span style="text-align:center;"><h2 style="color:white;font-family: 'Open Sans', 
        sans-serif;">You have ''' + pred_str + ''' beat. ''' + pred_desc + '''
</h2></span>
    </div>
  </body>
</html>
'''#.format(ufile.filename, size, ufile.content_type, data)
        os.remove("image.jpg")
        return out


if __name__ == '__main__':
    cherrypy.quickstart(App(), '/', config)