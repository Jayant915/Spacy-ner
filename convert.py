import spacy
from spacy.tokens import DocBin
import json

# Load JSON
with open("spacy_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

nlp = spacy.blank("en")
doc_bin = DocBin()

for text, annot in data:
    doc = nlp.make_doc(text)
    ents = []
    seen_tokens = set()

    for start, end, label in annot["entities"]:
        span = doc.char_span(start, end, label=label, alignment_mode="expand")

        if span is None:
            continue

        # Check overlap
        overlap = False
        for token in span:
            if token.i in seen_tokens:
                overlap = True
                break

        if overlap:
            continue

        for token in span:
            seen_tokens.add(token.i)

        ents.append(span)

    # Assign entities AFTER loop
    doc.ents = ents
    doc_bin.add(doc)

doc_bin.to_disk("train.spacy")

print("✅ Converted to train.spacy")