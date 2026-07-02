from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from config import CATEGORY_THRESHOLD

MODEL_PATH = "model"

LABELS = [
    "malignant",
    "highly_malignant",
    "rude",
    "threat",
    "abuse",
    "loathe"
]


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==========================
# Load Model
# ==========================

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

model.to(device)
model.eval()

print("Model loaded successfully!")

# ==========================
# Prediction Function
# ==========================

def analyze_message(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=256
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.sigmoid(outputs.logits)[0].cpu().numpy()

    detected_categories = []

    max_probability = 0.0

    for label, probability in zip(LABELS, probabilities):

        probability = float(probability)

        max_probability = max(max_probability, probability)

        if probability >= CATEGORY_THRESHOLD:

            detected_categories.append({

                "category": label,

                "confidence": round(probability * 100, 2)

            })

    is_safe = len(detected_categories) == 0

    detected_names = [

        item["category"]

        for item in detected_categories

    ]

    if is_safe:

        severity = "Safe"

    elif (
        "threat" in detected_names
        or
        "highly_malignant" in detected_names
    ):

        severity = "High"

    elif len(detected_names) >= 2:

        severity = "Medium"

    else:

        severity = "Low"

    return {

        "safe": is_safe,

        "severity": severity,

        "confidence": round(max_probability * 100, 2),

        "categories": detected_categories

    }