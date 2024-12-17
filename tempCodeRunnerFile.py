import os
from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the model
MODEL_PATH = 'models/model_v1.h5'
model = load_model(MODEL_PATH)

# Define class labels
class_labels = ["Normal", "COVID-19", "Viral"]

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    if file:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Preprocess the image
        image = load_img(file_path, target_size=(224, 224))  # Adjust target size to match your model input
        image_array = img_to_array(image) / 255.0           # Normalize pixel values
        image_array = np.expand_dims(image_array, axis=0)   # Add batch dimension

        # Make prediction
        predictions = model.predict(image_array)
        predicted_class = class_labels[np.argmax(predictions)]

        return render_template('index.html', prediction=predicted_class, image_url=file_path)

# Run the app
if __name__ == "__main__":
    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
