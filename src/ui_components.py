import streamlit as st
import datetime
import os
from src.models import Dish
from src.image_service import get_dish_image
from src.gemini_service import get_dish_copy
from src.weather_service import get_current_weather_context
from src.utils import image_to_base64

def load_css():
    css_file = "assets/styles.css"
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_header():
    load_css()
    
    hour = datetime.datetime.now().hour
    subline = "Hôm nay mình xứng đáng ăn ngon."
    if 5 <= hour < 10:
        subline = "Dậy rồi thì ăn gì cho tỉnh?"
    elif 10 <= hour < 14:
        subline = "Đến giờ giải quyết chiếc bụng rồi."
    elif 14 <= hour < 17:
        subline = "Hơi buồn miệng hay buồn thật?"
    elif 17 <= hour < 21:
        subline = "Hôm nay mình xứng đáng ăn ngon."
    else:
        subline = "Giờ này còn ở đây thì chắc chắn là đói."

    weather_ctx = get_current_weather_context()
    
    header_html = f"""<div style="text-align: center; margin-bottom: 30px;">
<h1 style="color: var(--primary); margin-bottom: 4px; font-size: 32px; font-weight: 800;">ĂN GÌ ĐÂY? 🥢</h1>
<p style="color: var(--text-muted); font-size: 16px; margin-top: 0; font-weight: 500;">{subline}</p>
<div class="weather-pill">🌦 Hà Nội · {weather_ctx['temp']}°C · {weather_ctx['description'].split(',')[1].split('.')[0].strip() if ',' in weather_ctx['description'] else 'Dễ chịu'}</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)

def render_dish_card(dish: Dish, current_mood: str):
    weather_ctx = get_current_weather_context()
    copy_data = get_dish_copy(dish, weather_ctx['tags'], current_mood)
    
    image_result = get_dish_image(dish.id, dish.name, dish.emoji, dish.fallback_image_category, dish.pexels_queries)
    img_url = image_result.image_url
    
    if not img_url.startswith("http"):
        base64_img = image_to_base64(img_url)
        img_url = f"data:image/jpeg;base64,{base64_img}"
        
    badges_html = ""
    badges_count = 0
    if "Lạnh" in dish.weather_tags or "Mưa" in dish.weather_tags:
        badges_html += "<span class='badge'>Hợp trời mưa lạnh</span>"
        badges_count += 1
    if dish.price_max <= 60000 and badges_count < 3:
        badges_html += "<span class='badge'>Dưới 60K</span>"
        badges_count += 1
    if dish.hanoi_relevance_score > 7 and badges_count < 3:
        badges_html += "<span class='badge'>Chuẩn Hà Nội</span>"

    chips_html = f"""<span class="chip">💰 {dish.price_min//1000}K - {dish.price_max//1000}K</span><span class="chip">🌶️ Cấp độ {dish.spice_level}</span><span class="chip">⭐ {dish.popularity_score}/10</span>"""

    credit_html = ""
    if image_result.source == "pexels":
        credit_html = f"""<div style='text-align: right; padding: 8px 24px 0; font-size: 11px; color: var(--text-muted);'>Ảnh: <a href='{image_result.photographer_url}' target='_blank' style='color: var(--text-muted); text-decoration: underline;'>{image_result.photographer_name}</a> · <a href='{image_result.pexels_page_url}' target='_blank' style='color: var(--text-muted); text-decoration: underline;'>Pexels</a></div>"""

    card_html = f"""<div class="custom-card">
<div class="dish-image-wrapper">
<img src="{img_url}" alt="{image_result.alt_text}" />
<div class="dish-image-overlay"></div>
<div class="dish-badges">{badges_html}</div>
</div>
{credit_html}
<div class="card-padding">
<h2 style="margin-top: 0; margin-bottom: 8px; font-size: 28px; color: var(--text-dark);">{dish.name}</h2>
<h4 style="margin-top: 0; margin-bottom: 12px; font-size: 18px; color: var(--primary); line-height: 1.4;">"{copy_data.get('headline', '')}"</h4>
<div style="margin-bottom: 20px;">{chips_html}</div>
<p style="color: var(--text-muted); font-size: 15px; margin-bottom: 16px; line-height: 1.5;">{dish.description}</p>
<div style="background-color: var(--bg-cream); padding: 16px; border-radius: 16px; border: 1px dashed var(--border-light);">
<p style="margin: 0; color: var(--text-dark); font-size: 14px;"><strong>Lý do app chọn món này:</strong> {copy_data.get('reason', '')}</p>
</div>
</div>
</div>"""
    st.markdown(card_html, unsafe_allow_html=True)
