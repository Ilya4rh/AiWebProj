import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

model = load_model('AIWebProject/ml_models/food_classifier_model.h5')

def get_class_labels():
    return ['alfredo', 'broccoli', 'brownie',
            'cake', 'carrot', 'cereal', 'cheese', 'chicken', 'chocolate',
            'coffee', 'cookie', 'corn', 'couscous', 'crab', 'donut', 'egg',
            'fajitas', 'fries', 'grilledcheese', 'hotdog', 'icecream', 'macncheese',
            'nachos', 'nuggets', 'rice', 'salad', 'salmon', 'shrimp', 'soup', 'steak',
            'sushi', 'tartare']

def preprocess_uploaded_image(image_file):
    img = Image.open(image_file).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    return img_array

def predict_class(image_file):
    class_labels = get_class_labels()
    img_array = preprocess_uploaded_image(image_file)
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)
    return class_labels[predicted_index]