from phoneme_bhava_map import PHONEME_BHAVA_MAP
from syllable_parser import parse_syllables

def guess_bhava_tags(name: str):
    syllables = parse_syllables(name)
    matched = [PHONEME_BHAVA_MAP[s] for s in syllables if s in PHONEME_BHAVA_MAP]
    guessed = [guess_phoneme(s) for s in syllables if s not in PHONEME_BHAVA_MAP]
    guessed = [g for g in guessed if g]
    return list(set(matched + guessed))

def guess_phoneme(syll: str):
    for key in PHONEME_BHAVA_MAP:
        if syll in key or key in syll or syll[0] == key[0]:
            return PHONEME_BHAVA_MAP[key]
    return None
