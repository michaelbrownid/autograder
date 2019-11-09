from skimage import io
from skimage import filters, color
from scipy import ndimage as ndi
from PIL import Image
import cv2



import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,6)

from itertools import chain
from math import ceil 
import subprocess
import os


from sklearn import svm
from matplotlib.colors import Normalize

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

colors = np.array(list(chain(mcolors.BASE_COLORS.values())))        ##mcolors.CSS4_COLORS



def count_seg(filename):
    image = io.imread(filename)
    gray_image = color.rgb2gray(np.invert(image))
    thresh = filters.threshold_mean(gray_image)
    binary = gray_image > thresh
    label_arr, num_seg = ndi.label(np.invert(binary))
    return num_seg

def label_segments(filename,savename='',photo=False,marker=False):
    alpha=1.1
    beta=0
    image = cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    if marker==False:
        try:
            image = cv2.blur(image, (8, 8))
        except:
            pass
    # fig,axes = plt.subplots(1,figsize=(20,10))
    # axes.imshow(image,cmap='gray')
    # axes.set_title('Raw Image')         
    if photo:
        arrraaayyy = np.array(image)
        gray_image = color.rgb2gray(arrraaayyy)
        meaaannn = np.mean(gray_image)
        if marker:
            binary = gray_image>(meaaannn*.9)
        else:
            binary = gray_image>(meaaannn*.85)
        huh = (binary==1)*0+(binary==0)*1
        temp = savename+'_original_from_photo.png'
        io.imsave(temp,np.array(image, dtype = np.uint8 ))
        label_arr, num_seg = ndi.label(huh)   
        #plot_numbered_image(label_arr)
        segments = np.arange(1,num_seg+1)
        fig,axes = plt.subplots(1,figsize=(20,10))
        axes.imshow(huh)
        axes.set_title('Postprocessed Image')
        return huh,np.array(label_arr),segments,image #label_segments(temp,savename,photo=False)
    else:
        gray_image = color.rgb2gray(image)
        thresh = filters.threshold_mean(gray_image)
        binary = gray_image > thresh

    io.imsave(savename+'_original.jpg',(np.array(binary*1, dtype = np.uint8 )))
#     binary = tf.image.convert_image_dtype(binary, dtype=tf.uint8)  ##suppresses warning of lossy conversion
#     io.imsave(savename+'_original.png',binary)
    label_arr, num_seg = ndi.label(np.invert(binary))
    
    segments = np.arange(1,num_seg+1)
    print(segments)
    return binary*1,np.array(label_arr),segments,image

def plot_image(label_arr):
    plt.subplots(ncols=1, nrows=1, figsize=(8, 8))
    plt.imshow(label_arr, cmap=plt.cm.gray)
    plt.title("Labeled image")
    plt.show()


def plot_numbered_image(label_arr,savename='',no_rotate=False):
    colors = np.array(list(chain(mcolors.TABLEAU_COLORS.values())))
    # np.repeat(colors,2)                                         ### put in repeat for large sets
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
                ax.text(i,j,val,fontsize=20,color=colors[val])
    plt.xticks([])
    plt.yticks([])            
    plt.show()
    fig.savefig(savename+'_segmented.png')

# def convert_inkml(directory, out_folder):
#     ink_files = []
#     f = os.popen("ls %s*.inkml" %directory)
#     for i in f.readlines():
#         ink_files.append(i[:-1])
#     f.close()    

#     for filename in ink_files:
#         outfile = out_folder +filename[len(directory):-6]+'.png'
#         print(filename,outfile)
#         conv.inkml2img(filename,outfile)    



# def crop_image(segment,label_arr,binary_arr,ax=None,plot=False,model=None,direc='export/',svc=False,tf=False):
#     nrows = 28
#     ncolumns = 28
#     found = label_arr == segment   
#     x,y = np.where(found)
#     xmin,xmax,ymin,ymax = np.min(x),np.max(x),np.min(y),np.max(y)
#     xlen,ylen = found[xmin:xmax,ymin:ymax].shape
#     diff = np.abs(ylen-xlen)
#     change = ceil(diff/2)
#     if diff!=0:
#         if ylen>xlen:
#             xmin-=change
#             xmax+=change

#         else:
#             ymin-=change
#             ymax+=change
#         xlen,ylen = xmax-xmin,ymax-ymin
#         diff=np.abs(ylen-xlen)
#         if xlen>ylen: ymax+=diff
#         elif ylen>xlen: xmax+=diff

#     prediction=None
#     digit = binary_arr[xmin:xmax,ymin:ymax]
#     digit = np.pad(digit,int(len(digit)*.2),mode= 'constant', constant_values=(1,1))  

