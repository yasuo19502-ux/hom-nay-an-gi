import streamlit as st
import time
from urllib.parse import quote_plus
from src.session_manager import init_session, reset_session, check_and_reset_filters, proceed_to_discovery, reject_current_dish, set_current_dish, go_back_to_previous, confirm_dish, retry_rejected_dishes
from src.data_loader import load_dishes
from src.recommendation_engine import get_ranked_candidates, get_next_dish
from src.ui_components import render_header, render_dish_card
from src.models import FilterCriteria
from src.weather_service import get_current_weather_context

st.set_page_config(page_title="Ăn Gì Đây - Hà Nội Edition", page_icon="🍜", layout="centered")

init_session()

dishes = load_dishes()
dish_dict = {d.id: d for d in dishes}

render_header()

if st.session_state.app_stage == "SETUP":
    st.markdown("<div class='custom-card card-padding'>", unsafe_allow_html=True)
    st.markdown("<h2 class='text-primary text-center' style='margin-top:0;'>Hôm nay bạn muốn ăn kiểu gì?</h2>", unsafe_allow_html=True)
    st.markdown("<p class='text-muted text-center' style='margin-bottom:24px;'>Chọn sơ sơ thôi, phần khó để app lo.</p>", unsafe_allow_html=True)
    
    meal_period = st.radio("Bữa ăn:", ["Tự động", "Sáng", "Trưa", "Xế", "Tối", "Đêm"], horizontal=True)
    budget = st.radio("Ngân sách mỗi người:", ["Không quan trọng", "Dưới 30.000 đồng", "30.000–60.000 đồng", "60.000–120.000 đồng", "Trên 120.000 đồng"], horizontal=True)
    mood = st.selectbox("Tâm trạng hiện tại:", ["Không biết, app tự chọn", "Cần món chắc bụng", "Muốn ăn nhẹ", "Thèm đồ nóng", "Thèm đồ mát", "Muốn ăn healthy", "Muốn tự thưởng", "Muốn ăn cùng hội bạn", "Muốn ăn nhanh cho xong"])
    spice_level = st.radio("Mức cay:", ["Không quan trọng", "Không cay", "Cay nhẹ", "Cay vừa", "Càng cay càng tốt"], horizontal=True)
    
    st.write("")
    with st.expander("🛠 Có gì cần né không? (Nâng cao)"):
        vegetarian = st.checkbox("Chỉ tìm đồ chay 🥬")
        district = st.selectbox("Khu vực Hà Nội:", ["Không quan trọng", "Hoàn Kiếm", "Ba Đình", "Đống Đa", "Hai Bà Trưng", "Cầu Giấy", "Thanh Xuân", "Tây Hồ", "Nam Từ Liêm", "Bắc Từ Liêm", "Hà Đông", "Long Biên", "Hoàng Mai"])
        st.write("Kiêng nguyên liệu:")
        cols = st.columns(3)
        avoid_opts = ["Bò", "Lợn", "Gà", "Hải sản", "Trứng", "Sữa"]
        avoid_ingredients = []
        for i, opt in enumerate(avoid_opts):
            with cols[i % 3]:
                if st.checkbox(f"Kiêng {opt.lower()}"):
                    avoid_ingredients.append(opt)
                    
    st.write("")
    if st.button("🎲 BỐC MÓN CHO TÔI", type="primary", use_container_width=True):
        criteria = FilterCriteria(
            meal_period=meal_period,
            budget=budget,
            mood=mood,
            spice_level=spice_level,
            vegetarian=vegetarian,
            avoid_ingredients=avoid_ingredients,
            district=district
        )
        
        sig = criteria.signature()
        check_and_reset_filters(sig)
        
        candidate_ids = get_ranked_candidates(dishes, criteria)
        
        if not candidate_ids:
            st.warning("🥲 Tiêu chí này hơi khó, không có món nào phù hợp. Vui lòng nới lỏng bộ lọc nhé!")
        else:
            st.session_state.current_mood = mood
            st.session_state.current_district = district
            proceed_to_discovery(candidate_ids)
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.app_stage == "DISCOVERY":
    if not st.session_state.current_dish_id:
        next_id = get_next_dish(st.session_state.remaining_ids)
        if next_id:
            set_current_dish(next_id)
            if st.session_state.remaining_ids and st.session_state.remaining_ids[0] == next_id:
                st.session_state.remaining_ids.pop(0)
            st.rerun()
        else:
            st.markdown("<div class='custom-card card-padding text-center'>", unsafe_allow_html=True)
            st.markdown("<h2 class='text-primary'>😅 Bạn vừa từ chối cả một nền ẩm thực!</h2>", unsafe_allow_html=True)
            st.markdown("<p class='text-muted'>Hết món hợp gu rồi. Bây giờ bạn muốn làm gì?</p>", unsafe_allow_html=True)
            st.write("")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 Nới bộ lọc", use_container_width=True):
                    st.session_state.app_stage = "SETUP"
                    st.rerun()
            with col2:
                if st.button("🔄 Cho cơ hội nữa", type="primary", use_container_width=True):
                    retry_rejected_dishes()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            st.stop()
            
    current_dish = dish_dict.get(st.session_state.current_dish_id)
    if current_dish:
        current_mood = st.session_state.get("current_mood", "Không biết, app tự chọn")
        render_dish_card(current_dish, current_mood)
        
        col_main1, col_main2 = st.columns([1, 1])
        with col_main1:
            if st.button("👎 KHÔNG ƯNG, ĐỔI MÓN!", type="primary", use_container_width=True):
                with st.spinner("Đang đảo lại mâm cơm..."):
                    time.sleep(0.3)
                    reject_current_dish()
                    st.rerun()
        with col_main2:
            if st.button("❤️ CHỐT MÓN NÀY", type="secondary", use_container_width=True):
                confirm_dish()
                st.session_state.show_balloons = True
                st.rerun()
                
        st.write("")
        col_sub1, col_sub2 = st.columns([1, 1])
        with col_sub1:
            if st.button("← Món vừa rồi", disabled=len(st.session_state.previous_dish_ids) == 0, use_container_width=True):
                go_back_to_previous()
                st.rerun()
        with col_sub2:
            if st.button("⚙️ Chỉnh gu", use_container_width=True):
                st.session_state.app_stage = "SETUP"
                st.rerun()
                
        st.markdown(f"<p class='text-muted text-center' style='margin-top:24px; font-size:14px;'>Còn <b>{len(st.session_state.remaining_ids)}</b> món hợp gu đang chờ được duyệt.</p>", unsafe_allow_html=True)
        
        if st.session_state.viewed_history:
            with st.expander("🕰 Những món vừa bị bạn phũ"):
                history = st.session_state.viewed_history[-5:]
                for hid in reversed(history):
                    hdish = dish_dict.get(hid)
                    if hdish:
                        st.markdown(f"<p style='margin:0; font-size:14px;'>• {hdish.emoji} {hdish.name}</p>", unsafe_allow_html=True)

