import pytest
from unittest.mock import patch, MagicMock
from src.weather_service import fetch_weather_data, get_fallback_weather, process_weather_data

@patch('src.weather_service.requests.get')
def test_fetch_weather_data_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"current": {"temperature_2m": 30}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    
    data = fetch_weather_data()
    assert data["temperature_2m"] == 30

@patch('src.weather_service.requests.get')
def test_fetch_weather_data_timeout(mock_get):
    mock_get.side_effect = Exception("Timeout")
    data = fetch_weather_data()
    assert data is None

def test_process_weather_data_hot():
    data = {"temperature_2m": 36, "rain": 0, "precipitation": 0, "relative_humidity_2m": 50, "wind_speed_10m": 5}
    result = process_weather_data(data)
    assert "very_hot" in result["tags"]
    assert "normal" not in result["tags"]

def test_process_weather_data_fallback():
    result = process_weather_data(None)
    assert "temp" in result
    assert isinstance(result["tags"], list)