#     try:
#         xlen,ylen = digit.shape
#     except:
#         return
#     if ylen<20 or xlen<20 or np.mean(digit)<.02:
#         if plot: ax.set_visible(False)
#         return None,[ymin,prediction],xmin,digit  
#     if xlen/ylen>1.2 or xlen/ylen<0.8:
#         if plot: ax.set_visible(False)
#         return None,[ymin,prediction],xmin,digit  
#     tempfile = direc+str(segment)+'.jpg'
#     Image.fromarray(digit).save(tempfile)
#     if count_seg(tempfile)>=2:
#         if plot: ax.set_visible(False)
#         return None,[ymin,prediction],xmin,digit
#     img = cv2.resize(cv2.imread(tempfile,cv2.IMREAD_GRAYSCALE),(nrows,ncolumns),interpolation=cv2.INTER_CUBIC)
#     if model!=None: 
#         if tf:
#             prediction = np.argmax(model.predict(img.astype(float).flatten().reshape((1, 28, 28, 1)))) 
#             if model.predict(img.astype(float).flatten().reshape((1, 28, 28, 1)))[prediction]<.2:
#                 prediction = None
#         elif svc:
#             scaler = StandardScaler()
#             prediction = model.predict(scaler.fit_transform(img).flatten().reshape(1,-1))[0]

#         else:
#             prediction = model.predict(img.flatten().reshape(1,-1))[0]
#         predicted = '  Prediction: '+str(prediction)    
        
#     else: predicted= None
#     if plot==True:
#         if ax!= None:
#             ax.imshow(digit,cmap='Greys_r')
#             ax.set_title('Segment #'+str(segment)+predicted,fontsize=15)
            
#         else:
#             plt.imshow(digit,cmap='Greys_r')
#             plt.title('Segment #'+str(segment)+predicted,fontsize=15)
#     return img,[ymin,prediction],digit
    


# def process_image(filename,dirname,fitted_clf,plot=False,svc=False,tf=False,photo=False):
#     binary_arr,label_arr, segments,orig = label_segments(filename,dirname,photo)
#     # plot_numbered_image(label_arr,dirname)
#     temp = 'tempimgs/'
#     predicted=[]    
#     if plot:
#         fig,axes = plt.subplots(len(segments),1,figsize=(5,len(segments)*5))
#         for seg,ax in list(zip(segments,axes.flatten())):
#             try: 
#                 if crop_image(seg,label_arr,orig,model=fitted_clf,direc=temp,svc=False,tf=True)==None:
#                     predicted.append(None)
#             except:
#                 predicted.append(crop_image(seg,label_arr,orig,ax=ax,plot=True,model=fitted_clf,direc=temp,svc=svc,tf=tf)[1])
#         fig.savefig(dirname+'_predictions.png')
#     else:
#         for seg in segments:
#             if tf:
#                 try: 
#                     if crop_image(seg,label_arr,orig,model=fitted_clf,direc=temp,svc=False,tf=True)==None:
#                         finding='%'
#                 except:
#                     finding = crop_image(seg,label_arr,orig,model=fitted_clf,direc=temp,svc=False,tf=True)[1]
#                 if finding!= None:
#                     predicted.append(finding)            
#             elif svc:
#                 predicted.append(crop_image(seg,label_arr,orig,model=fitted_clf,direc=temp,svc=True,tf=False)[1])
#             else:
#                 predicted.append(crop_image(seg,label_arr,orig,model=fitted_clf,direc=temp,svc=False,tf=False)[1])
#     try:
#         predicted.sort()
#         pred = [p[1] for p in predicted]
#     except:
#         pred = predicted
#     while(len(pred)>4):
#         try:
#                 pred.remove(None)
#         except:
#             try: 
#                 pred.remove(3)
#             except:
#                 pred.pop()
#     result = np.array(pred)
#     result = np.where(result==None, 1, result)
#     if result.shape!=(4,):
#         result = list(result)
#         try:
#             result.sort()
#             result = np.array([p[0] for p in result]   )
#         except:
#             pass
# #     edited = np.where(result==None, 1, result)
#     return result


# def setdiff(x):
#     return x['truth']==x['predict']

# def main(prepared=0,svc=False,fitted_clf=None,tf=False):
#     (X_tr,y_tr),(X_ts,y_ts) = mnist.load_data()   
#     if fitted_clf==None:
#         yhat, acc,fitted_clf =  get_clf(X_tr,X_ts,y_tr,y_ts)
#     if prepared.all() == 0:
#         dataset = make_stuff(X_ts[:2000])
#         results = pd.DataFrame(dataset)
#     else:
#         results = pd.DataFrame(prepared)
#     results.columns = ['image','truth']
#     predictions = []
#     for index,image in enumerate(results['image']):
#         matname = 'tf22/output__'+str(index)
#         print(image)
#         predictions.append(process_image(image,matname,fitted_clf,svc=svc,tf=tf))
    
#     predictions=np.array(predictions)
#     results['predict'] = predictions
#     results['correct']=results.apply(setdiff,axis=1)
#     results.to_csv('results_TF.csv')
#     return results


# def getscore(x):
#     if x['string']=='False':
#         return -10
#     else:
#         return x['string'].count('True')/4
        
# def process_results(results4):
#     results4['string']= results4.correct.astype(str)
#     results4['score'] = results4.apply(getscore,axis=1)    
#     mismatched = results4[results4.score<0]
#     mainset = results4[results4.score>=0]
#     mismatched.drop('string',axis=1,inplace=True)
#     mainset.drop('string',axis=1,inplace=True)
#     return results4, mismatched, mainset
