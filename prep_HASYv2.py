from IPython.display import Image
import matplotlib.pyplot as plt
from PIL import Image as img
import numpy as np
import pandas as pd
from clf import get_clf

import cv2
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split



def make_pixel_array(df):
    im = img.open('HASYv2/'+df['path'],'r').convert('L')
    return np.asarray(im)  ##255-val inverts colors


def read_process_images(img_list,y,invert=False):
    nrows = 28
    ncolumns = 28
    channels = 1
    img_list,y = shuffle(img_list,y)
    #y = [int(label) for label in y] 
    X=[]
    for path in img_list:
        image = 'HASYv2/' + path       ##can do color .IMREAD_COLOR
        X.append(cv2.resize(cv2.imread(image,cv2.IMREAD_GRAYSCALE),(nrows,ncolumns),interpolation=cv2.INTER_CUBIC))
    if invert==True:
        return 255-np.array(X),np.array(y)
    return np.array(X),np.array(y)

def prep():
    label_file = 'HASYv2/hasy-data-labels.csv'
    useful = pd.read_csv('symbol_map.csv')
    sym_list = list(useful.symbol_id)
    del useful
    digits = pd.read_csv(label_file)
    # sym_file = 'HASYv2/symbols.csv'
    # symbols = pd.read_csv(sym_file)
    digits = digits[digits.apply(lambda x: True if x.symbol_id in sym_list else False,axis=1)]
    digits['pixels']=digits.apply(make_pixel_array,axis=1)
    X,y = read_process_images(digits['path'],digits['latex'],invert=True)
    del digits
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=.8)
    return get_clf(X_train, X_test, y_train, y_test)

  
