import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from io import BytesIO
from fuzzywuzzy import fuzz
from bhava_guesser import guess_bhava_tags
from bhava_card_export import get_card_png_bytes
from bhava_csv_batch_processor import process_csv
from chakra_bhava_deity_mantra_map import get_chakra_deity_map

st.set_page_config(page_title="Bhāva Name Engine", page_icon="🕉", layout="centered")

@st.cache_data
def load_glossary():
    with open("bhava_glossary_full.json", "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    return {
        k: v for k, v in raw_data.items()
        if isinstance(v, dict) and all(x in v for x in ["chakra", "rasa", "meaning"])
    }

def is_fuzzy_match(query, target, threshold=60):
    if not query or not target:
        return False
    return fuzz.partial_ratio(query.lower(), target.lower()) >= threshold

def generate_chakra_sparkline(bhava_entries):
    chakra_counts = {}
    for bhava, data in bhava_entries:
        chakra = data["chakra"]
        chakra_counts[chakra] = chakra_counts.get(chakra, 0) + 1

    chakras_ordered = ["Mūlādhāra", "Svādhiṣṭhāna", "Maṇipūra", "Anāhata", "Viśuddha", "Ājñā", "Sahasrāra"]
    counts = [chakra_counts.get(c, 0) for c in chakras_ordered]

    fig, ax = plt.subplots(figsize=(6, 1.5))
    ax.bar(chakras_ordered, counts, color='skyblue')
    ax.set_xticklabels(chakras_ordered, rotation=45, ha='right')
    ax.set_yticks([])
    ax.set_title("Bhāva Distribution by Chakra", fontsize=10)

    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

glossary = load_glossary()
all_chakras = sorted(list({v["chakra"] for v in glossary.values()}))
all_rasas = sorted(list({v["rasa"] for v in glossary.values()}))
all_bhavas = sorted(glossary.keys())

# Sidebar Filters
st.sidebar.title("🔍 Glossary Filters")
selected_chakras = st.sidebar.multiselect("Select Chakra(s)", all_chakras, default=[])
selected_rasas = st.sidebar.multiselect("Select Rasa(s)", all_rasas, default=[])
selected_bhavas = st.sidebar.multiselect("Select Bhāva(s)", all_bhavas, default=[])
name_query = st.sidebar.text_input("Search by Name")
filter_scripture_only = st.sidebar.checkbox("📖 Only Bhāvas with Scripture")
show_references = st.sidebar.checkbox("📿 Show Chakra–Deity–Mantra References")

st.title("🌸 Bhāva Name Engine")

tab1, tab2, tab3 = st.tabs(["🧑‍🎤 Single Name Tagger", "📁 Batch CSV Upload", "📚 Bhāva Glossary"])

with tab1:
    st.subheader("🔤 Enter a Name")
    name_input = st.text_input("Name:")
    if name_input:
        tags = guess_bhava_tags(name_input)
        if tags:
            st.success("✨ Bhāva Tags:")
            for bhava, chakra, rasa, color in tags:
                st.markdown(
                    f"<div style='padding:10px;margin:5px;border-radius:10px;background:{color};color:white;"
                    f"box-shadow: 0 0 12px {color}; font-size: 16px;'>"
                    f"<b>{chakra}</b> • {bhava} • <i>{rasa}</i></div>",
                    unsafe_allow_html=True
                )
            png_data = get_card_png_bytes(name_input, tags)
            st.download_button("📥 Download Bhāva Card (PNG)", data=png_data, file_name=f"{name_input}_bhava_card.png", mime="image/png")
        else:
            st.warning("No Bhāva tags could be confidently inferred.")

with tab2:
    st.subheader("📂 Upload CSV with Name Column")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        with st.spinner("Processing CSV..."):
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file.flush()
                df_out = process_csv(temp_file.name)
        st.success("✅ Bhāva Tags Processed")
        st.dataframe(df_out)
        csv = df_out.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Tagged CSV", data=csv, file_name="Bhava_Tagged_Names.csv", mime="text/csv")

with tab3:
    st.subheader("📚 Filtered Bhāva Glossary")
    filtered_results = [
        (bhava, data) for bhava, data in glossary.items()
        if (not selected_chakras or data["chakra"] in selected_chakras) and
           (not selected_rasas or data["rasa"] in selected_rasas) and
           (not selected_bhavas or bhava in selected_bhavas) and
           (not name_query or is_fuzzy_match(name_query, bhava)) and
           (not filter_scripture_only or ("scripture_quote" in data and data["scripture_quote"]))
    ]

    st.markdown(f"**{len(filtered_results)} results found**")
    sparkline_buf = generate_chakra_sparkline(filtered_results)
    st.image(sparkline_buf, use_container_width=True)

    for bhava, data in filtered_results:
        st.markdown(f\"\"\"
        ### 🪷 {bhava}
        - **Meaning**: {data["meaning"]}
        - **Chakra**: {data["chakra"]}
        - **Rasa**: {data["rasa"]}
        \"\"\")
        if "scripture_quote" in data:
            with st.expander("📖 View Scripture Details"):
                st.markdown(f"**Sanskrit:** {data['scripture_quote']}")
                st.markdown(f"**Translation:** {data['scripture_translation']}")
                st.markdown(f"**Source:** _{data['scripture_source']}_")
