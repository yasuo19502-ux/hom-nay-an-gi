from pydantic import BaseModel
from typing import List, Optional

class Dish(BaseModel):
    id: str
    name: str
    short_name: str
    emoji: str
    description: str
    fun_fact: str
    meal_periods: List[str]
    weather_tags: List[str]
    temperature_tags: List[str]
    food_types: List[str]
    mood_tags: List[str]
    diet_tags: List[str]
    avoid_ingredients: List[str]
    main_ingredients: List[str]
    price_min: int
    price_max: int
    spice_level: int # 0=Không cay, 1=Cay nhẹ, 2=Cay vừa, 3=Rất cay
    heaviness_level: int # 1 to 5
    healthy_score: int # 1 to 10
    popularity_score: int # 1 to 10
    hanoi_relevance_score: int # 1 to 10
    pexels_queries: List[str]
    fallback_image_category: str
    map_search_query: str

class FilterCriteria(BaseModel):
    meal_period: str = "Tự động"
    budget: str = "Không quan trọng"
    mood: str = "Không biết, app tự chọn"
    spice_level: str = "Không quan trọng"
    vegetarian: bool = False
    avoid_ingredients: List[str] = []
    district: str = "Không quan trọng"
    
    def signature(self) -> str:
        av_str = "-".join(sorted(self.avoid_ingredients))
        return f"{self.meal_period}_{self.budget}_{self.mood}_{self.spice_level}_{self.vegetarian}_{av_str}_{self.district}"
