import os
from PIL import Image, ImageDraw, ImageFont
import base64
from io import BytesIO

def create_pillow_fallback(name: str, emoji: str, category: str) -> str:
    # Ensure assets dir exists
    os.makedirs("assets", exist_ok=True)
    
    # Simple color map based on category
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
    
    # Draw simple gradient
    for y in range(height):
        r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * y / height)
        g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * y / height)
        b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Try to load a font, otherwise use default
    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 80)
        font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 40)
    except Exception:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw text
    draw.text((width//2, height//2 - 50), emoji, font=font_large, fill=(50, 50, 50), anchor="mm")
    draw.text((width//2, height//2 + 50), name, font=font_small, fill=(50, 50, 50), anchor="mm")
    
    filename = f"assets/fallback_{category}_{hash(name)}.jpg"
    img.save(filename, format="JPEG")
    return filename

def image_to_base64(img_path: str) -> str:
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
