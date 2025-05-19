PHONEMES = sorted([
    'kha', 'gha', 'cha', 'jha', 'ṭha', 'ḍha', 'tha', 'dha', 'pha', 'bha',
    'ka', 'ga', 'ca', 'ja', 'ṭa', 'ḍa', 'ta', 'da', 'pa', 'ba',
    'ṅa', 'ña', 'ṇa', 'na', 'ma',
    'ya', 'ra', 'la', 'va',
    'śa', 'ṣa', 'sa', 'ha',
    'a', 'ā', 'i', 'ī', 'u', 'ū', 'e', 'ai', 'o', 'au', 'ṁ', 'ḥ'
], key=len, reverse=True)

def parse_syllables(name: str):
    name = name.lower().strip().replace('ṃ', 'ṁ')
    syllables = []
    while name:
        match = next((p for p in PHONEMES if name.startswith(p)), None)
        if match:
            syllables.append(match)
            name = name[len(match):]
        else:
            name = name[1:]
    return syllables
