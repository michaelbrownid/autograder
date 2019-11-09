import os
#import magic
import urllib.request
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from PIL import Image
from predict import predict_tf
import tensorflow as tf
keras = tf.keras
import cv2
from PIL import Image

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

tf_model = keras.models.load_model('static/mnist_hasyv2_master_20epochs_batch64_201911081573209782.h5')  #tf_model.h5
#tf_model = keras.models.load_model('static/tf_model.h5')

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	# return render_template('upload.html')
	return render_template('index.html')

@app.route('/predict')
def predict():
	# return render_template('crop.html')
	filename = '~/Downloads/imagename.png'
	predictions = predict_tf(tf_model,filename)
	return str(predictions)


@app.route('/crop')
def crop():
	# return render_template('crop.html')
	return render_template('testcrop.html')   ##credit to Pen by Moncho Varela

# @app.route('/landingpage/<imgurl>',methods=['GET', 'POST', 'PUT'])
# def landingpage(imgurl):
@app.route('/landingpage',methods=['GET', 'POST', 'PUT'])
def landingpage():
	url=request.args['imgurl']
	imgfile,typee  = urllib.request.urlretrieve(str(url) )
	arr=cv2.imread(imgfile) 
	im = Image.fromarray(arr)
	tempfile = 'cropped_image.jpg'
	im.save(tempfile)
	predictions = predict_tf(tf_model,tempfile)
	#return str(predictions)	
	return '<img src=\"'+url+'\"><br><h1>'+str(predictions)	+'</h1>'

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			data = open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'rb')
			s3.Bucket('autograder-site').put_object(Key='/my_app/uploads/temp.jpg',Body = data)
			flash('File successfully uploaded')
			return redirect('/crop')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":
    app.run()

# from tesseract import *
# import pytesseract

# def ocr_core(filename):
#     """
#     This function will handle the core OCR processing of images.
#     """
#     text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
#     return text

# print(ocr_core('uploads/HANDWRITING__5113_original_from_photo.jpg'))