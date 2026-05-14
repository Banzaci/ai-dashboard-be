import spacy

import os
print("CWD:", os.getcwd())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model-best")

nlp = spacy.load(MODEL_PATH)


def predict(text: str):
    doc = nlp(text)

    intent_scores = doc.cats

    best_intent = ""
    best_score = -1.0

    for k, v in intent_scores.items():
        if v > best_score:
            best_score = v
            best_intent = k

    # safety fallback
    if best_intent == "":
        best_intent = "unknown"

    entities = [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
    ]

    return {
        "intent": best_intent,
        "confidence": best_score,
        "entities": entities
    }


if __name__ == "__main__":
    text = "1 room for 2 people from 1st June for 3 nights"
    print(predict(text))