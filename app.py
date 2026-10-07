import os
import numpy as np
import keras
from keras.utils import load_img, img_to_array
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ====================== MODEL LOADING ======================

model_path = "brain_tumor_model_fixed.h5"

class SafeDense(keras.layers.Dense):
    def __init__(self, **kwargs):
        kwargs.pop("quantization_config", None)
        super().__init__(**kwargs)

def load_compatible_model(path):
    return keras.models.load_model(
        path,
        compile=False,
        custom_objects={"Dense": SafeDense}
    )

model = load_compatible_model(model_path)
print("✅ Model loaded successfully!")

# ===========================================================

def get_className(prediction):
    classes = {
        0: "Glioma Brain Tumor Detected",
        1: "Meningioma Brain Tumor Detected",
        2: "No Brain Tumor Detected",
        3: "Pituitary Brain Tumor Detected"
    }
    return classes.get(prediction, "Unknown")


def predict(img_path):
    test_image = load_img(img_path, target_size=(224, 224))

    image = img_to_array(test_image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    result = model.predict(image, verbose=0)

    predicted_class = np.argmax(result, axis=1)[0]
    confidence = float(np.max(result)) * 100

    return predicted_class, confidence


# ====================== ROUTES ======================

@app.route('/')
def home():
    return render_template('index.html')


# About Us Page Route
@app.route('/project2')
def project2():
    return render_template('BTD/project2.html')


@app.route('/predict', methods=['POST'])
def predict_route():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    f = request.files['file']

    if f.filename == '':
        return jsonify({"error": "No file selected"}), 400

    basepath = os.path.dirname(__file__)

    upload_folder = os.path.join(basepath, "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(
        upload_folder,
        secure_filename(f.filename)
    )

    f.save(file_path)

    try:
        class_id, confidence = predict(file_path)

        return jsonify({
            "result": get_className(class_id),
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ====================== RUN APP ======================

if __name__ == '__main__':
    print("🚀 Flask app started at http://127.0.0.1:5000")
    app.run(debug=True)