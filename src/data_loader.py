import json
import streamlit as st
from typing import List, Dict
from src.models import Dish
from src.config import Config

@st.cache_data
def load_dishes() -> List[Dish]:
    try:
        with open(Config.DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Dish(**item) for item in data]
    except Exception as e:
        st.error(f"Error loading dishes: {e}")
        return []

@st.cache_data
def get_categories(dishes: List[Dish]) -> List[str]:
    return sorted(list(set(d.category for d in dishes)))

@st.cache_data
def get_all_tags(dishes: List[Dish]) -> List[str]:
    tags = set()
    for d in dishes:
        tags.update(d.tags)
    return sorted(list(tags))
