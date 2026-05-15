import spacy
from spacy.tokens import DocBin
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

nlp = spacy.blank("en")

df = pd.read_json("./data/raw.jsonl", lines=True)

doc_bin = DocBin()

for _, row in df.iterrows():

    doc = nlp.make_doc(row["text"])

    spans = []

    for ent in row.get("entities", []):

        span = doc.char_span(
            ent["start"],
            ent["end"],
            label=ent["label"]
        )

        if span is None:
            logging.warning(f"Bad span skipped: {ent}")
            continue

        spans.append(span)

    doc.ents = spans

    doc.cats = {
        row["intent"]: 1.0
    }

    doc_bin.add(doc)

doc_bin.to_disk("./data/train.spacy")

print("✔ dataset built")