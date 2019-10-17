from skimage import io
from skimage import filters, color
from scipy import ndimage as ndi
from PIL import Image
import cv2

import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,6)

from scipy.misc import imresize
import inkml.inkml2img as conv
from itertools import chain
from math import ceil 
import subprocess
import os

colors = np.array(list(chain(mcolors.CSS4_COLORS.values())))

def count_seg(filename):
    image = io.imread(filename)
    gray_image = color.rgb2gray(np.invert(image))
    thresh = filters.threshold_mean(gray_image)
    binary = gray_image > thresh
    label_arr, num_seg = ndi.label(np.invert(binary))
    return num_seg

def label_segments(filename,savename=''):
    image = io.imread(filename)
    gray_image = color.rgb2gray(image)
    thresh = filters.threshold_mean(gray_image)
    binary = gray_image > thresh

    io.imshow(binary)
    io.show()
    io.imsave(savename+'_original.png',binary*1)

    label_arr, num_seg = ndi.label(np.invert(binary))
    print("number of segments", num_seg)
    segments = np.arange(1,num_seg+1)
    return binary,np.array(label_arr),segments

def plot_image(label_arr):
    plt.subplots(ncols=1, nrows=1, figsize=(8, 8))
    plt.imshow(label_arr, cmap=plt.cm.gray)
    plt.title("Labeled image")
    plt.show()


def plot_numbered_image(label_arr,savename=''):
    colors = np.array(list(chain(mcolors.CSS4_COLORS.values())))
    np.repeat(colors,2)                                         ### put in repeat for large sets
    pixarray=np.rot90(label_arr,3)
    imax,jmax = pixarray.shape
    fig,ax=plt.subplots(ncols=1, nrows=1, figsize=(20,int(20*jmax/imax)))
    plt.xticks(np.arange(0,imax))
    plt.yticks(np.arange(0,jmax))
    np.random.shuffle(colors)
    for i in range(imax):
        for j in range(jmax):
            val = pixarray[i][j]
            if val != 0:
                ax.text(i,j,val,fontsize=10,color=colors[val])
    plt.xticks([])
    plt.yticks([])            
    plt.show()
    fig.savefig(savename+'_segmented.png')

def convert_inkml(directory, out_folder):
    ink_files = []
    f = os.popen("ls %s*.inkml" %directory)
    for i in f.readlines():
        ink_files.append(i[:-1])
    f.close()    
    for filename in ink_files:
        outfile = out_folder +filename[len(directory):-6]+'.png'
        print(filename,outfile)
        conv.inkml2img(filename,outfile)    



def crop_image(segment,label_arr,binary_arr,ax=None,plot=False,model=None,direc='export/'):
    nrows = 28
    ncolumns = 28
    found = label_arr == segment    #plt.imshow(found)
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

    digit = np.invert(binary_arr[xmin:xmax,ymin:ymax])
    # digit = np.invert(label_arr[xmin:xmax,ymin:ymax])
    digit = np.pad(digit,int(len(digit)*.2))
    xlen,ylen = digit.shape
    if ylen/xlen>1.2 or ylen/xlen<0.8:
        ax.set_visible(False)
        return None  
    tempfile = direc+str(segment)+'.png'
    Image.fromarray(digit).save(tempfile)
    if count_seg(tempfile)>=2:
        ax.set_visible(False)
        return None
    img = cv2.resize(cv2.imread(tempfile,cv2.IMREAD_GRAYSCALE),(nrows,ncolumns),interpolation=cv2.INTER_CUBIC)

    prediction=''
    if model!=None: 
        prediction = model.predict(img.flatten().reshape(1,-1))[0]
        predicted = '  Prediction: '+str(prediction)    
        
    else: predicted= ''
    if plot==True:
        if ax!= None:
            ax.imshow(digit,cmap='Greys_r')
            ax.set_title('Segment #'+str(segment)+predicted,fontsize=15)
            
        else:
            plt.imshow(digit,cmap='Greys_r')
            plt.title('Segment #'+str(segment)+predicted,fontsize=15)

    return img,prediction,xmin,digit
    
