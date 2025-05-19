from PIL import Image, ImageDraw, ImageFont
import io

def generate_bhava_card(name: str, tags: list):
    width = 720
    height = 120 * len(tags) + 100
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_body = ImageFont.truetype("arial.ttf", 24)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
    draw.text((20, 20), f"Bhāva Profile: {name}", fill="black", font=font_title)
    y = 80
    for bhava, chakra, rasa, color in tags:
        draw.rectangle([(20, y), (width - 20, y + 80)], fill=color)
        draw.text((40, y + 25), f"{chakra} • {bhava} • {rasa}", fill="white", font=font_body)
        y += 100
    return img

def get_card_png_bytes(name: str, tags: list):
    img = generate_bhava_card(name, tags)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
