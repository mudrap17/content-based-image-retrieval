import numpy as np
import pandas as pd
import os
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Activation, Dropout, Flatten, Dense, Input, Layer
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import matplotlib.pyplot as plt
import seaborn as sns

def get_embeddings():
    path = 'fashion/images'
    styles_df = pd.read_csv("styles.csv", on_bad_lines='skip')
    styles_df['filename'] = styles_df['id'].astype(str) + '.jpg'
    image_files = os.listdir(path)
    styles_df['present'] = styles_df['filename'].apply(lambda x: x in image_files)
    styles_df = styles_df[styles_df['present']].reset_index(drop=True)
    img_size = 224
    datagen = ImageDataGenerator(rescale=1/255.) 
    generator = datagen.flow_from_dataframe(dataframe=styles_df,
                                        directory=path,
                                        target_size=(img_size,img_size),
                                        x_col='filename',
                                        class_mode=None,
                                        batch_size=32,
                                        shuffle=False,
                                        classes=None)
    base_model = VGG16(include_top=False, input_shape=(img_size,img_size,3))
    for layer in base_model.layers:
        layer.trainable = False

    input_layer = Input(shape=(img_size,img_size,3))
    x = base_model(input_layer)
    output = GlobalAveragePooling2D()(x)
    embeddings = Model(inputs=input_layer, outputs=output)
    embeddings.summary()
    X = embeddings.predict(generator, verbose=1)
    y = styles_df['id']

    return (X,y,embeddings,styles_df)
