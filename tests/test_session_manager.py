import pytest
import streamlit as st
from unittest.mock import patch
from src.session_manager import init_session, reset_session, proceed_to_discovery, reject_current_dish, go_back_to_previous, check_and_reset_filters, set_current_dish, retry_rejected_dishes

@pytest.fixture(autouse=True)
def setup_streamlit_state():
    st.session_state.clear()
    init_session()
    yield

def test_session_init():
    assert st.session_state.app_stage == "SETUP"
    assert len(st.session_state.remaining_ids) == 0

def test_dish_not_repeated_after_reject():
    proceed_to_discovery(["1", "2", "3"])
    set_current_dish("1")
    assert st.session_state.current_dish_id == "1"
    
    # Reject it
    reject_current_dish()
    assert st.session_state.current_dish_id is None
    assert "1" in st.session_state.rejected_ids
    assert "1" not in st.session_state.remaining_ids
    assert "1" in st.session_state.previous_dish_ids
    
    # Try next
    set_current_dish("2")
    assert st.session_state.current_dish_id == "2"

def test_go_back_to_previous():
    proceed_to_discovery(["1", "2", "3"])
    set_current_dish("1")
    reject_current_dish()
    
    set_current_dish("2")
    
    # User clicks go back
    go_back_to_previous()
    assert st.session_state.current_dish_id == "1"
    assert st.session_state.remaining_ids[0] == "2" # 2 goes back to remaining
    
def test_reset_when_filter_changes():
    # Sig 1
    assert check_and_reset_filters("sig_1") == True
    proceed_to_discovery(["1", "2"])
    
    # Sig 1 again
    assert check_and_reset_filters("sig_1") == False
    assert len(st.session_state.candidate_ids) == 2
    
    # Sig 2
    assert check_and_reset_filters("sig_2") == True
    assert len(st.session_state.candidate_ids) == 0

def test_end_of_queue():
    proceed_to_discovery(["1"])
    set_current_dish("1")
    reject_current_dish()
    
    assert len(st.session_state.remaining_ids) == 0
    # No more remaining

def test_retry_rejected_dishes():
    proceed_to_discovery(["1", "2"])
    set_current_dish("1")
    reject_current_dish()
    
    set_current_dish("2")
    reject_current_dish()
    
    assert len(st.session_state.remaining_ids) == 0
    assert "1" in st.session_state.rejected_ids
    
    retry_rejected_dishes()
    assert len(st.session_state.remaining_ids) == 2
    assert len(st.session_state.rejected_ids) == 0
