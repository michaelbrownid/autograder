
import numpy as np
from PIL import Image
from keras.datasets import mnist


def stack_imgs(row):
    stacked = np.hstack([Image.fromarray(img) for img in row])
    return Image.fromarray(255-stacked)


def grab_indices(indices,n,index_list):
    indices = list(np.arange(len(indices)))
    sel = np.random.choice(indices,4,replace=False)
    for ind in sel:
        indices.remove(ind)
    index_list.append(sel)
    del sel
    return indices,index_list

def make_stuff(X_ts=None,n=4):
    (a,c),(b,d) = mnist.load_data()
    X_ts = np.concatenate((a,b))
    y_ts = np.concatenate((c,d))    
    index_list=[]
    indices = list(np.arange(len(X_ts))) 
    for i in range(int(len(X_ts)/n)):
        indices,index_list = grab_indices(indices,n,index_list)
    unlabeled_pics = [ stack_imgs(row) for row in X_ts[index_list]]
    labeled_foursomes = list(zip(unlabeled_pics,y_ts[index_list]))
    labeled_foursomes = np.array(labeled_foursomes)
    return make_png(labeled_foursomes,savedir='generated_imageset/')


def make_png(labeled_foursomes,savedir='generated_imageset/'):
    file_list = []
    targets = []
    for i,img in enumerate(labeled_foursomes):
        truth = img[1]
        truth = ''.join([str(ans) for ans in truth])
        path = savedir+'merge_'+str(len(img[1]))+'_'+str(i)+'____'+truth+'.png'
        img[0].save(path)
        file_list.append(path)
        targets.append(img[1])
    return list(zip(file_list,targets))

