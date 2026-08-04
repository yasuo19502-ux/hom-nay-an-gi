import sys
from unittest.mock import MagicMock

# Create a mock streamlit module
mock_st = MagicMock()

# Specifically mock session_state as a dict-like object
class SessionState(dict):
    def __getattr__(self, item):
        if item in self:
            return self[item]
        raise AttributeError
        
    def __setattr__(self, key, value):
        self[key] = value

mock_st.session_state = SessionState()
def mock_cache_data(*args, **kwargs):
    if len(args) == 1 and callable(args[0]) and not kwargs:
        return args[0]
    return lambda f: f

mock_st.cache_data = mock_cache_data

# Replace the module in sys.modules
sys.modules["streamlit"] = mock_st
