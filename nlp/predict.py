import spacy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model-best")

nlp = spacy.load(MODEL_PATH)

INTENT_THRESHOLD = 0.6


def predict(text: str):

    if not text:
        return {"intent": "unknown", "confidence": 0.0, "entities": []}

    doc = nlp(text)

    best_intent, best_score = max(
        doc.cats.items(),
        key=lambda x: x[1],
        default=("unknown", 0.0)
    )

    if best_score < INTENT_THRESHOLD:
        best_intent = "unknown"

    return {
        "intent": best_intent,
        "confidence": float(best_score),
        "entities": [
            {"text": e.text, "label": e.label_}
            for e in doc.ents
        ]
    }