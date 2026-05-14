import spacy
from spacy.tokens import DocBin
import json

# -----------------------
# LOAD BLANK MODEL
# -----------------------
nlp = spacy.blank("en")

# -----------------------
# LOAD RAW DATA
# -----------------------
with open("data/raw.jsonl", "r") as f:
    raw_data = [json.loads(line) for line in f]

# -----------------------
# CREATE DOCBIN (training format)
# -----------------------
doc_bin = DocBin()

for item in raw_data:
    doc = nlp.make_doc(item["text"])

    spans = []

    for ent in item.get("entities", []):
        span = doc.char_span(ent["start"], ent["end"], label=ent["label"])
        if span:
            spans.append(span)

    doc.ents = spans

    # 🔥 THIS IS WHAT YOU MISSED
    doc.cats = {item["intent"]: 1.0}

    doc_bin.add(doc)

# -----------------------
# SAVE TRAINING FILE
# -----------------------
doc_bin.to_disk("data/train.spacy")

print("✔ train.spacy created successfully")