elif st.session_state.app_stage == "CONFIRMED":
    if st.session_state.get("show_balloons", False):
        st.balloons()
        st.session_state.show_balloons = False
        
    dish = dish_dict.get(st.session_state.selected_dish_id)
    if dish:
        current_mood = st.session_state.get("current_mood", "Không biết, app tự chọn")
        district_query = st.session_state.get("current_district", "")
        if district_query == "Không quan trọng":
            district_query = ""
            
        st.markdown("<div class='custom-card card-padding text-center' style='background-color: var(--success); color: white;'>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='margin:0; color: white;'>CHỐT KÈO: {dish.name.upper()}! 🎉</h1>", unsafe_allow_html=True)
        st.markdown("<p style='margin:8px 0 0 0; font-size:16px; opacity:0.9;'>Thôi không nghĩ nữa. Đi ăn.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        render_dish_card(dish, current_mood)
        
        st.write("")
        map_query = quote_plus(f"{dish.map_search_query} {district_query} Hà Nội")
        maps_link = f"https://www.google.com/maps/search/?api=1&query={map_query}"
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<a href='{maps_link}' target='_blank' style='display:block; text-align:center; background-color:var(--primary); color:white; padding:16px; border-radius:20px; font-weight:bold; text-decoration:none;'>📍 TÌM QUÁN TRÊN MAPS</a>", unsafe_allow_html=True)
        with col2:
            copy_text = f"Chốt nhé: đi ăn {dish.name}. App Ăn Gì Đây đã phán rồi, không tranh luận nữa."
            st.code(copy_text, language=None)
            
        st.write("")
        st.write("")
        col3, col4 = st.columns(2)
        with col3:
            if st.button("TÔI LẠI ĐỔI Ý", use_container_width=True):
                st.session_state.app_stage = "DISCOVERY"
                # Reject this one so it doesn't loop immediately
                reject_current_dish()
                st.rerun()
        with col4:
            if st.button("CHỌN LẠI TỪ ĐẦU", use_container_width=True):
                reset_session()
                st.rerun()
