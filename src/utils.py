import os
import base64
import unicodedata
from PIL import Image, ImageDraw, ImageFont

def remove_accents(input_str: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def create_pillow_fallback(name: str, emoji: str, category: str) -> str:
    os.makedirs("assets", exist_ok=True)
    
    color_map = {
        "noodles": ((255, 230, 204), (255, 179, 102)),
        "rice": ((230, 242, 255), (153, 204, 255)),
        "soup": ((255, 204, 204), (255, 102, 102)),
        "hotpot": ((255, 230, 230), (255, 51, 51)),
        "fast_food": ((255, 255, 204), (255, 204, 0)),
        "dessert": ((255, 204, 255), (255, 102, 204)),
        "vegetarian": ((230, 255, 230), (102, 255, 102)),
        "snack": ((242, 242, 242), (204, 204, 204)),
        "default": ((249, 232, 203), (249, 168, 38))
    }
    colors = color_map.get(category, color_map["default"])
    
    width, height = 800, 450
    img = Image.new('RGB', (width, height), color=colors[0])
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * y / height)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * y / height)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf"
    ]
    font = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, 48)
                break
            except Exception:
                pass
    if not font:
        font = ImageFont.load_default()

    display_text = remove_accents(name)
    draw.text((width//2, height//2), display_text, font=font, fill=(40, 40, 40), anchor="mm")
    
    filename = f"assets/fallback_{category}_{abs(hash(name))}.jpg"
    img.save(filename, format="JPEG")
    return filename

def image_to_base64(img_path: str) -> str:
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
