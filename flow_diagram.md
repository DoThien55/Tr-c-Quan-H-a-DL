# SƠ ĐỒ LUỒNG: TỪ DỮ LIỆU → PHÂN TÍCH → KHUYẾN NGHỊ AI AGENT

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      1. DỮ LIỆU ĐẦU VÀO (4 CSV)                           ║
║                                                                            ║
║  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐  ┌───────────┐ ║
║  │ Worker Desires  │  │ Expert Capacity │  │   Metadata   │  │ Task Info │ ║
║  │ 5,731 tasks     │  │ 2,057 tasks     │  │ 1,500 workers│  │ O*NET     │ ║
║  │ Worker tự đánh  │  │ Chuyên gia đánh │  │ Nhân khẩu +  │  │ Tần suất  │ ║
║  │ giá mức muốn    │  │ giá khả năng tự │  │ AI attitude  │  │ Importance│ ║
║  │ tự động hóa     │  │ động hóa được   │  │ + LLM usage  │  │           │ ║
║  └────────┬────────┘  └────────┬────────┘  └──────┬───────┘  └─────┬─────┘ ║
╚═══════════╪════════════════════╪═══════════════════╪════════════════╪═══════╝
            │                    │                   │                │
            └────────┬───────────┴───────┬───────────┴────┬───────────┘
                     │                   │                │
                     ▼                   ▼                ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                       2. PHÂN TÍCH & XỬ LÝ                                 ║
║                                                                            ║
║  ┌─────────────────────────────────┐                                       ║
║  │ [Worker Desire Analysis]        │                                       ║
║  │ - Mức độ mong muốn tự động hóa  │                                       ║
║  │ - Lý do: Free Time, Lặp lại,... │                                       ║
║  │ - Mức độ quan trọng của con     │                                       ║
║  │   người (Human Agency)          │                                       ║
║  └───────────────┬─────────────────┘                                       ║
║                  │                                                         ║
║  ┌─────────────────────────────────┐                                       ║
║  │ [Expert Capacity Analysis]      │                                       ║
║  │ - Khả năng tự động hóa thực tế  │                                       ║
║  │ - Yếu tố ảnh hưởng: độ phức     │                                       ║
║  │   tạp, giao tiếp, chuyên môn    │                                       ║
║  └───────────────┬─────────────────┘                                       ║
║                  │                                                         ║
║  ┌─────────────────────────────────┐                                       ║
║  │ [Metadata Analysis]             │                                       ║
║  │ - Mức độ sẵn sàng dùng AI      │                                       ║
║  │ - LLM adoption rate             │                                       ║
║  │ - Thái độ với AI               │                                       ║
║  └───────────────┬─────────────────┘                                       ║
╚══════════════════╪══════════════════════════════════════════════════════════╝
                   │
                   ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                        3. INSIGHTS & KPIs                                  ║
║                                                                            ║
║  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────────────┐  ║
║  │ [GAP ANALYSIS]     │  │ [REASON ANALYSIS]  │  │ [CS DEEP DIVE]       │  ║
║  │                    │  │                    │  │                      │  ║
║  │ So sánh:           │  │ Lý do MUỐN tự động│  │ - LLM adoption 47%   │  ║
║  │ Desire vs Capacity │  │ hóa: Free Time 44% │  │ - Tương quan giữa    │  ║
║  │                    │  │ Lý do KHÔNG muốn:  │  │   các yếu tố         │  ║
║  │ GAP ÂM = Cơ hội    │  │ Domain Knowledge   │  │ - Phân tích từng     │  ║
║  │ GAP DƯƠNG = Thách  │  │ 30%, Oversight 30% │  │   occupation cụ thể  │  ║
║  │ thức               │  │                    │  │                      │  ║
║  └─────────┬──────────┘  └─────────┬──────────┘  └──────────┬───────────┘  ║
╚════════════╪═══════════════════════╪═════════════════════════╪══════════════╝
             │                       │                         │
             └───────────┬───────────┴─────────────┬───────────┘
                         │                         │
                         ▼                         ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                     4. ĐỀ XUẤT AI AGENT (6 cái)                           ║
