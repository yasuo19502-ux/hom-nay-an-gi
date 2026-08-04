import requests
import streamlit as st
import datetime
from src.config import Config

HANOI_LAT = 21.0285
HANOI_LON = 105.8542

@st.cache_data(ttl=600, show_spinner=False)
def fetch_weather_data():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={HANOI_LAT}&longitude={HANOI_LON}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m&timezone=Asia%2FBangkok"
    headers = {"User-Agent": "HanoiFoodApp/1.0"}
    try:
        res = requests.get(url, headers=headers, timeout=8)
        res.raise_for_status()
        data = res.json()
        return data.get("current", {})
    except Exception as e:
        return None

def get_fallback_weather():
    now = datetime.datetime.now()
    month = now.month
    hour = now.hour
    
    # Simple heuristic for Hanoi
    temp = 25
    if 5 <= month <= 9:
        temp = 32 if 10 <= hour <= 16 else 28
    elif 11 <= month <= 2:
        temp = 16 if 20 <= hour <= 6 else 20
        
    return {
        "temperature_2m": temp,
        "apparent_temperature": temp,
        "precipitation": 0,
        "rain": 0,
        "weather_code": 0,
        "relative_humidity_2m": 70,
        "wind_speed_10m": 10
    }

def process_weather_data(current_data):
    if not current_data:
        current_data = get_fallback_weather()
        
    temp = current_data.get("temperature_2m", 25)
    rain = current_data.get("rain", 0)
    precip = current_data.get("precipitation", 0)
    humidity = current_data.get("relative_humidity_2m", 70)
    wind = current_data.get("wind_speed_10m", 0)
    
    tags = []
    
    if temp >= 35:
        tags.append("very_hot")
    elif temp >= 30:
        tags.append("hot")
    elif temp <= 15:
        tags.append("cold")
    elif temp <= 22:
        tags.append("cool")
    else:
        tags.append("normal")
        
    if rain > 0 or precip > 0:
        tags.append("rainy")
        
    if humidity >= 80:
        tags.append("humid")
    elif humidity <= 40:
        tags.append("dry")
        
    if wind >= 20:
        tags.append("windy")
        
    desc = generate_weather_description(temp, tags)
    return {"tags": tags, "description": desc, "temp": temp}

def generate_weather_description(temp, tags):
    if "rainy" in tags:
        return f"Ngoài trời đang mưa ({temp}°C), ăn món ấm nóng là chuẩn bài."
    elif "very_hot" in tags:
        return f"Hà Nội đang {temp}°C, nắng nóng gay gắt. Ưu tiên món mát mẻ nhé!"
    elif "hot" in tags:
        return f"Trời đang {temp}°C, hơi oi bức. Làm món gì dễ ăn thôi."
    elif "cold" in tags:
        return f"Trời rét {temp}°C thế này, thèm một bát nước dùng nóng hổi bốc khói."
    elif "cool" in tags:
        return f"Thời tiết {temp}°C siêu mát mẻ, ăn gì cũng thấy ngon."
    else:
        return f"Hà Nội đang {temp}°C, thời tiết dễ chịu. Lên kèo đi ăn thôi!"

@st.cache_data(ttl=600, show_spinner=False)
def get_current_weather_context():
    data = fetch_weather_data()
    return process_weather_data(data)
