def conll_to_spacy(filepath):
    sentences = []
    sentence = []
    labels = []

    # Label mapping
    label_map = {
        "PER": "PERSON",
        "LOC": "LOCATION",
        "ORG": "ORG",
        "MISC": "MISC"
    }

    # -------- STEP 1: READ FILE --------
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line == "" or line.startswith("-DOCSTART-"):
                if sentence:
                    sentences.append((sentence, labels))
                    sentence = []
                    labels = []
                continue

            parts = line.split()
            if len(parts) < 2:
                continue

            word = parts[0]
            tag = parts[-1]

            sentence.append(word)
            labels.append(tag)

    # -------- STEP 2: CONVERT --------
    spacy_data = []

    for words, tags in sentences:
        text = " ".join(words)
        entities = []

        i = 0
        char_pos = 0  # keeps track of correct position

        while i < len(words):
            word = words[i]
            tag = tags[i]

            start = char_pos
            end = start + len(word)

            if tag.startswith("B-"):
                label = label_map.get(tag[2:], tag[2:])
                ent_start = start
                ent_end = end

                i += 1
                char_pos = end + 1  # move after space

                # handle I- tags
                while (
                    i < len(tags)
                    and tags[i].startswith("I-")
                    and tags[i][2:] == tag[2:]
                ):
                    next_word = words[i]
                    ent_end = char_pos + len(next_word)

                    char_pos = ent_end + 1
                    i += 1

                entities.append((ent_start, ent_end, label))

            else:
                i += 1
                char_pos = end + 1

        spacy_data.append((text, {"entities": entities}))

    return spacy_data


# 🔥 RUN
data = conll_to_spacy("train.txt")

# ✅ Check first 5 samples
for i in range(5):
    print(data[i])

# 💾 Save JSON
import json
with open("spacy_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("\n✅ Conversion completed and saved to spacy_data.json")