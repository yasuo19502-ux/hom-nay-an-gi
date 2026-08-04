import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
from src.image_service import search_pexels, get_dish_image

@patch('src.image_service.requests.get')
def test_search_pexels_success(mock_get):
    # Ensure config is mocked to have API key
    with patch('src.image_service.Config.PEXELS_API_KEY', 'fake_key'):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "photos": [
                {"src": {"large2x": "url1"}, "photographer": "A", "photographer_url": "urlA", "url": "pageA", "alt": "food1", "width": 100, "height": 100},
                {"src": {"large2x": "url2"}, "photographer": "B", "photographer_url": "urlB", "url": "pageB", "alt": "food2", "width": 100, "height": 100}
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = search_pexels(["query"])
        assert result is not None
        assert result["src"]["large2x"] in ["url1", "url2"]

@patch('src.image_service.requests.get')
def test_search_pexels_timeout(mock_get):
    with patch('src.image_service.Config.PEXELS_API_KEY', 'fake_key'):
        mock_get.side_effect = Exception("Timeout")
        result = search_pexels(["query"])
        assert result is None

@patch('src.image_service.search_pexels')
def test_get_dish_image_fallback(mock_search):
    # Mock no result from pexels
    mock_search.return_value = None
    
    # Needs session state setup
    if not hasattr(st, "session_state"):
        st.session_state = {}
        
    result = get_dish_image("dish1", "Pho", "🍜", "noodles", ["pho"])
    assert result.source == "local"
    assert "fallback" in result.image_url
    assert "dish1" in st.session_state.image_cache
