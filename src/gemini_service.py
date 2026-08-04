import random
import streamlit as st
import json
from google import genai
from google.genai import types
from src.config import Config
from src.models import Dish

fallback_templates = [
    ("Trời này mà làm bát {name} nóng hổi thì cái bụng tự khắc biết điều.", "Ngon từ thịt, ngọt từ xương, chuẩn bài rồi!", "Đi ăn {name} không bạn ơi, đang thèm!"),
    ("Lương chưa về nhưng {name} vẫn đủ sức cứu một ngày dài.", "Giá cả hợp lý mà ăn ngon quên sầu.", "Đói rã rời, đi làm bữa {name} giải cứu tâm hồn nào!"),
    ("Không phải bạn thèm {name}, là {name} đang gọi tên bạn đấy.", "Món ngon phải thử ngay kẻo lỡ.", "Ai đó làm ơn rủ tôi đi ăn {name} với!"),
    ("Đã đói thì đừng thử thách lòng kiên nhẫn bằng việc nhịn {name}.", "Đủ năng lượng cho bạn hoạt động tiếp.", "Thèm {name} quá, triển luôn không đợi?"),
    ("Cứ mỗi lần không biết ăn gì, {name} lại là chân ái.", "Sự lựa chọn quốc dân không bao giờ sai.", "Cuối ngày rồi, tự thưởng bát {name} thôi!"),
    ("Thấy {name} là tự dưng thấy cồn cào.", "Mùi thơm nức mũi, không ăn hơi phí.", "Trời đẹp thế này, đi ăn {name} là hợp lý nhất."),
    ("{name} - Đỉnh cao ẩm thực giải cứu chiếc bụng đói.", "Không cần nghĩ nhiều, ngon là dứt.", "Ăn {name} cho đời thêm tươi bạn ơi!"),
    ("Món {name} này không ăn hôm nay thì ngày mai vẫn thèm.", "Cắn một miếng là say đắm một đời.", "Ai đi ăn {name} điểm danh!"),
    ("Nghe nói ăn {name} sẽ giúp tâm trạng tốt hơn 200%.", "Sự thật đã được chứng minh qua nhiều cái bụng.", "Bạn đã thử {name} hôm nay chưa?"),
    ("Một phần {name} đầy đặn, đánh tan mọi muộn phiền.", "Ăn ngon mặc đẹp, tội gì không thử.", "Sáng ra làm suất {name} là tỉnh cả người."),
    ("Làm sao có thể chối từ sự hấp dẫn của {name}?", "Hương vị bùng nổ, ăn là ghiền.", "Bụng reo rồi, {name} thẳng tiến!"),
    ("Nắng mưa là chuyện của trời, thèm {name} là chuyện của tui.", "Thời tiết nào thì món này cũng cân tất.", "Hôm nay quyết tâm phải ăn được {name}!"),
    ("{name} ngon số dách, không thử hơi phí.", "Tuyệt kỹ ẩm thực hội tụ trong một món ăn.", "Cuối tuần rồi, rủ bạn bè đi xơi {name} ngay!"),
    ("Ăn {name} xong là thấy yêu đời hẳn ra.", "Đồ ăn ngon làm người ta hạnh phúc.", "Chỉ một từ thôi: {name}!"),
    ("Chiếc bụng đói đang gào thét đòi {name}.", "Hãy lắng nghe tiếng gọi từ bao tử.", "Cứu đói khẩn cấp bằng {name}!"),
    ("Không ăn {name} hôm nay, bạn sẽ tiếc hùi hụi.", "Món ngon không chờ đợi ai.", "Quyết định rồi, chốt {name}!"),
    ("Chỉ cần một suất {name}, mọi muộn phiền bay biến.", "Sức mạnh kỳ diệu của đồ ăn ngon.", "Đi ăn {name} để xả stress nào!"),
    ("Hôm nay ăn gì? Đáp án chỉ có một: {name}.", "Sự lựa chọn hoàn hảo không cần suy nghĩ.", "Chốt đơn {name} thôi anh em ơi!"),
    ("Thèm {name} quá, ai rủ đi ăn ngay đi!", "Chỉ đợi một lời mời.", "Có ai đi ăn {name} không, cho đi ké với!"),
    ("Đừng để bụng đói, hãy lấp đầy bằng {name}.", "Ăn ngoan cho chóng lớn.", "Nuông chiều bản thân bằng {name} một chút đi."),
    ("{name} - Tình yêu không cần lời nói.", "Chỉ cần cảm nhận bằng vị giác.", "Say đắm hương vị {name} mất rồi!"),
    ("Một ngày trọn vẹn không thể thiếu {name}.", "Miếng ngon nhớ lâu.", "Khởi đầu ngày mới với {name} là nhất!"),
    ("Ăn {name} cho có sức cày cuốc tiếp nào.", "Nạp năng lượng tức thì.", "Đang đuối quá, phải nạp {name} gấp!"),
    ("Trời ơi, tự dưng thèm {name} ngang ngược.", "Cái nết ăn uống không đỡ nổi.", "Có thực mới vực được đạo, đi ăn {name}!"),
    ("Đừng hỏi tại sao tôi lại mê {name} đến vậy.", "Ngon thế này ai mà chối từ được.", "Hội những người cuồng {name} điểm danh!"),
    ("Một lần thử {name}, vạn lần say đắm.", "Hương vị vương vấn mãi không thôi.", "Ghiền {name} mất rồi làm sao đây?"),
    ("{name} - Giải pháp tối ưu cho chiếc bụng rỗng.", "Nhanh, gọn, lẹ mà vẫn siêu ngon.", "Không có thời gian thì cứ {name} mà táng!"),
    ("Ăn {name} cùng hội bạn thân là bao vui.", "Thêm bạn thêm vui, thêm {name} thêm no.", "Set kèo ăn {name} với đám bạn ngay!"),
    ("Chỉ mong ngày nào cũng được ăn {name}.", "Ước mơ nhỏ nhoi của tâm hồn ăn uống.", "Hôm nay nhất định phải ăn {name}!"),
    ("{name} - Chân ái của đời tôi.", "Không gì có thể thay thế.", "Yêu {name} hơn cả người yêu cũ!")
]

