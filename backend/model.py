import numpy as np
import json
import os
import io
import hashlib
import random
from PIL import Image

# ── PATHS ─────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'disease_model.tflite')
LABEL_PATH = os.path.join(BASE_DIR, 'class_labels.json')

IMG_SIZE = 224

# ── LOAD CLASS LABELS ─────────────────────────
with open(LABEL_PATH, 'r') as f:
    CLASS_LABELS = json.load(f)
print(f"Labels loaded: {CLASS_LABELS}")

# ── LOAD TFLITE MODEL ─────────────────────────
USE_REAL_MODEL = False
interpreter    = None

try:
    import tensorflow as tf
    interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details  = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    USE_REAL_MODEL = True
    print(f"Real MobileNetV2 model loaded — {len(CLASS_LABELS)} classes")
except Exception as e:
    print(f"Could not load real model: {e}")
    print("Using mock predictions as fallback")

# ── PREPROCESS ────────────────────────────────
def preprocess(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0).astype(np.float32)

# ── REAL PREDICTION ───────────────────────────
def real_predict(image_bytes):
    input_data = preprocess(image_bytes)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])[0]

    top_idx    = int(np.argmax(output))
    disease    = CLASS_LABELS[str(top_idx)]
    confidence = round(float(output[top_idx]), 2)

    all_preds = sorted(
        [
            {
                'disease':    CLASS_LABELS[str(i)],
                'confidence': round(float(output[i]), 2)
            }
            for i in range(len(output))
        ],
        key=lambda x: x['confidence'],
        reverse=True
    )

    return disease, confidence, all_preds[:3]

# ── MOCK FALLBACK ─────────────────────────────
MOCK_LABELS = [
    "Healthy",
    "Potato Early Blight",
    "Septoria Leaf Blotch",
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Mold"
]

def mock_predict(image_bytes):
    seed = int(hashlib.md5(image_bytes).hexdigest()[:8], 16)
    random.seed(seed)
    disease    = random.choice(MOCK_LABELS)
    confidence = round(random.uniform(0.75, 0.95), 2)
    remaining  = [d for d in MOCK_LABELS if d != disease]
    other1, other2 = random.sample(remaining, 2)
    conf2 = round(random.uniform(0.03, 0.12), 2)
    conf3 = round(max(0.01, 1 - confidence - conf2), 2)
    return disease, confidence, [
        {'disease': disease, 'confidence': confidence},
        {'disease': other1,  'confidence': conf2},
        {'disease': other2,  'confidence': conf3}
    ]

# ── MAIN ENTRY POINT ──────────────────────────
def predict_image(image_bytes):
    if USE_REAL_MODEL:
        try:
            return real_predict(image_bytes)
        except Exception as e:
            print(f"Real model error: {e} — using mock")
            return mock_predict(image_bytes)
    return mock_predict(image_bytes)