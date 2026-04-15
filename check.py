import spacy
from spacy.tokens import DocBin

doc_bin = DocBin().from_disk("train.spacy")
docs = list(doc_bin.get_docs(spacy.blank("en").vocab))

count = 0
for doc in docs:
    if doc.ents:
        count += 1

print("Total docs:", len(docs))
print("Docs with entities:", count)