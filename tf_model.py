
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import timeit

import tensorflow as tf
from keras.datasets import mnist

from tensorflow.keras import layers
keras = tf.keras
AUTOTUNE = tf.data.experimental.AUTOTUNE ## tf.data transformation parameters

matplotlib.style.use('ggplot')

def reshape_img(images):
    return images.reshape(images.shape[0], images.shape[1], images.shape[2], 1)

def load_model():
    model = keras.models.load_model('mnist_5epochs_20191027.h5')
    (train_images,train_labels),(test_images,test_labels) = mnist.load_data()   
    train_images = reshape_img(train_images)
    test_images = reshape_img(test_images)
    model.fit(train_images,train_labels,epochs=10)
    # test_loss, test_acc = model.evaluate(test_images, test_labels)
    # print('\nTest accuracy {:5.2f}%'.format(100*test_acc))
    return model


if __name__ == '__main__': 
    from datetime import datetime
    saved_model_path = "./saved_models/mnist_5epochs_{}.h5".format(datetime.now().strftime("%Y%m%d")) # _%H%M%S
    # Save entire model to a HDF5 file
    load_model().save(saved_model_path)