import streamlit as st
import spacy

# Load model (same as your test.py)
@st.cache_resource
def load_model():
    return spacy.load("output/model-last")

nlp = load_model()

st.title("🧠 Named Entity Recognition (NER) Demo")

# Input text
text = st.text_area(
    "Enter your text:",
    "Barack Obama visited Germany last week and met officials from the European Union in Berlin."
)

# Analyze button
if st.button("Analyze"):
    doc = nlp(text)

    st.subheader("📌 Extracted Entities")

    if doc.ents:
        for ent in doc.ents:
            st.write(f"**{ent.text}** → {ent.label_}")
    else:
        st.write("No entities found.")

    # ---- Highlighted Output ----
    st.subheader("🎨 Highlighted Text")

    colors = {
        "PERSON": "#ffd54f",
        "ORG": "#81c784",
        "GPE": "#64b5f6",
        "LOC": "#9eb8c4"
    }

    highlighted_text = text

    for ent in doc.ents:
        color = colors.get(ent.label_, "#e0e0e0")

        highlighted_text = highlighted_text.replace(
            ent.text,
            f"<span style='background-color:{color}; padding:2px; border-radius:4px'>"
            f"{ent.text} ({ent.label_})</span>"
        )

    st.markdown(highlighted_text, unsafe_allow_html=True)