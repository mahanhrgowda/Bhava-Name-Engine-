
import streamlit as st

CHAKRA_DISPLAY_NAMES = {
    "Mūlādhāra": "🔴 Mūlādhāra – Grounding",
    "Svādhiṣṭhāna": "🟠 Svādhiṣṭhāna – Emotions",
    "Maṇipūra": "🟡 Maṇipūra – Power",
    "Anāhata": "💚 Anāhata – Love",
    "Viśuddha": "🔵 Viśuddha – Expression",
    "Ājñā": "🟣 Ājñā – Intuition",
    "Sahasrāra": "🕉️ Sahasrāra – Divine",
    "All": "🌈 All – Universal"
}

CHAKRA_REVERSE_MAP = {v: k for k, v in CHAKRA_DISPLAY_NAMES.items()}

RASA_DISPLAY_NAMES = {
    "Śṛṅgāra (Beauty)": "💖 Śṛṅgāra – Beauty",
    "Vīra (Courage)": "🔥 Vīra – Heroism",
    "Karuṇā (Compassion)": "😢 Karuṇā – Compassion",
    "Hāsya (Joy)": "😂 Hāsya – Laughter",
    "Adbhuta (Wonder)": "✨ Adbhuta – Awe",
    "Raudra (Anger)": "⚡ Raudra – Rage",
    "Bībhatsa (Disgust)": "🤢 Bībhatsa – Aversion",
    "Bhayānaka (Fear)": "😱 Bhayānaka – Terror",
    "Śānta (Calm)": "🕊️ Śānta – Peace",
    "Śānta (Tranquility)": "🧘 Śānta – Stillness",
    "Vīra (Justice)": "⚖️ Vīra – Justice"
}

RASA_REVERSE_MAP = {v: k for k, v in RASA_DISPLAY_NAMES.items()}

def chakra_filter_ui():
    selected_display = st.sidebar.multiselect(
        "🧘 Select Chakras (with function hint):",
        list(CHAKRA_DISPLAY_NAMES.values()),
        default=list(CHAKRA_DISPLAY_NAMES.values())
    )
    return [CHAKRA_REVERSE_MAP[label] for label in selected_display]

def rasa_filter_ui():
    selected_display = st.sidebar.multiselect(
        "🎭 Select Rasas (with essence hint):",
        list(RASA_DISPLAY_NAMES.values()),
        default=list(RASA_DISPLAY_NAMES.values())
    )
    return [RASA_REVERSE_MAP[label] for label in selected_display]
