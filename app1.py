import os
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

# =========================
# FLASK APP
# =========================

app = Flask(__name__)

# =========================
# LOAD MODEL
# =========================

MODEL_PATH = r"C:\Users\Veda sri\OneDrive\Documents\Desktop\BrainTumorProject\brain_tumor_model.keras"

model = load_model(MODEL_PATH)

print("✅ Model loaded successfully!")
print("🚀 Open Browser: http://127.0.0.1:5000")

# =========================
# CLASS NAMES
# =========================

CLASS_NAMES = {
    0: "Glioma Brain Tumor Detected",
    1: "Meningioma Brain Tumor Detected",
    2: "No Brain Tumor Detected",
    3: "Pituitary Brain Tumor Detected"
}

# =========================
# PREDICTION FUNCTION
# =========================

def predict_image(img_path):

    # IMPORTANT:
    # Use SAME SIZE as training
    img = load_img(img_path, target_size=(224, 224))

    img_array = img_to_array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    print("Raw Prediction:", prediction)

    predicted_class = np.argmax(prediction, axis=1)[0]

    confidence = np.max(prediction) * 100

    print("Predicted Class:", predicted_class)
    print("Confidence:", confidence)

    return predicted_class, confidence

# =========================
# HOME PAGE
# =========================

@app.route('/', methods=['GET'])
def home():

    return render_template('index.html')

# =========================
# PREDICT ROUTE
# =========================

@app.route('/submit', methods=['POST'])
def upload():

    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Upload folder
    basepath = os.path.dirname(__file__)

    upload_folder = os.path.join(basepath, 'uploads')

    os.makedirs(upload_folder, exist_ok=True)

    # Save file
    file_path = os.path.join(
        upload_folder,
        secure_filename(file.filename)
    )

    file.save(file_path)

    # Predict
    class_id, confidence = predict_image(file_path)

    result = CLASS_NAMES[class_id]

    return f"""
    <h2>{result}</h2>
    <h3>Confidence: {confidence:.2f}%</h3>
    """

# =========================
# MAIN
# =========================

if __name__ == '__main__':

    app.run(debug=True)