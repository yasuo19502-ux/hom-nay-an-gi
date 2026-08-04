import pytest
from unittest.mock import patch, MagicMock
from src.gemini_service import generate_fun_copy

@patch('src.gemini_service.genai.Client')
def test_generate_fun_copy_success(mock_client_class):
    with patch('src.gemini_service.Config.GEMINI_API_KEY', 'fake_key'):
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"headline": "H1", "reason": "R1", "share_text": "S1"}'
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        res = generate_fun_copy("dish1", "Pho", "Trưa", ("Nắng",), "Vui")
        assert res["headline"] == "H1"
        assert res["share_text"] == "S1"

@patch('src.gemini_service.genai.Client')
def test_generate_fun_copy_timeout_or_error(mock_client_class):
    with patch('src.gemini_service.Config.GEMINI_API_KEY', 'fake_key'):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("Timeout")
        mock_client_class.return_value = mock_client
        
        res = generate_fun_copy("dish1", "Pho", "Trưa", ("Nắng",), "Vui")
        # Should fallback
        assert "headline" in res
        assert "Pho" in res["headline"] or "Pho" in res["reason"] or "Pho" in res["share_text"]

def test_generate_fun_copy_no_key():
    with patch('src.gemini_service.Config.GEMINI_API_KEY', None):
        res = generate_fun_copy("dish1", "Pho", "Trưa", ("Nắng",), "Vui")
        assert "Pho" in res["headline"] or "Pho" in res["reason"] or "Pho" in res["share_text"]
