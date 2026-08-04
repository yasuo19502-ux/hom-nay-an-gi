import requests
import random
import streamlit as st
from typing import Dict, Any, List
from src.config import Config
from src.utils import create_pillow_fallback

class ImageResult:
    def __init__(self, image_url: str, photographer_name: str, photographer_url: str, pexels_page_url: str, alt_text: str, source: str, width: int, height: int):
        self.image_url = image_url
        self.photographer_name = photographer_name
        self.photographer_url = photographer_url
        self.pexels_page_url = pexels_page_url
        self.alt_text = alt_text
        self.source = source
        self.width = width
        self.height = height

@st.cache_data(ttl=86400, show_spinner=False)
def _fetch_pexels_cached(queries_tuple: tuple, api_key: str) -> Dict[str, Any]:
    headers = {"Authorization": api_key}
    for query in queries_tuple:
        url = f"https://api.pexels.com/v1/search?query={query}&per_page=15&orientation=landscape"
        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            data = res.json()
            photos = data.get("photos", [])
            if photos:
                return random.choice(photos[:3])
        except Exception:
            continue
    return None

def search_pexels(queries: List[str]) -> Dict[str, Any]:
    if not Config.PEXELS_API_KEY:
        return None
    return _fetch_pexels_cached(tuple(queries), Config.PEXELS_API_KEY)

def get_dish_image(dish_id: str, name: str, emoji: str, category: str, queries: List[str]) -> ImageResult:
    if "image_cache" not in st.session_state:
        st.session_state.image_cache = {}
        
    if dish_id in st.session_state.image_cache:
        cached = st.session_state.image_cache[dish_id]
        if cached.source == "pexels" or not Config.PEXELS_API_KEY:
            return cached
        
    photo = search_pexels(queries)
    if photo:
        result = ImageResult(
            image_url=photo["src"]["large2x"],
            photographer_name=photo["photographer"],
            photographer_url=photo["photographer_url"],
            pexels_page_url=photo["url"],
            alt_text=photo.get("alt", name),
            source="pexels",
            width=photo["width"],
            height=photo["height"]
        )
        st.session_state.image_cache[dish_id] = result
        return result
        
    fallback_path = create_pillow_fallback(name, emoji, category)
    result = ImageResult(
        image_url=fallback_path,
        photographer_name="System",
        photographer_url="",
        pexels_page_url="",
        alt_text=name,
        source="local",
        width=800,
        height=450
    )
    st.session_state.image_cache[dish_id] = result
    return result
