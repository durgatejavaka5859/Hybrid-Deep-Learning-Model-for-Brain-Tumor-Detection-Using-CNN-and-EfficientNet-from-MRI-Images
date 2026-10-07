import tensorflow as tf
from tensorflow.keras.models import load_model

MODEL_PATH = r"C:\Users\Veda sri\OneDrive\Documents\Desktop\BrainTumorProject\model3.h5"
SAVED_MODEL_DIR = r"C:\Users\Veda sri\OneDrive\Documents\Desktop\BrainTumorProject\saved_model"

print("🔄 Loading model...")
try:
    model = load_model(MODEL_PATH, compile=False)
    print("✅ Model loaded successfully!")
    model.summary()

    print("💾 Saving to SavedModel format...")
    tf.saved_model.save(model, SAVED_MODEL_DIR)
    print(f"🎉 Conversion successful!\nSaved at: {SAVED_MODEL_DIR}")

except Exception as e:
    print(f"❌ Error: {e}")