import json
import random

base_dishes = [
    ("pho_bo", "Phở Bò", "Phở Bò", "🍜", 35000, 70000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Bò"]),
    ("pho_ga", "Phở Gà", "Phở Gà", "🍜", 35000, 60000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Gà"]),
    ("pho_sot_vang", "Phở Sốt Vang", "Phở Sốt Vang", "🍜", 45000, 70000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Bò"]),
    ("bun_cha", "Bún Chả", "Bún Chả", "🍲", 35000, 60000, 0, ["Khô", "Bún/Phở/Miến"], ["Trưa", "Tối"], ["Lợn"]),
    ("bun_rieu", "Bún Riêu", "Bún Riêu", "🍜", 30000, 55000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Hải sản"]),
    ("bun_oc", "Bún Ốc", "Bún Ốc", "🍜", 35000, 55000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa"], ["Hải sản"]),
    ("bun_moc", "Bún Mọc", "Bún Mọc", "🍜", 35000, 50000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa"], ["Lợn"]),
    ("bun_thang", "Bún Thang", "Bún Thang", "🍜", 40000, 65000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa"], ["Gà", "Lợn", "Trứng"]),
    ("bun_ca", "Bún Cá", "Bún Cá", "🍜", 35000, 50000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Hải sản"]),
    ("mien_luon", "Miến Lươn", "Miến Lươn", "🍲", 40000, 65000, 0, ["Nước", "Khô", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Hải sản"]),
    ("mien_ga", "Miến Gà", "Miến Gà", "🍜", 35000, 55000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa"], ["Gà"]),
    ("mien_tron", "Miến Trộn", "Miến Trộn", "🍲", 35000, 50000, 0, ["Khô", "Bún/Phở/Miến"], ["Trưa", "Tối"], []),
    ("chao_suon", "Cháo Sườn", "Cháo Sườn", "🥣", 20000, 40000, 0, ["Nước", "Healthy"], ["Sáng", "Xế", "Đêm"], ["Lợn"]),
    ("chao_long", "Cháo Lòng", "Cháo Lòng", "🥣", 30000, 50000, 0, ["Nước", "Nhậu"], ["Sáng", "Trưa", "Tối", "Đêm"], ["Lợn"]),
    ("chao_trai", "Cháo Trai", "Cháo Trai", "🥣", 15000, 30000, 0, ["Nước", "Ăn vặt"], ["Xế", "Đêm"], ["Hải sản"]),
    ("xoi_xeo", "Xôi Xéo", "Xôi Xéo", "🍚", 15000, 35000, 0, ["Khô", "Cơm"], ["Sáng"], ["Lợn"]),
    ("xoi_thit", "Xôi Thịt", "Xôi Thịt", "🍚", 25000, 45000, 0, ["Khô", "Cơm"], ["Sáng", "Trưa", "Đêm"], ["Lợn"]),
    ("xoi_ga", "Xôi Gà", "Xôi Gà", "🍚", 35000, 55000, 0, ["Khô", "Cơm"], ["Sáng", "Trưa", "Đêm"], ["Gà"]),
    ("banh_cuon", "Bánh Cuốn", "Bánh Cuốn", "🌯", 25000, 45000, 0, ["Khô"], ["Sáng", "Tối", "Đêm"], ["Lợn"]),
    ("banh_mi", "Bánh Mì", "Bánh Mì", "🥖", 15000, 35000, 0, ["Khô", "Nhanh"], ["Sáng", "Trưa", "Xế", "Tối", "Đêm"], ["Lợn"]),
    ("com_rang_dua_bo", "Cơm Rang Dưa Bò", "Cơm Rang", "🍛", 40000, 65000, 0, ["Cơm", "Khô"], ["Trưa", "Tối", "Đêm"], ["Bò"]),
    ("com_rang_thap_cam", "Cơm Rang Thập Cẩm", "Cơm Thập Cẩm", "🍛", 35000, 55000, 0, ["Cơm", "Khô"], ["Trưa", "Tối", "Đêm"], ["Lợn", "Trứng"]),
    ("com_ga", "Cơm Gà", "Cơm Gà", "🍛", 45000, 70000, 0, ["Cơm", "Khô"], ["Trưa", "Tối"], ["Gà"]),
    ("com_tam", "Cơm Tấm", "Cơm Tấm", "🍛", 40000, 80000, 0, ["Cơm", "Khô"], ["Trưa", "Tối"], ["Lợn"]),
    ("com_nieu", "Cơm Niêu", "Cơm Niêu", "🥘", 50000, 100000, 0, ["Cơm", "Khô"], ["Trưa", "Tối"], []),
    ("com_van_phong", "Cơm Văn Phòng", "Cơm VP", "🍱", 35000, 50000, 0, ["Cơm", "Nhanh"], ["Trưa"], []),
    ("bun_dau_mam_tom", "Bún Đậu Mắm Tôm", "Bún Đậu", "🥗", 35000, 60000, 0, ["Khô", "Bún/Phở/Miến"], ["Trưa", "Tối"], ["Lợn"]),
    ("cha_ca", "Chả Cá", "Chả Cá", "🐟", 120000, 200000, 0, ["Khô", "Nhậu"], ["Trưa", "Tối"], ["Hải sản"]),
    ("lau_rieu_cua", "Lẩu Riêu Cua", "Lẩu Riêu", "🍲", 150000, 300000, 0, ["Nước", "Nhậu"], ["Trưa", "Tối", "Đêm"], ["Hải sản", "Bò"]),
    ("lau_thai", "Lẩu Thái", "Lẩu Thái", "🍲", 150000, 300000, 2, ["Nước", "Nhậu"], ["Trưa", "Tối", "Đêm"], ["Hải sản"]),
    ("lau_ga", "Lẩu Gà", "Lẩu Gà", "🍲", 150000, 250000, 0, ["Nước", "Nhậu"], ["Trưa", "Tối", "Đêm"], ["Gà"]),
    ("lau_ech", "Lẩu Ếch", "Lẩu Ếch", "🍲", 150000, 250000, 1, ["Nước", "Nhậu"], ["Trưa", "Tối", "Đêm"], []),
    ("ga_tan", "Gà Tần", "Gà Tần", "🥣", 50000, 80000, 0, ["Nước", "Healthy"], ["Xế", "Tối", "Đêm"], ["Gà"]),
    ("mi_van_than", "Mì Vằn Thắn", "Mì Vằn Thắn", "🍜", 40000, 60000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Lợn", "Hải sản"]),
    ("mi_tron", "Mì Trộn", "Mì Trộn", "🍝", 35000, 50000, 0, ["Khô", "Bún/Phở/Miến"], ["Trưa", "Tối"], []),
    ("mi_cay", "Mì Cay", "Mì Cay", "🍜", 40000, 70000, 3, ["Nước", "Bún/Phở/Miến"], ["Trưa", "Tối"], ["Hải sản"]),
    ("pho_cuon", "Phở Cuốn", "Phở Cuốn", "🌯", 40000, 80000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối"], ["Bò"]),
    ("nem_nuong", "Nem Nướng", "Nem Nướng", "🍢", 30000, 60000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối"], ["Lợn"]),
    ("banh_trang_tron", "Bánh Tráng Trộn", "Bánh Tráng", "🥗", 20000, 35000, 1, ["Khô", "Ăn vặt"], ["Xế", "Tối"], ["Bò", "Trứng"]),
    ("tao_pho", "Tào Phớ", "Tào Phớ", "🍨", 10000, 20000, 0, ["Ngọt", "Ăn vặt", "Mát"], ["Sáng", "Trưa", "Xế", "Tối"], []),
    ("che", "Chè", "Chè", "🍧", 15000, 30000, 0, ["Ngọt", "Ăn vặt", "Mát"], ["Xế", "Tối"], []),
    ("sua_chua", "Sữa Chua", "Sữa Chua", "🍦", 15000, 30000, 0, ["Ngọt", "Ăn vặt", "Mát"], ["Xế", "Tối"], ["Sữa"]),
    ("kem", "Kem", "Kem", "🍦", 10000, 30000, 0, ["Ngọt", "Ăn vặt", "Mát"], ["Xế", "Tối"], ["Sữa"]),
    ("pizza", "Pizza", "Pizza", "🍕", 100000, 300000, 0, ["Khô", "Nhanh"], ["Trưa", "Tối"], ["Sữa", "Lợn"]),
    ("burger", "Burger", "Burger", "🍔", 40000, 100000, 0, ["Khô", "Nhanh"], ["Trưa", "Tối"], ["Bò"]),
    ("ga_ran", "Gà Rán", "Gà Rán", "🍗", 40000, 150000, 0, ["Khô", "Nhanh"], ["Trưa", "Tối", "Xế"], ["Gà"]),
    ("sushi", "Sushi", "Sushi", "🍣", 100000, 500000, 0, ["Khô", "Healthy"], ["Trưa", "Tối"], ["Hải sản"]),
    ("salad", "Salad", "Salad", "🥗", 40000, 120000, 0, ["Khô", "Healthy", "Chay"], ["Sáng", "Trưa", "Tối"], []),
    ("do_chay", "Đồ Chay", "Đồ Chay", "🥬", 30000, 80000, 0, ["Khô", "Healthy", "Chay"], ["Sáng", "Trưa", "Tối", "Xế"], ["Bò", "Lợn", "Gà", "Hải sản"]),
]

additional_dishes = [
    ("bun_bo_hue", "Bún Bò Huế", "Bún Bò", "🍜", 40000, 70000, 1, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Bò", "Lợn"]),
    ("hu_tieu", "Hủ Tiếu", "Hủ Tiếu", "🍜", 35000, 60000, 0, ["Nước", "Khô", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối", "Đêm"], ["Lợn", "Hải sản"]),
    ("com_suon", "Cơm Sườn", "Cơm Sườn", "🍛", 40000, 70000, 0, ["Cơm", "Khô"], ["Trưa", "Tối"], ["Lợn"]),
    ("banh_xeo", "Bánh Xèo", "Bánh Xèo", "🌮", 30000, 60000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối"], ["Lợn", "Hải sản"]),
    ("nem_lui", "Nem Lụi", "Nem Lụi", "🍢", 30000, 60000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối"], ["Lợn"]),
    ("banh_goi", "Bánh Gối", "Bánh Gối", "🥟", 15000, 40000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối"], ["Lợn"]),
    ("banh_ran_man", "Bánh Rán Mặn", "Bánh Rán", "🥯", 10000, 30000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối"], ["Lợn"]),
    ("banh_tom", "Bánh Tôm", "Bánh Tôm", "🍤", 30000, 70000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối"], ["Hải sản"]),
    ("banh_duc_nong", "Bánh Đúc Nóng", "Bánh Đúc", "🥣", 15000, 30000, 0, ["Nước", "Ăn vặt"], ["Xế", "Tối"], ["Lợn"]),
    ("bun_ngan", "Bún Ngan", "Bún Ngan", "🍜", 40000, 65000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Gà"]),
    ("bun_vit", "Bún Vịt", "Bún Vịt", "🍜", 40000, 65000, 0, ["Nước", "Bún/Phở/Miến"], ["Trưa", "Tối"], ["Gà"]),
    ("ngan_chay_toi", "Ngan Cháy Tỏi", "Ngan Tỏi", "🍗", 150000, 250000, 0, ["Khô", "Nhậu"], ["Trưa", "Tối"], ["Gà"]),
    ("ga_luoc", "Gà Luộc", "Gà Luộc", "🍗", 100000, 300000, 0, ["Khô", "Nhậu", "Healthy"], ["Trưa", "Tối"], ["Gà"]),
    ("ga_nuong", "Gà Nướng", "Gà Nướng", "🍗", 100000, 300000, 0, ["Khô", "Nhậu"], ["Trưa", "Tối"], ["Gà"]),
    ("vit_quay", "Vịt Quay", "Vịt Quay", "🍗", 150000, 300000, 0, ["Khô", "Nhậu"], ["Trưa", "Tối"], ["Gà"]),
    ("lon_quay", "Lợn Quay", "Lợn Quay", "🍖", 150000, 300000, 0, ["Khô", "Nhậu"], ["Trưa", "Tối"], ["Lợn"]),
    ("bo_ne", "Bò Né", "Bò Né", "🥩", 50000, 100000, 0, ["Khô", "Nhậu"], ["Sáng", "Trưa", "Tối"], ["Bò", "Trứng"]),
    ("bo_bit_tet", "Bò Bít Tết", "Bít Tết", "🥩", 70000, 200000, 0, ["Khô", "Sang"], ["Trưa", "Tối"], ["Bò"]),
    ("mi_y", "Mì Ý", "Mì Ý", "🍝", 60000, 150000, 0, ["Khô", "Bún/Phở/Miến"], ["Trưa", "Tối"], ["Bò"]),
    ("banh_bao", "Bánh Bao", "Bánh Bao", "🥟", 15000, 30000, 0, ["Khô", "Ăn vặt"], ["Sáng", "Xế", "Đêm"], ["Lợn", "Trứng"]),
    ("xuc_xich", "Xúc Xích", "Xúc Xích", "🌭", 15000, 35000, 0, ["Khô", "Ăn vặt", "Nhanh"], ["Xế", "Tối", "Đêm"], ["Lợn"]),
    ("thit_xien_nuong", "Thịt Xiên", "Thịt Xiên", "🍢", 10000, 50000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối", "Đêm"], ["Lợn"]),
    ("oc_luoc", "Ốc Luộc", "Ốc Luộc", "🐌", 40000, 100000, 0, ["Khô", "Nhậu", "Ăn vặt"], ["Tối", "Đêm"], ["Hải sản"]),
    ("oc_xao", "Ốc Xào", "Ốc Xào", "🐌", 50000, 120000, 1, ["Khô", "Nhậu", "Ăn vặt"], ["Tối", "Đêm"], ["Hải sản"]),
    ("nem_chua_ran", "Nem Chua Rán", "Nem Rán", "🍢", 30000, 70000, 0, ["Khô", "Ăn vặt"], ["Xế", "Tối", "Đêm"], ["Lợn"]),
    ("chan_ga_sa_ot", "Chân Gà Sả Ớt", "Chân Gà", "🍗", 50000, 100000, 2, ["Khô", "Nhậu", "Ăn vặt"], ["Tối", "Đêm"], ["Gà"]),
    ("lau_bo", "Lẩu Bò", "Lẩu Bò", "🍲", 150000, 300000, 0, ["Nước", "Nhậu"], ["Trưa", "Tối", "Đêm"], ["Bò"]),
    ("lau_nam", "Lẩu Nấm", "Lẩu Nấm", "🍲", 150000, 300000, 0, ["Nước", "Healthy", "Nhậu"], ["Trưa", "Tối"], []),
    ("lau_hai_san", "Lẩu Hải Sản", "Lẩu HS", "🍲", 200000, 500000, 0, ["Nước", "Nhậu"], ["Trưa", "Tối", "Đêm"], ["Hải sản"]),
    ("bun_hai_san", "Bún Hải Sản", "Bún HS", "🍜", 40000, 70000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Hải sản"]),
    ("banh_da_cua", "Bánh Đa Cua", "Bánh Đa", "🍜", 35000, 60000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Hải sản"]),
    ("mien_cua", "Miến Cua", "Miến Cua", "🍜", 40000, 70000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Hải sản"]),
    ("com_chien_hai_san", "Cơm Chiên HS", "Cơm HS", "🍛", 50000, 90000, 0, ["Cơm", "Khô"], ["Trưa", "Tối"], ["Hải sản"]),
    ("com_chay", "Cơm Chay", "Cơm Chay", "🍛", 30000, 60000, 0, ["Cơm", "Chay", "Healthy"], ["Trưa", "Tối"], ["Bò", "Lợn", "Gà", "Hải sản"]),
    ("bun_chay", "Bún Chay", "Bún Chay", "🍜", 30000, 60000, 0, ["Nước", "Chay", "Healthy"], ["Sáng", "Trưa", "Tối"], ["Bò", "Lợn", "Gà", "Hải sản"]),
    ("pho_chay", "Phở Chay", "Phở Chay", "🍜", 35000, 65000, 0, ["Nước", "Chay", "Healthy"], ["Sáng", "Trưa", "Tối"], ["Bò", "Lợn", "Gà", "Hải sản"]),
    ("sup_luon", "Súp Lươn", "Súp Lươn", "🥣", 30000, 60000, 0, ["Nước", "Healthy"], ["Sáng", "Tối"], ["Hải sản"]),
    ("sup_cua", "Súp Cua", "Súp Cua", "🥣", 20000, 40000, 0, ["Nước", "Ăn vặt"], ["Xế", "Tối"], ["Hải sản"]),
    ("sup_ga", "Súp Gà", "Súp Gà", "🥣", 20000, 40000, 0, ["Nước", "Healthy"], ["Xế", "Tối"], ["Gà"]),
    ("chao_chim", "Cháo Chim", "Cháo Chim", "🥣", 50000, 100000, 0, ["Nước", "Healthy"], ["Tối", "Đêm"], ["Gà"]),
    ("xoi_man", "Xôi Mặn", "Xôi Mặn", "🍚", 20000, 50000, 0, ["Khô", "Cơm"], ["Sáng", "Đêm"], ["Lợn"]),
    ("banh_gio", "Bánh Giò", "Bánh Giò", "🥟", 15000, 30000, 0, ["Khô", "Ăn vặt"], ["Sáng", "Xế", "Đêm"], ["Lợn"]),
    ("banh_chung", "Bánh Chưng", "Bánh Chưng", "🍘", 50000, 100000, 0, ["Khô", "Cơm"], ["Sáng", "Trưa", "Tối"], ["Lợn"]),
    ("banh_tet", "Bánh Tét", "Bánh Tét", "🍘", 50000, 100000, 0, ["Khô", "Cơm"], ["Sáng", "Trưa", "Tối"], ["Lợn"]),
    ("mi_xao_mem", "Mì Xào Mềm", "Mì Xào", "🍝", 40000, 70000, 0, ["Khô", "Bún/Phở/Miến"], ["Trưa", "Tối", "Đêm"], ["Bò"]),
    ("mi_xao_gion", "Mì Xào Giòn", "Mì Giòn", "🍝", 45000, 80000, 0, ["Khô", "Bún/Phở/Miến"], ["Trưa", "Tối"], ["Hải sản", "Bò"]),
    ("hu_tieu_nam_vang", "Hủ Tiếu Nam Vang", "Hủ Tiếu NV", "🍜", 45000, 75000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Lợn", "Hải sản"]),
    ("bun_tom", "Bún Tôm", "Bún Tôm", "🍜", 40000, 70000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa"], ["Hải sản"]),
    ("bun_hen", "Bún Hến", "Bún Hến", "🍜", 25000, 45000, 1, ["Khô", "Bún/Phở/Miến"], ["Sáng", "Trưa"], ["Hải sản"]),
    ("chao_hen", "Cháo Hến", "Cháo Hến", "🥣", 25000, 45000, 1, ["Nước"], ["Sáng", "Tối"], ["Hải sản"]),
    ("com_hen", "Cơm Hến", "Cơm Hến", "🍛", 25000, 45000, 1, ["Cơm", "Khô"], ["Trưa", "Tối"], ["Hải sản"]),
    ("banh_canh_cua", "Bánh Canh Cua", "Bánh Canh", "🍜", 40000, 80000, 0, ["Nước", "Bún/Phở/Miến"], ["Sáng", "Trưa", "Tối"], ["Hải sản"])
]

all_dishes_raw = base_dishes + additional_dishes

dishes = []
for d in all_dishes_raw:
    id, name, short, emoji, pmin, pmax, spice, types, meals, avoids = d
    
    dish = {
        "id": id,
        "name": name,
        "short_name": short,
        "emoji": emoji,
        "description": f"Tuyệt phẩm {name.lower()} đậm đà hương vị, một lựa chọn tuyệt vời cho ngày hôm nay.",
        "fun_fact": f"Bạn có biết {name.lower()} là một trong những món được yêu thích nhất ở Hà Nội không?",
        "meal_periods": meals,
        "weather_tags": ["Nắng", "Mưa", "Lạnh", "Mát"] if "Nước" not in types else ["Mưa", "Lạnh", "Mát"],
        "temperature_tags": ["Nóng", "Ấm"] if "Nước" in types else ["Vừa", "Mát", "Nóng"],
        "food_types": types,
        "mood_tags": ["Chắc bụng", "Tự thưởng", "Tụ tập"] if pmin >= 50000 else ["Chắc bụng", "Nhanh gọn"],
        "diet_tags": ["Chay"] if "Chay" in types else [],
        "avoid_ingredients": avoids,
        "main_ingredients": avoids + ["Gạo"] if "Cơm" in types else avoids,
        "price_min": pmin,
        "price_max": pmax,
        "spice_level": spice,
        "heaviness_level": 4 if pmax > 50000 else 2,
        "healthy_score": 8 if "Healthy" in types else 5,
        "popularity_score": random.randint(7, 10),
        "hanoi_relevance_score": 9 if "pho" in id or "bun" in id else 6,
        "pexels_queries": [
            f"vietnamese {name.lower()} food",
            f"vietnam {name.lower()}",
            f"{name.lower()} dish",
            "asian street food",
            "delicious vietnamese food"
        ],
        "fallback_image_category": "food",
        "map_search_query": f"{name} ngon Hà Nội"
    }
    
    if "chay" in id or "salad" in id:
        dish["diet_tags"].append("Ít béo")
    
    dishes.append(dish)

with open('data/dishes.json', 'w', encoding='utf-8') as f:
    json.dump(dishes, f, ensure_ascii=False, indent=2)

print(f"Generated {len(dishes)} dishes.")
