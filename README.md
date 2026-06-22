# 📊 🌐 AI Agent trong Khoa học Máy tính - Phân tích & Đề xuất

Ứng dụng web trực quan hóa dữ liệu được xây dựng trên nền tảng **Streamlit** nhằm hỗ trợ các nhà quản lý, kỹ sư công nghệ và chuyên gia AI có góc nhìn sâu sắc về nhu cầu thực tế của người lao động đối lập với năng lực công nghệ hiện tại trong ngành Khoa học Máy tính. Từ đó, hệ thống đưa ra các giải pháp cấu hình **AI Agent** tối ưu nhất cho từng vị trí công việc chuyên biệt.

---

## 📂 Dataset

Ứng dụng xử lý bộ dữ liệu đa chiều liên kết giữa hành vi con người và năng lực công nghệ:

| File | Nội dung | Records | Trạng thái trong Code |
|------|----------|---------|-----------------------|
| `domain_worker_desires.csv` | Worker tự đánh giá mong muốn tự động hóa cho từng task | 5,731 tasks | **Đang sử dụng** (Tính toán `Worker Desire`) |
| `domain_worker_metadata.csv` | Thông tin nhân khẩu học và thái độ về AI của worker | 1,500 workers | *Sẵn sàng cho tích hợp mở rộng* |
| `expert_rated_technological_capability.csv` | Chuyên gia đánh giá khả năng tự động hóa của task | 2,057 tasks | **Đang sử dụng** (Tính toán `Expert Capacity`) |
| `task_statement_with_metadata.csv` | O*NET task metadata (tần suất, tầm quan trọng, skill) | ~1,200+ tasks | *Sẵn sàng cho tích hợp mở rộng* |

---

## 🚀 Các Tính Năng Chính Của Ứng Dụng

Hệ thống phân tích chuyên sâu **13 ngành nghề trọng điểm** thuộc khối Khoa học Máy tính (CS Roles) và được chia làm 4 phân hệ chính điều hướng qua Sidebar:

* **Tổng quan (Overview):** 
  * Hiển thị thống kê nhanh số lượng mẫu và số ngành IT bằng thẻ `st.metric`.
  * Trực quan hóa **Top lý do muốn dùng AI** (Giải phóng thời gian, xử lý data lớn, giảm sai sót...) và **Top lý do sợ giao việc 100% cho AI** (Cần người duyệt chất lượng, trách nhiệm đạo đức/pháp lý, hiểu ngữ cảnh công ty...).
* **Phân tích Độ Lệch (Gap Analysis):** 
  * Tính toán chỉ số lệch bằng công thức $Gap = \text{Worker Desire} - \text{Expert Capacity}$.
  * Trực quan hóa **Bản Đồ Định Vị 4 Góc Phần Tư** (Desire vs Capacity) dựa trên mốc trung vị chuẩn hóa $3.5$ giúp phân loại ngành nghề thành *Nhóm E dè* và *Nhóm Chờ đợi*.
* **Phân tích Chuyên Sâu (CS Deep Dive):** 
  * Bộ lọc chi tiết cho từng ngành để mổ xẻ động lực thúc đẩy và rào cản tâm lý của nhân sự.
  * Tự động phân loại nhóm hành vi (*Nhóm Cẩn Thận*, *Nhóm Mệt Mỏi*, *Nhóm Cân Bằng*) để đưa ra lời khuyên quản trị thực tế.
* **Đề xuất AI Agent:** 
  * Khuyến nghị tự động cấu hình các AI Agent chuyên biệt phù hợp cho từng vị trí công việc (Ví dụ: `Code Review Agent` cho Lập trình viên, `Threat Detection Agent` cho An ninh mạng, `Self-healing Agent` cho Quản trị hệ thống...) kèm lập luận thực tế.

---

## 🛠️ Công nghệ & Tối ưu 

* **Framework & Thư viện:** `Python 3.8+`, `Streamlit`, `Pandas`, `Plotly Express` & `Graph Objects`.
* **Cơ chế An toàn dữ liệu:** Tích hợp bọc `try-except` thông minh khi đọc file CSV. Nếu thiếu file dữ liệu, ứng dụng sẽ thông báo lỗi bằng `st.error` và dừng app an toàn thay vì làm sụp giao diện.
* **Tối ưu hiển thị (CSS Custom):** Nhúng mã CSS trực tiếp để phóng to kích thước hiển thị trên màn hình lớn hoặc máy chiếu (Chữ văn bản: **22px**, Tiêu đề con: **30px**, Chỉ số Metric: **45px Bold**), tăng cường khả năng quét thông tin nhanh chóng.

---

## 💻 Hướng dẫn Cài đặt & Khởi chạy

### 1. Cài đặt các thư viện
```bash
pip install streamlit pandas plotly