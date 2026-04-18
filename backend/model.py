import hashlib
import random

CLASS_LABELS = [
    "Wheat Leaf Rust",
    "Septoria Leaf Blotch",
    "Tomato Leaf Mold",
    "Potato Early Blight",
    "Rice Blast",
    "Healthy"
]

def predict_image(image_bytes):
    image_hash = hashlib.md5(image_bytes).hexdigest()
    seed = int(image_hash[:8], 16)
    random.seed(seed)

    disease = random.choice(CLASS_LABELS)
    confidence = round(random.uniform(0.75, 0.95), 2)

    remaining = [d for d in CLASS_LABELS if d != disease]
    other1, other2 = random.sample(remaining, 2)

    conf2 = round(random.uniform(0.03, 0.12), 2)
    conf3 = round(max(0.01, 1 - confidence - conf2), 2)  # clamp fix

    top_predictions = [
        {"disease": disease, "confidence": confidence},
        {"disease": other1, "confidence": conf2},
        {"disease": other2, "confidence": conf3}
    ]

    return disease, confidence, top_predictions