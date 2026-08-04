# 🍜 ĂN GÌ ĐÂY? — HÀ NỘI EDITION

![Ăn Gì Đây App](assets/fallback_food.jpg)

## 🎯 Giới thiệu
**"Ăn Gì Đây? — Hà Nội Edition"** là ứng dụng web tương tác vui nhộn, giúp giải quyết triệt để câu hỏi hóc búa nhất mọi thời đại: *"Hôm nay ăn gì?"*. 
Đặc biệt, kho dữ liệu được tuyển chọn kỹ lưỡng với **100+ món ăn đặc sắc nhất của thủ đô Hà Nội**.

## 💡 Vấn đề giải quyết
- **Lưỡng lự:** Chọn món quá khó vì có quá nhiều lựa chọn. App giới hạn "mỗi lần chỉ hiện một món" và không lặp lại món đã từ chối để bạn tập trung quyết định.
- **Không biết ăn gì hợp:** Thuật toán (Recommendation Engine) chấm điểm món ăn dựa trên Giờ giấc thực tế, Thời tiết thực tế (nóng, lạnh, mưa, oi bức) và Tâm trạng của bạn.
- **Chán nản vì khô khan:** Ứng dụng tích hợp AI sinh tạo nội dung (Gemini) để viết những câu rủ rê, "dụ dỗ" đi ăn cực kỳ hài hước, dí dỏm, đậm chất Hà Nội.

## ✨ Tính năng nổi bật
- Thuật toán Hard Filter & Weighted Scoring thông minh.
- Nhận diện thời tiết và giờ giấc thời gian thực (Open-Meteo).
- Fetch ảnh món ăn đẹp mắt từ Pexels API. Tự động sinh ảnh minh hoạ (Fallback) siêu đẹp nếu mạng lỗi.
- Sinh nội dung dụ dỗ vui bằng Google Gemini AI (với 30 câu dự phòng nếu AI lỗi).
- UI/UX cực kỳ bắt mắt, thân thiện với mobile.
- Tìm kiếm nhanh quán ăn trên Google Maps.

---

## 🛠 Hướng dẫn Cài đặt & Chạy Local

### 1. Yêu cầu hệ thống
- **Python 3.11 hoặc 3.12** (Khuyến cáo để tương thích tốt nhất với Streamlit).

### 2. Clone repository & Tạo Virtual Environment
```bash
# Clone source code
git clone https://github.com/your-username/hom-nay-an-gi-hanoi.git
cd hom-nay-an-gi-hanoi

# Tạo virtual environment
python -m venv venv

# Kích hoạt (Mac/Linux)
source venv/bin/activate
# Kích hoạt (Windows)
venv\Scripts\activate
```

### 3. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 4. Thiết lập API Keys (Bắt buộc nếu muốn dùng AI & Ảnh thật)
- **Gemini API:** Lấy miễn phí tại [Google AI Studio](https://aistudio.google.com/).
- **Pexels API:** Lấy miễn phí tại [Pexels API](https://www.pexels.com/api/).

Tạo file `.streamlit/secrets.toml` từ file mẫu:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Mở `.streamlit/secrets.toml` và điền key của bạn vào:
```toml
GEMINI_API_KEY = "key_cua_ban"
GEMINI_MODEL = "gemini-2.5-flash"
PEXELS_API_KEY = "key_cua_ban"
```
> **Lưu ý:** TUYỆT ĐỐI KHÔNG commit file `secrets.toml` hay `.env` lên GitHub. Chúng đã được đưa vào `.gitignore`.
> App hoàn toàn CÓ THỂ CHẠY MƯỢT MÀ ngay cả khi bạn không cấu hình bất kỳ API Key nào nhờ hệ thống Fallback nội bộ.

### 5. Khởi chạy ứng dụng
```bash
streamlit run app.py
```
Mở trình duyệt ở địa chỉ `http://localhost:8501`.

---

## 🚀 Hướng dẫn Deploy lên Streamlit Community Cloud

1. Đẩy source code lên GitHub.
2. Truy cập [share.streamlit.io](https://share.streamlit.io/) và đăng nhập bằng GitHub.
3. Nhấn **New app**, chọn repository `hom-nay-an-gi-hanoi`, nhánh `main`, file chạy là `app.py`.
4. Nhấn vào **Advanced settings** (hoặc mục Secrets) và dán nội dung từ `.streamlit/secrets.toml` của bạn vào đó.
5. Nhấn **Deploy** và chờ vài phút.

---

## 📂 Cách tùy biến dữ liệu

- **Thêm món mới / Sửa dữ liệu món:** Mở file `data/dishes.json` và thêm/sửa JSON object mới tuân thủ schema hiện tại.
- **Tắt Gemini / Đổi Model:** Nếu không muốn dùng Gemini, đơn giản là xóa API Key khỏi secrets. App sẽ dùng 30 mẫu câu vui nhộn có sẵn. Muốn đổi model (vd sang pro), sửa biến `GEMINI_MODEL` trong cấu hình.
- **Thay ảnh món mặc định:** Thêm ảnh của bạn vào thư mục `assets/` và chỉnh sửa config nếu muốn hardcode ảnh.

## 🐛 Các lỗi thường gặp
- **ModuleNotFoundError: No module named 'streamlit'** -> Bạn quên kích hoạt Virtual Environment hoặc quên chạy `pip install -r requirements.txt`.
- **Thiếu ảnh** -> Pexels API hết lượt gọi hoặc sai key. App sẽ tự chuyển sang ảnh placeholder (hệ màu dựa trên category).
- **Lỗi không lấy được thời tiết** -> Open-Meteo có thể thỉnh thoảng block IP, app sẽ dùng thuật toán fallback mặc định 25 độ tuỳ tháng.

---
*Ghi chú: Ảnh minh hoạ lấy từ Pexels (miễn phí bản quyền). Source code được xây dựng hoàn toàn từ các công cụ mã nguồn mở.*
