import spacy

nlp = spacy.load("output/model-best")

print("Pipeline:", nlp.pipe_names)

text = "Barack Obama visited Germany last week and met officials from the European Union in Berlin. During the meeting, representatives from Google and Microsoft also discussed new technology policies. Meanwhile, Indian Prime Minister Narendra Modi held talks with French President Emmanuel Macron in Paris regarding climate change agreements."
doc = nlp(text)

print("TEXT:", text)
print("Entities:", doc.ents)

for ent in doc.ents:
    print(ent.text, ent.label_)