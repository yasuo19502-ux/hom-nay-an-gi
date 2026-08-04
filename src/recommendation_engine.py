import random
from typing import List, Tuple
from datetime import datetime
from src.models import Dish, FilterCriteria

def determine_meal_period_by_hour(hour: int) -> str:
    if 5 <= hour < 10:
        return "Sáng"
    elif 10 <= hour < 14:
        return "Trưa"
    elif 14 <= hour < 17:
        return "Xế"
    elif 17 <= hour < 21:
        return "Tối"
    else:
        return "Đêm"

def filter_dishes_step_a(dishes: List[Dish], criteria: FilterCriteria) -> List[Dish]:
    filtered = []
    
    current_hour = datetime.now().hour
    auto_meal = determine_meal_period_by_hour(current_hour)
    target_meal = auto_meal if criteria.meal_period == "Tự động" else criteria.meal_period

    for d in dishes:
        # Meal filter
        if target_meal not in d.meal_periods:
            continue
            
        # Budget filter
        if criteria.budget != "Không quan trọng":
            if criteria.budget == "Dưới 30.000 đồng" and d.price_min >= 30000:
                continue
            elif criteria.budget == "30.000–60.000 đồng" and (d.price_min > 60000 or d.price_max < 30000):
                continue
            elif criteria.budget == "60.000–120.000 đồng" and (d.price_min > 120000 or d.price_max < 60000):
                continue
            elif criteria.budget == "Trên 120.000 đồng" and d.price_max <= 120000:
                continue
                
        # Vegetarian
        if criteria.vegetarian and "Chay" not in d.diet_tags:
            continue
            
        # Avoid ingredients
        if criteria.avoid_ingredients:
            if any(avoid in d.main_ingredients for avoid in criteria.avoid_ingredients):
                continue
                
        # Spice level
        spice_map = {"Không cay": 0, "Cay nhẹ": 1, "Cay vừa": 2, "Càng cay càng tốt": 3}
        if criteria.spice_level != "Không quan trọng":
            max_spice = spice_map.get(criteria.spice_level, 3)
            if d.spice_level > max_spice:
                continue
                
        filtered.append(d)
        
    return filtered

def score_dishes_step_b(filtered_dishes: List[Dish], criteria: FilterCriteria, weather: str = "Nắng", temperature: str = "Vừa") -> List[Tuple[str, float]]:
    scored = []
    for d in filtered_dishes:
        score = 0.0
        
        # Weather and temp
        if weather in d.weather_tags:
            score += 2.0
        if temperature in d.temperature_tags:
            score += 2.0
            
        # Mood
        if criteria.mood != "Không biết, app tự chọn":
            if criteria.mood in d.mood_tags:
                score += 3.0
                
        # Popularity & Hanoi relevance
        score += d.popularity_score * 0.2
        score += d.hanoi_relevance_score * 0.3
        
        # Random noise to make it less robotic
        score += random.uniform(0, 2.0)
        
        scored.append((d.id, score))
        
    # Sort descending
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored

def get_ranked_candidates(dishes: List[Dish], criteria: FilterCriteria) -> List[str]:
    # Hard filter
    candidates = filter_dishes_step_a(dishes, criteria)
    if not candidates:
        return []
        
    # Scored filter
    # For now assume static weather/temp for scoring
    scored = score_dishes_step_b(candidates, criteria, "Nắng", "Vừa")
    return [s[0] for s in scored]

def get_next_dish(remaining_ids: List[str]) -> str:
    if not remaining_ids:
        return None
    return remaining_ids[0]
