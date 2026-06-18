# Sơ đồ luồng: Từ phân tích dữ liệu đến khuyến nghị AI Agent

```mermaid
flowchart TB
    subgraph DATA["1. DỮ LIỆU ĐẦU VÀO"]
        D1[domain_worker_desires<br/>5,731 tasks<br/>Worker tự đánh giá]
        D2[expert_rated_capability<br/>2,057 tasks<br/>Chuyên gia đánh giá]
        D3[domain_worker_metadata<br/>1,500 workers<br/>Nhân khẩu & AI attitude]
        D4[task_statement_metadata<br/>O*NET task info]
    end

    subgraph PROCESS["2. PHÂN TÍCH & XỬ LÝ"]
        P1[Worker Desire Analysis<br/>Mong muốn & lý do tự động hóa]
        P2[Expert Capacity Analysis<br/>Khả năng tự động hóa theo chuyên gia]
        P3[Metadata Analysis<br/>LLM usage, AI attitude, nhân khẩu học]
    end

    subgraph INSIGHT["3. INSIGHTS & KPIs"]
        I1[GAP ANALYSIS<br/>Desire vs Capacity<br/>Khoảng cách đầu tư]
        I2[REASON ANALYSIS<br/>Tự động hóa: Free Time 44%<br/>Human Agency: Knowledge 30%]
        I3[CS DEEP DIVE<br/>LLM Adoption 47% daily<br/>Correlation matrix]
    end

    subgraph PROPOSAL["4. ĐỀ XUẤT AI AGENT"]
        A1[SQA & Test<br/>Agent]
        A2[DBA<br/>Agent]
        A3[Web Dev<br/>Agent]
        A4[Research<br/>Agent]
        A5[Project Mgmt<br/>Agent]
        A6[Network Admin<br/>Agent]
    end

    subgraph ARCH["5. KIẾN TRÚC"]
        Arch["Human (Oversight, Control, Domain Expert)<br/>↓<br/>Orchestrator Agent<br/>↓<br/>Tool Layer (APIs, DB, Git, Cloud, CLI)"]
    end

    D1 --> P1
    D2 --> P2
    D3 --> P3
    D4 --> P2

    P1 --> I1
    P2 --> I1
    P1 --> I2
    P3 --> I3
    P1 --> I3

    I1 --> A1
    I1 --> A2
    I1 --> A3
    I2 --> A4
    I2 --> A5
    I3 --> A6

    A1 --> Arch
    A2 --> Arch
    A3 --> Arch
    A4 --> Arch
    A5 --> Arch
    A6 --> Arch
```

## Giải thích luồng

| Tầng | Mô tả |
|------|-------|
| **1. Dữ liệu đầu vào** | 4 bộ CSV được load và xử lý song song |
| **2. Phân tích & Xử lý** | 3 nhánh phân tích độc lập: Worker Desire, Expert Capacity, Metadata |
| **3. Insights & KPIs** | Tổng hợp thành các chỉ số chính: Gap, Reason Analysis, CS Deep Dive |
| **4. Đề xuất** | 6 AI Agent được đề xuất dựa trên gap và reason analysis |
| **5. Kiến trúc** | Human-in-the-loop với Orchestrator Agent và Tool Layer |

## Kết nối chính

- **Worker Desire + Expert Capacity → Gap Analysis**: So sánh mong muốn vs khả năng thực tế
- **Gap âm (DBA, Web Dev, Network Support)**: Worker chưa nhận thức đủ → Ưu tiên triển khai
- **Gap dương (Research Scientists, IT Managers)**: Worker muốn nhiều hơn khả năng → Chờ công nghệ
- **Reason Analysis → Proposals 4 & 5**: Free Time & Stress → Research Agent, Project Mgmt Agent
- **CS Deep Dive → Proposal 6**: LLM Adoption cao, repetitive tasks → Network Admin Agent
