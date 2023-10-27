from flask import Flask, request,Response, jsonify
from sklearn.neighbors import KNeighborsClassifier
import tensorflow as tf
from preprocess import get_embeddings
from flask_cors import CORS
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array,load_img
import io
import os
import numpy as np
import json

app = Flask(__name__)
CORS(app)

knn = KNeighborsClassifier(n_neighbors=7)
features, labels, embeddings, styles_df = get_embeddings()
img_size=224
path = 'fashion/images'
knn.fit(features, labels)

UPLOAD_FOLDER = "uploads"

def read_img(image_path):
    image = load_img(image_path,target_size=(img_size,img_size,3))
    image = img_to_array(image)
    image = image/255.
    return image

@app.route('/train', methods=['GET'])
def train():
    knn.fit(features, labels)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        image = request.files["image"]
        img_path=os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(img_path)
        image=read_img(img_path)
        prediction = embeddings.predict(image[None,:])  # Extract features from the uploaded image
        dist, index = knn.kneighbors(X=prediction.reshape(1,-1)) 
        similar_images=[]
        for i in range(7):
            similar_images.append(styles_df.loc[index[0][i],'filename'])
        response=jsonify({'similar_images': similar_images})
        response.headers["Access-Control-Allow-Origin"]="*"
        return json.dumps({'similar_images': similar_images})
    except Exception as e:
        response= jsonify({'error': str(e)})
        response.headers["Access-Control-Allow-Origin"]="*"
        return response

if __name__ == '__main__':
    app.run(debug=True)
