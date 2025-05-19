
import streamlit as st
import json
import re
import difflib
from chakra_rasa_filters import chakra_filter_ui, rasa_filter_ui
from chakra_bhava_deity_mantra_map import CHAKRA_BHAVA_DEITY_MANTRA_MAP

# Load Glossary
with open("bhava_glossary_full.json", "r", encoding="utf-8") as f:
    glossary = json.load(f)

# Chakra color definitions
CHAKRA_COLORS = {
    "Mūlādhāra": "#e74c3c", "Svādhiṣṭhāna": "#e67e22", "Maṇipūra": "#f1c40f",
    "Anāhata": "#2ecc71", "Viśuddha": "#3498db", "Ājñā": "#9b59b6",
    "Sahasrāra": "#8e44ad", "All": "#7f8c8d"
}

# Sidebar Filters
selected_chakras = chakra_filter_ui()
selected_rasas = rasa_filter_ui()
search_query = st.sidebar.text_input("🔎 Search Bhāvas (name, meaning, Chakra, or Rasa):").lower().strip()

# Matching Logic
def is_fuzzy_match(query, text, threshold=0.6):
    return difflib.SequenceMatcher(None, query.lower(), text.lower()).ratio() >= threshold

def highlight_text_colored(text, query, chakra=None):
    if not query:
        return text
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    color = CHAKRA_COLORS.get(chakra, "#fffd55")
    return pattern.sub(lambda m: f"<mark style='background: {color}; color: white; padding: 0 2px; border-radius: 3px'>{m.group(0)}</mark>", text)

# Filter glossary
filtered = {
    bhava: data for bhava, data in glossary.items()
    if data["chakra"] in selected_chakras and data["rasa"] in selected_rasas and (
        is_fuzzy_match(search_query, bhava) or
        is_fuzzy_match(search_query, data["meaning"]) or
        is_fuzzy_match(search_query, data["chakra"]) or
        is_fuzzy_match(search_query, data["rasa"])
    )
}

# Count and badge color
count = len(filtered)
if count == 0:
    badge_color = "#e74c3c"
elif len(selected_chakras) == 1:
    badge_color = CHAKRA_COLORS.get(selected_chakras[0], "#3498db")
elif count <= 3:
    badge_color = "#f1c40f"
else:
    badge_color = "#2ecc71"

st.markdown(f"<h4>📊 Filtered Bhāvas: <span style='background:{badge_color};padding:6px 14px;border-radius:20px;color:#fff;font-size:14px'>{count} match{'es' if count != 1 else ''}</span></h4>", unsafe_allow_html=True)
st.sidebar.image("chakra_bhava_sparkline.png", use_column_width=True)

# Display results
for bhava, data in filtered.items():
    chakra = data["chakra"]
    color = CHAKRA_COLORS.get(chakra, "#ccc")
    bhava_name = highlight_text_colored(bhava, search_query, chakra)
    chakra_name = highlight_text_colored(chakra, search_query, chakra)
    rasa_name = highlight_text_colored(data["rasa"], search_query, chakra)
    meaning = highlight_text_colored(data["meaning"], search_query, chakra)

    st.markdown(f'''
    <div style='margin-bottom:10px;padding:10px;background:#f9f9f9;border-left:5px solid {color};border-radius:8px'>
        <b>{bhava_name}</b><br>
        <i>Chakra:</i> {chakra_name}<br>
        <i>Rasa:</i> {rasa_name}<br>
        <i>Meaning:</i> {meaning}<br>
    </div>
    ''', unsafe_allow_html=True)