@st.cache_data(ttl=86400, show_spinner=False)
def generate_fun_copy(dish_id: str, dish_name: str, meal_period: str, weather_tags: tuple, mood: str) -> dict:
    fallback = random.choice(fallback_templates)
    fallback_result = {
        "headline": fallback[0].format(name=dish_name),
        "reason": fallback[1].format(name=dish_name),
        "share_text": fallback[2].format(name=dish_name)
    }

    if not Config.GEMINI_API_KEY:
        return fallback_result
        
    try:
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        
        weather_str = ", ".join(weather_tags)
        
        prompt = f"""
Viết nội dung rủ rê đi ăn món '{dish_name}'. 
Hoàn cảnh: Bữa {meal_period}, Thời tiết: {weather_str}, Tâm trạng: {mood}.
Yêu cầu:
- Viết tiếng Việt, giọng vui, dí dỏm, tự nhiên như một người bạn.
- Hơi mang màu sắc Hà Nội.
- Không thô tục, không bịa quán ăn, không bịa giá, không tạo claim sức khỏe.
- Nhắc được món ăn.
- Không lặp nguyên văn description.
- Không nói mình là AI.
"""

        response = client.models.generate_content(
            model=Config.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "headline": types.Schema(type=types.Type.STRING, description="Headline rủ rê, tối đa 12 từ."),
                        "reason": types.Schema(type=types.Type.STRING, description="Lý do nên ăn, tối đa 25 từ."),
                        "share_text": types.Schema(type=types.Type.STRING, description="Câu ngắn rủ rê đăng story, tối đa 35 từ.")
                    },
                    required=["headline", "reason", "share_text"]
                ),
                temperature=0.8
            )
        )
        
        if response.text:
            data = json.loads(response.text)
            return data
            
    except Exception as e:
        print(f"Gemini API Error: {e}")
        
    return fallback_result

def get_dish_copy(dish: Dish, weather_tags: list, mood: str) -> dict:
    # Use session_state to avoid recalling for the exact same context if needed, 
    # but st.cache_data on generate_fun_copy already does this perfectly.
    # Convert list to tuple for cache key hashing
    weather_tuple = tuple(weather_tags)
    return generate_fun_copy(dish.id, dish.name, dish.meal_periods[0] if dish.meal_periods else "Tự động", weather_tuple, mood)