║                                                                            ║
║  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐  ┌──────┐ ║
║  │  SQA &  │  │   DBA   │  │ Web Dev │  │Research │  │Project │  │Net-  │ ║
║  │  Test   │  │  Agent  │  │  Agent  │  │  Agent  │  │ Mgmt   │  │work  │ ║
║  │  Agent  │  │         │  │         │  │         │  │ Agent  │  │Admin │ ║
║  │         │  │         │  │         │  │         │  │        │  │Agent │ ║
║  │Gap:-0.53│  │Gap:-1.27│  │Gap:-1.02│  │Gap:+1.17│  │Gap:+0.3│  │Gap:  │ ║
║  │🔥Cao   │  │🔥CAO    │  │🔥CAO    │  │⏳Chờ   │  │⏳Chờ  │  │+0.23 │ ║
║  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └───┬────┘  └───┬──┘ ║
╚═══════╪═════════════╪═══════════╪═════════════╪═══════════╪═══════════╪═════╝
        │             │           │             │           │           │
        └──────┬──────┴─────┬─────┴──────┬──────┴─────┬─────┴─────┬─────┘
               │            │            │            │           │
               ▼            ▼            ▼            ▼           ▼
╔══════════════════════════════════════════════════════════════════════════════╗
║                        5. KIẾN TRÚC AI AGENT                               ║
║                                                                            ║
║  ┌──────────────────────────────────────────────────────────────────────┐  ║
║  │          CON NGƯỜI (Human Oversight)                                │  ║
║  │     • Kiểm tra chất lượng • Quyết định cuối • Cung cấp chuyên môn   │  ║
║  └────────────────────────────┬─────────────────────────────────────────┘  ║
║                               │ Phê duyệt / Feedback                       ║
║                               ▼                                             ║
║  ┌──────────────────────────────────────────────────────────────────────┐  ║
║  │                 ORCHESTRATOR AGENT                                   │  ║
║  │  Nhận y/c → Chia nhỏ → Gọi đúng Agent → Gom kết quả → Báo cáo       │  ║
║  └──┬─────┬─────┬─────┬─────┬──────┬─────┬──────────────────────────────┘  ║
║     │     │     │     │     │      │                                      ║
║     ▼     ▼     ▼     ▼     ▼      ▼                                      ║
║   📝    🗄️    🌐    ✅    🔬     📋                                       ║
║  CODE   DB   WEB  TEST  RESEARCH  PM                                       ║
║  AGENT AGENT AGENT AGENT  AGENT  AGENT                                     ║
║     │     │     │     │     │      │                                      ║
║     └─────┴─────┴─────┴─────┴──────┘                                      ║
║                     │                                                      ║
║                     ▼                                                      ║
║  ┌──────────────────────────────────────────────────────────────────────┐  ║
║  │            TOOL LAYER (Công cụ)                                     │  ║
║  │         APIs • Database • Git • Cloud • CLI                         │  ║
║  └──────────────────────────────────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## GIẢI THÍCH NHANH

| Ký hiệu | Ý nghĩa |
|---------|---------|
| 🔥 GAP ÂM | AI đủ giỏi, worker chưa biết → **Triển khai ngay** |
| ⏳ GAP DƯƠNG | Worker muốn nhưng AI chưa đủ → **Cần chờ công nghệ** |
| GAP = Desire - Capacity | = Worker muốn bao nhiêu trừ đi AI làm được bao nhiêu |

## 3 SỐ LIỆU CHÍNH

| Số | Nội dung | Giá trị |
|----|----------|---------|
| 1 | Lý do muốn tự động hóa số 1 | 🕐 **Giải phóng thời gian (44%)** |
| 2 | Lý do giữ con người số 1 | 🧠 **Kiến thức chuyên môn (30%)** |
| 3 | Khoảng cách lớn nhất | 🗄️ **Database Admin (GAP = -1.27)** |

## 6 AI AGENT NGẮN GỌN

| # | Agent | Làm gì? | GAP | Mức độ |
|---|-------|---------|-----|--------|
| 1 | **DBA Agent** 🗄️ | Tự động tối ưu SQL, backup, phát hiện lỗi | -1.27 | 🔥 CAO NHẤT |
| 2 | **Web Dev Agent** 🌐 | Viết code từ bản vẽ, kiểm tra code tự động | -1.02 | 🔥 Cao |
| 3 | **Network Admin Agent** 🌍 | Sửa lỗi mạng, phát hiện xâm nhập | +0.23 | 🔥 Cao |
| 4 | **SQA & Test Agent** ✅ | Kiểm tra lỗi phần mềm tự động | -0.53 | 🔥 Cao |
| 5 | **Research Agent** 🔬 | Tìm tài liệu, thiết kế thí nghiệm | +1.17 | ⏳ Chờ |
| 6 | **Project Mgmt Agent** 📋 | Lập kế hoạch, báo cáo tiến độ | +0.31 | ⏳ Chờ |
