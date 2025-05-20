
import streamlit as st

def get_selected_filters():
    all_chakras = ["Muladhara", "Svadhisthana", "Manipura", "Anahata", "Vishuddha", "Ajna", "Sahasrara"]
    all_rasas = ["Śṛṅgāra", "Vīra", "Karuṇa", "Raudra", "Hāsya", "Bhayānaka", "Bībhatsa", "Adbhuta", "Śānta"]

    selected_chakras = st.sidebar.multiselect("Select Chakras", all_chakras, default=all_chakras)
    selected_rasas = st.sidebar.multiselect("Select Rasas", all_rasas, default=all_rasas)
    return selected_chakras, selected_rasas
