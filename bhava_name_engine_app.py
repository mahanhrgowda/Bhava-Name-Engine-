
import streamlit as st
import json
from chakra_rasa_filters import get_selected_filters
from chakra_bhava_deity_mantra_map import get_chakra_deity_map
from fuzzywuzzy import fuzz

@st.cache_data
def load_glossary():
    with open("bhava_glossary_full.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return {
        k: v for k, v in raw_data.items()
        if isinstance(v, dict) and all(x in v for x in ["chakra", "rasa", "meaning"])
    }

glossary = load_glossary()

def is_fuzzy_match(query, target, threshold=60):
    if not query or not target:
        return False
    return fuzz.partial_ratio(query.lower(), target.lower()) >= threshold

st.sidebar.title("🔍 Filter Bhāvas")
selected_chakras, selected_rasas = get_selected_filters()
search_query = st.sidebar.text_input("Search Bhāva, Meaning, Chakra, or Rasa")

filtered_results = [
    (bhava, data) for bhava, data in glossary.items()
    if data["chakra"] in selected_chakras and
       data["rasa"] in selected_rasas and (
           is_fuzzy_match(search_query, bhava) or
           is_fuzzy_match(search_query, data["meaning"]) or
           is_fuzzy_match(search_query, data["chakra"]) or
           is_fuzzy_match(search_query, data["rasa"])
       )
]

st.title("🌸 Bhāva Name Engine Glossary")
st.markdown(f"**Results: {len(filtered_results)} matching entries**")

if not filtered_results:
    st.warning("No matching Bhāvas found.")
else:
    for bhava, data in filtered_results:
        st.markdown(f"""
        ### 🪷 {bhava}
        - **Meaning**: {data["meaning"]}
        - **Chakra**: {data["chakra"]}
        - **Rasa**: {data["rasa"]}
        """)

if st.checkbox("Show Chakra–Deity–Mantra References"):
    chakra_map = get_chakra_deity_map()
    for chakra, ref in chakra_map.items():
        st.markdown(f"""
        #### 🔘 {chakra}
        - **Deity**: {ref['deity']}
        - **Mantra**: `{ref['mantra']}`
        """)
