import pandas as pd
from bhava_guesser import guess_bhava_tags

def process_name(name: str):
    tags = guess_bhava_tags(name)
    if not tags:
        return ("", "", "", "")
    bhavas, chakras, rasas, colors = zip(*tags)
    return (
        ", ".join(sorted(set(bhavas))),
        ", ".join(sorted(set(chakras))),
        ", ".join(sorted(set(rasas))),
        ", ".join(sorted(set(colors)))
    )

def process_csv(input_csv: str):
    df = pd.read_csv(input_csv)
    output_data = []
    for _, row in df.iterrows():
        name = str(row['Name'])
        bhava, chakra, rasa, color = process_name(name)
        output_data.append({
            "Name": name,
            "Bhāva Tags": bhava,
            "Chakras": chakra,
            "Rasa": rasa,
            "Colors": color
        })
    return pd.DataFrame(output_data)
