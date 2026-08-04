import os
import streamlit as st

class Config:
    try:
        PEXELS_API_KEY = st.secrets.get("PEXELS_API_KEY", os.getenv("PEXELS_API_KEY"))
    except Exception:
        PEXELS_API_KEY = None

    try:
        GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    except Exception:
        GEMINI_API_KEY = None

    try:
        GEMINI_MODEL = st.secrets.get("GEMINI_MODEL", os.getenv("GEMINI_MODEL", "gemini-2.5-flash"))
    except Exception:
        GEMINI_MODEL = "gemini-2.5-flash"

    DATA_FILE = "data/dishes.json"
    FALLBACK_IMAGE = "assets/fallback_food.jpg"
    REQUEST_TIMEOUT = 5
