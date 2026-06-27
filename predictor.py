from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# ==========================
# Configuration
# ==========================

MODEL_PATH = "model"

LABELS = [
    "malignant",
    "highly_malignant",
    "rude",
    "threat",
    "abuse",
    "loathe"
]

THRESHOLD = 0.5

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

        if probability > max_probability:
            max_probability = probability

        if probability >= THRESHOLD:

            detected_categories.append({
                "category": label,
                "confidence": round(probability * 100, 2)
            })

    # Determine if message is safe
    is_safe = len(detected_categories) == 0

    # Determine severity
    if is_safe:
        severity = "Safe"

    elif max_probability >= 0.90:
        severity = "High"

    elif max_probability >= 0.70:
        severity = "Medium"

    else:
        severity = "Low"

    return {

        "safe": is_safe,

        "severity": severity,

        "confidence": round(max_probability * 100, 2),

        "categories": detected_categories

    }


# ==========================
# Test Mode
# ==========================

if __name__ == "__main__":

    print("\nHate Speech Detector Ready!\n")

    while True:

        text = input("You: ")

        if text.lower() in ["exit", "quit"]:
            break

        result = analyze_message(text)

        print("\nResult")
        print("------------------------")
        print(f"Safe: {result['safe']}")
        print(f"Severity: {result['severity']}")
        print(f"Confidence: {result['confidence']}%")

        if result["categories"]:

            print("\nDetected Categories:")

            for category in result["categories"]:

                print(
                    f"• {category['category']} ({category['confidence']}%)"
                )

        else:

            print("\nNo hate speech detected.")

        print()