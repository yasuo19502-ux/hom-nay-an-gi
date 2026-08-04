import streamlit as st
import time

def init_session():
    defaults = {
        "app_stage": "SETUP",
        "filter_signature": "",
        "candidate_ids": [],
        "remaining_ids": [],
        "rejected_ids": [],
        "viewed_history": [],
        "previous_dish_ids": [],
        "current_dish_id": None,
        "selected_dish_id": None,
        "image_cache": {},
        "gemini_copy_cache": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_session():
    st.session_state.app_stage = "SETUP"
    st.session_state.candidate_ids = []
    st.session_state.remaining_ids = []
    st.session_state.rejected_ids = []
    st.session_state.viewed_history = []
    st.session_state.previous_dish_ids = []
    st.session_state.current_dish_id = None
    st.session_state.selected_dish_id = None
    st.session_state.filter_signature = ""

def check_and_reset_filters(new_signature: str):
    if st.session_state.filter_signature != new_signature:
        st.session_state.candidate_ids = []
        st.session_state.remaining_ids = []
        st.session_state.rejected_ids = []
        st.session_state.viewed_history = []
        st.session_state.previous_dish_ids = []
        st.session_state.current_dish_id = None
        st.session_state.selected_dish_id = None
        st.session_state.filter_signature = new_signature
        return True
    return False

def proceed_to_discovery(candidate_ids):
    st.session_state.app_stage = "DISCOVERY"
    st.session_state.candidate_ids = candidate_ids
    st.session_state.remaining_ids = candidate_ids.copy()
    
    # We do not reset rejected_ids or previous_dish_ids if they just change stage without changing filters, 
    # but filters reset handles that. If they come back here without changing filters, we just keep state.
    # However, if candidate_ids changed, it's a new filter.
    
    # But we want to ensure remaining_ids only has items not rejected
    st.session_state.remaining_ids = [cid for cid in candidate_ids if cid not in st.session_state.rejected_ids]
    st.session_state.current_dish_id = None

def reject_current_dish():
    curr = st.session_state.current_dish_id
    if curr:
        if curr not in st.session_state.rejected_ids:
            st.session_state.rejected_ids.append(curr)
        if curr not in st.session_state.viewed_history:
            st.session_state.viewed_history.append(curr)
        
        st.session_state.previous_dish_ids.append(curr)
        
        if st.session_state.remaining_ids and st.session_state.remaining_ids[0] == curr:
            st.session_state.remaining_ids.pop(0)
            
        st.session_state.current_dish_id = None

def set_current_dish(dish_id):
    st.session_state.current_dish_id = dish_id

def go_back_to_previous():
    if st.session_state.previous_dish_ids:
        prev = st.session_state.previous_dish_ids.pop()
        
        if st.session_state.current_dish_id:
            # push current back to remaining so it's not lost
            st.session_state.remaining_ids.insert(0, st.session_state.current_dish_id)
            
        st.session_state.current_dish_id = prev
        # it was in rejected, we can optionally remove it if we want them to be able to accept it now
        # the spec says "Món bị từ chối không xuất hiện lại", but if they go back, they are explicitly revisiting it.
        # We will temporarily allow it to be the current dish.

def confirm_dish():
    st.session_state.selected_dish_id = st.session_state.current_dish_id
    st.session_state.app_stage = "CONFIRMED"

def retry_rejected_dishes():
    # Remove candidate_ids from rejected_ids
    st.session_state.rejected_ids = [rid for rid in st.session_state.rejected_ids if rid not in st.session_state.candidate_ids]
    st.session_state.remaining_ids = st.session_state.candidate_ids.copy()
    st.session_state.current_dish_id = None
