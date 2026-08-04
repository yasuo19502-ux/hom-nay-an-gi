import pytest
from src.data_loader import load_dishes

def test_all_dish_ids_are_unique():
    dishes = load_dishes()
    ids = [d.id for d in dishes]
    assert len(ids) == len(set(ids)), "Dish IDs must be unique"

def test_all_dishes_have_image_queries():
    dishes = load_dishes()
    for d in dishes:
        assert (len(d.pexels_queries) >= 3) or d.fallback_image_category, f"Dish {d.id} is missing image fallbacks or queries"

def test_data_validation():
    dishes = load_dishes()
    for d in dishes:
        assert d.name.strip() != "", f"Dish {d.id} has empty name"
        assert d.price_min <= d.price_max, f"Dish {d.id} has min_price > max_price"
        assert 0 <= d.spice_level <= 3, f"Dish {d.id} has invalid spice_level"
        assert 1 <= d.heaviness_level <= 5, f"Dish {d.id} has invalid heaviness_level"
        assert len(d.meal_periods) > 0, f"Dish {d.id} has no meal_period"
        assert len(d.food_types) > 0, f"Dish {d.id} has no food_type"
        assert d.map_search_query.strip() != "", f"Dish {d.id} has empty map_search_query"
