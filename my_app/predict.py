import os
import pandas as pd
import numpy as np

from math import ceil 
from skimage import io
from skimage import filters, color
from scipy import ndimage as ndi
from PIL import Image
import cv2
import matplotlib
matplotlib.rcParams.update({'figure.max_open_warning': 0})

import processing as proc

from tensorflow.keras import models
import matplotlib.pyplot as plt
import pickle
import pandas as pd
import os

import shutil  




def predict_tf(tf_model, image):
    matname = 'data/predictions__img'
    print('processing ',image)
    binary_arr,label_arr, segments,orig = proc.label_segments(image,matname,photo=True,marker=False)
    os.remove(image)
    predicted = []
    fig,axes = plt.subplots(len(segments),figsize=(6,6*len(segments)))
    for seg,ax in list(zip(segments,axes.flatten())):
        found = label_arr==seg
        x,y = np.where(found)
        xmin,xmax,ymin,ymax = np.min(x),np.max(x),np.min(y),np.max(y)
        xlen,ylen = found[xmin:xmax,ymin:ymax].shape
        diff = np.abs(ylen-xlen)
        change = ceil(diff/2)
        if diff!=0:
            if ylen>xlen:
                xmin-=change
                xmax+=change

            else:
                ymin-=change
                ymax+=change

            xlen,ylen = xmax-xmin,ymax-ymin
            diff=np.abs(ylen-xlen)
            if xlen>ylen: ymax+=diff
            elif ylen>xlen: xmax+=diff
        digit = binary_arr[xmin:xmax,ymin:ymax]
        digit = np.pad(digit,int(len(digit)*.2),mode= 'constant', constant_values=(0,0))        
        if digit.shape[0]<10:
            ax.set_visible(False)       
            pass
        else:
            ax.imshow(digit,cmap='gray')
            im = Image.fromarray(np.array(digit)*255.0).convert("RGB")
            im.save('000.jpg')
            img = cv2.resize(cv2.imread('000.jpg',cv2.IMREAD_GRAYSCALE),(28,28),interpolation=cv2.INTER_CUBIC)
            os.remove('000.jpg')
            p = np.argmax(tf_model.predict(img.astype(float).flatten().reshape((1, 28, 28, 1))))
            ax.set_title(p)
            #im.save(matname+'___predicted____'+str(p)+'.jpg')
            predicted.append([ymin,p])

    predicted.sort()    
    predicted = [pr[1] for pr in predicted]
    plt.close('all')
    return predicted

if __name__ == "__main__":
    # tf_model = keras.models.load_model('static/mnist_hasyv2_master_20epochs_batch64_201911081573209782.h5')  #tf_model.h5
    # oldfilename = '/home/nina/Downloads/imagename.png'
    # filename = '/home/nina/autograder/my_app/imagename.png'
    
    # shutil.move(oldfilename,filename)
    # predictions = predict_tf(tf_model,filename)
    # print(predictions)
    pass