
# 🌺 Bhāva Name Engine UI — Chakra–Rasa Glossary WebApp

A fully interactive **Streamlit WebApp** for exploring Sanskrit Bhāva archetypes by **Chakra** and **Rasa**, complete with deity mappings, mantras, emoji filters, sparkline analytics, and search highlighting.

![Chakra Sparkline](./chakra_bhava_sparkline.png)

## 📦 Features

- Emoji-based Chakra & Rasa filtering  
- Bhāva–Deity–Mantra–Scripture glossary  
- Chakra-colored search highlighting  
- Live fuzzy search with partial match tolerance  
- Sidebar sparkline chart (Bhāva trend by Chakra)  
- Chakra icon packs and animated fallback mandala  
- Downloadable CSV exports for filtered results  
- Modular backend + customizable UI components

## 🚀 How to Run

```bash
pip install -r requirements.txt
streamlit run bhava_glossary_app.py
```

## 📁 Structure

```
bhava_name_engine_ui/
├── bhava_glossary_app.py
├── chakra_rasa_filters.py
├── chakra_bhava_deity_mantra_map.py
├── bhava_glossary_full.json
├── chakra_icons/
├── chakra_bhava_sparkline.png
├── requirements.txt
└── README.md
```

MIT License | Created by Mahan Ravindra
