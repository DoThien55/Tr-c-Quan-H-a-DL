# AI Agent trong Khoa học Máy tính - Phân tích & Đề xuất

## Tổng quan

Dự án phân tích bộ dữ liệu khảo sát về automation desire của worker và expert-rated capability, nhằm đưa ra đề xuất ứng dụng AI Agent trong lĩnh vực Khoa học Máy tính.

## Dataset

| File | Nội dung | Records |
|------|----------|---------|
| `domain_worker_desires.csv` | Worker tự đánh giá mong muốn tự động hóa cho từng task | 5,731 tasks |
| `domain_worker_metadata.csv` | Thông tin nhân khẩu học và thái độ về AI của worker | 1,500 workers |
| `expert_rated_technological_capability.csv` | Chuyên gia đánh giá khả năng tự động hóa của task | 2,057 tasks |
| `task_statement_with_metadata.csv` | O*NET task metadata (tần suất, importance, skill) | ~1,200+ tasks |

## Insight chính

### Gap Analysis (Desire vs Capacity)

| CS Occupation | Worker Desire | Expert Capacity | Gap |
|---|---|---|---|
| Computer & Info Research Scientists | 3.77 | 2.60 | **+1.17** |
| Computer & Info Systems Managers | 3.31 | 2.56 | **+0.75** |
| Network/Systems Administrators | 3.65 | 3.42 | +0.23 |
| Computer Systems Engineers | 3.23 | 3.04 | +0.19 |
| IT Project Managers | 2.86 | 2.55 | +0.31 |
| **Database Administrators** | **2.53** | **3.80** | **-1.27** |
| Computer Network Support | 2.71 | 3.74 | -1.03 |
| Web Developers | 3.07 | 4.09 | -1.02 |
| Computer User Support | 2.95 | 3.89 | -0.94 |
| Computer Programmers | 2.93 | 3.84 | -0.91 |
| Computer Systems Analysts | 2.60 | 3.41 | -0.81 |
| SQA Analysts & Testers | 3.23 | 3.76 | -0.53 |

### Lý do Worker muốn tự động hóa
- Free Time (43.8%) > Repetitive (29.4%) = Human Error (29.4%) = Scale (29.4%) > Stress (16.1%) > Difficulty (11.9%)

### Lý do Worker muốn giữ con người
- Domain Knowledge (30.2%) > Quality Oversight (30%) > Control (27.6%) > Empathy (25.8%) > Dynamic (24.1%) > Ethical (18.1%)

## Đề xuất 6 AI Agent

1. **SQA & Testing Agent** - Auto test generation, regression, bug detection
2. **Database Administration Agent** - Query optimization, auto DBA, NL2SQL
3. **Web Development Agent** - Figma-to-code, code review, doc generation
4. **Research Scientist Agent** - Literature review, experiment design, reproducibility
5. **IT Project Management Agent** - Planning, risk monitoring, status reporting
6. **Network & Systems Admin Agent** - Self-healing, security response, capacity planning

## Hướng dẫn

```bash
# Cài đặt dependencies
pip install streamlit pandas plotly

# Chạy Streamlit app
streamlit run streamlit_app.py
```

## Kiến trúc

```
Human (Oversight, Control, Domain Expert)
    ↓ Feedback/Approval
Orchestrator Agent (Task decomposition, Planning)
    ↓
Code Agent | Test Agent | Doc Agent | Analysis Agent
    ↓
Tool Layer (APIs, DB, Cloud, Git)
```
