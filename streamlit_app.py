import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="AI Agent trong CS", layout="wide")
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    d = pd.read_csv(os.path.join(DATA_DIR, "domain_worker_desires.csv"))
    c = pd.read_csv(os.path.join(DATA_DIR, "expert_rated_technological_capability.csv"))
    return d, c

desires, capability = load_data()

CS_ROLES = [
    "Computer Programmers", "Computer Systems Analysts",
    "Computer Systems Engineers/Architects", "Computer Network Support Specialists",
    "Computer User Support Specialists", "Computer and Information Systems Managers",
    "Computer and Information Research Scientists", "Software Quality Assurance Analysts and Testers",
    "Web Developers", "Database Administrators", "Information Security Analysts",
    "Information Technology Project Managers", "Network and Computer Systems Administrators"
]

avg_desire = desires.groupby("Occupation (O*NET-SOC Title)")["Automation Desire Rating"].mean()
avg_cap = capability.groupby("Occupation (O*NET-SOC Title)")["Automation Capacity Rating"].mean()
common = avg_desire.index.intersection(avg_cap.index)
gap_df = pd.DataFrame({"Occupation": common, "Worker Desire": avg_desire[common].values,
                       "Expert Capacity": avg_cap[common].values})
gap_df["Gap"] = (gap_df["Worker Desire"] - gap_df["Expert Capacity"]).round(2)
cs_gap = gap_df[gap_df["Occupation"].isin(CS_ROLES)].sort_values("Gap")

st.sidebar.title("Menu")
pages = ["Sơ đồ luồng", "Tổng quan", "Gap Analysis", "CS Deep Dive", "Đề xuất AI Agent"]
choice = st.sidebar.radio("Chọn", pages)

if choice == "Sơ đồ luồng":
    st.title("Sơ đồ luồng: Từ dữ liệu đến khuyến nghị AI Agent")

    fig = go.Figure()
    fig.update_layout(
        width=1100, height=820,
        xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 12]),
        yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[0, 14]),
        plot_bgcolor="white",
        title="Quy trình phân tích & đề xuất AI Agent"
    )

    colors = {
        "data": "#E8F5E9",
        "process": "#E3F2FD",
        "insight": "#FFF3E0",
        "proposal": "#FCE4EC",
        "arch": "#F3E5F5",
        "border": "#333",
        "arrow": "#666"
    }

    def box(x0, y0, x1, y1, text, color, font_size=13):
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                      fillcolor=color, line=dict(color=colors["border"], width=2))
        fig.add_annotation(x=(x0+x1)/2, y=(y0+y1)/2, text=text,
                           showarrow=False, font=dict(size=font_size, color="#000"),
                           align="center", xanchor="center", yanchor="middle")

    def arrow(x0, y0, x1, y1):
        fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y",
                           axref="x", ayref="y", showarrow=True,
                           arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor=colors["arrow"])

    # Layer 1: Data Input
    box(1, 12.5, 11, 13.8, "DỮ LIỆU ĐẦU VÀO", colors["data"], 15)
    box(0.5, 11, 3, 12.2, "domain_worker_desires\n5,731 tasks\nWorker tự đánh giá", colors["data"])
    box(3.5, 11, 6, 12.2, "expert_rated_capability\n2,057 tasks\nChuyên gia đánh giá", colors["data"])
    box(6.5, 11, 9, 12.2, "domain_worker_metadata\n1,500 workers\nNhân khẩu & AI attitude", colors["data"])
    box(9.5, 11, 12, 12.2, "task_statement_metadata\nO*NET task info", colors["data"])

    arrow(6, 11, 6, 10.2)
    arrow(3, 11, 4.5, 10.2)
    arrow(9, 11, 7.5, 10.2)

    # Layer 2: Processing
    box(1, 8.5, 11, 10, "PHÂN TÍCH & XỬ LÝ", colors["process"], 15)
    box(0.5, 7.2, 4, 8.3, "Worker Desire Analysis\nMong muốn & lý do\ntự động hóa", colors["process"])
    box(4.5, 7.2, 8, 8.3, "Expert Capacity Analysis\nKhả năng tự động hóa\ntheo chuyên gia", colors["process"])
    box(8.5, 7.2, 12, 8.3, "Metadata Analysis\nLLM usage, AI attitude,\nnhân khẩu học", colors["process"])

    arrow(6, 8.3, 6, 7.5)
    arrow(2.25, 7.2, 2.25, 6.5)
    arrow(6.25, 7.2, 6.25, 6.5)
    arrow(10.25, 7.2, 10.25, 6.5)
    arrow(2.25, 6.5, 6.25, 6.5)
    arrow(10.25, 6.5, 6.25, 6.5)

    # Layer 3: Insights
    box(1, 4.8, 11, 6.3, "INSIGHTS & KPIs", colors["insight"], 15)
    box(0.5, 3.5, 4, 4.6, "GAP ANALYSIS\nDesire vs Capacity\nKhoảng cách đầu tư", colors["insight"])
    box(4.5, 3.5, 8, 4.6, "REASON ANALYSIS\nTự động hóa: Free Time 44%\nHuman Agency: Knowledge 30%", colors["insight"])
    box(8.5, 3.5, 12, 4.6, "CS OCCUPATION DEEP DIVE\nLLM Adoption 47% daily\nCorrelation ma trận", colors["insight"])

    arrow(6, 4.6, 6, 3.8)
    arrow(2.25, 3.5, 2.25, 2.8)
    arrow(6.25, 3.5, 6.25, 2.8)
    arrow(10.25, 3.5, 10.25, 2.8)
    arrow(2.25, 2.8, 6.25, 2.8)
    arrow(10.25, 2.8, 6.25, 2.8)

    # Layer 4: Proposals
    box(1, 1.2, 11, 2.6, "ĐỀ XUẤT AI AGENT (6 Proposals)", colors["proposal"], 15)
    props = ["SQA &\nTest Agent", "DBA\nAgent", "Web Dev\nAgent", "Research\nAgent", "Project\nMgmt Agent", "Network\nAdmin Agent"]
    for i, p in enumerate(props):
        x0 = 0.5 + i * 2
        x1 = 2.2 + i * 2
        box(x0, 0.15, x1, 1.1, p, colors["proposal"])

    arrow(6, 2.6, 6, 1.8)

    # Layer 5: Architecture
    box(2, -0.8, 10, 0, "KIẾN TRÚC: Human (Oversight) → Orchestrator Agent → Tool Layer (APIs, DB, Git, Cloud)", colors["arch"], 14)

    arrow(6, 0.15, 6, 0)

    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### Giải thích luồng:
    1. **Dữ liệu đầu vào**: 4 bộ CSV được load và xử lý song song
    2. **Phân tích & Xử lý**: Tách thành 3 nhánh phân tích độc lập
    3. **Insights & KPIs**: Tổng hợp thành các chỉ số chính (gap, lý do, tương quan)
    4. **Đề xuất**: 6 AI Agent được đề xuất dựa trên gap và reason analysis
    5. **Kiến trúc**: Thiết kế Human-in-the-loop với Orchestrator Agent
    """)

elif choice == "Tổng quan":
    st.title("AI Agent trong Khoa học Máy tính")
    st.markdown("**Dataset**: 5,731 tasks (worker survey) + 2,057 tasks (expert ratings)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Worker Desire", f"{len(desires):,}")
    col2.metric("Expert Capacity", f"{len(capability):,}")
    col3.metric("CS Occupations", len(CS_ROLES))
    col4.metric("LLM Daily Use (CS)", "47%")

    st.subheader("Lý do Worker muốn tự động hóa")
    rc = {c.split(" - ")[1]: int(desires[c].sum()) for c in
          ["Reasons for Automation Desire - Free Time", "Reasons for Automation Desire - Repetitive",
           "Reasons for Automation Desire - Human Error", "Reasons for Automation Desire - Scale",
           "Reasons for Automation Desire - Stress", "Reasons for Automation Desire - Difficulty"]}
    rdf = pd.DataFrame({"Reason": list(rc.keys()), "Count": list(rc.values())})
    rdf["%"] = (rdf["Count"] / len(desires) * 100).round(1)
    fig1 = px.bar(rdf, x="Reason", y="Count", text="Count", color="Count",
                  color_continuous_scale="reds", title="Lý do Worker muốn tự động hóa")
    fig1.update_traces(texttemplate="%{text} (%{customdata}%)", textposition="outside",
                       customdata=rdf[["%"]])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Lý do giữ con người (Human Agency)")
    ac = {c.split(" - ")[1]: int(desires[c].sum()) for c in
          ["Reasons for Human Agency - Domain Knowledge", "Reasons for Human Agency - Quality Oversight",
           "Reasons for Human Agency - Control", "Reasons for Human Agency - Empathy",
           "Reasons for Human Agency - Dynamic", "Reasons for Human Agency - Ethical"]}
    adf = pd.DataFrame({"Reason": list(ac.keys()), "Count": list(ac.values())})
    adf["%"] = (adf["Count"] / len(desires) * 100).round(1)
    fig2 = px.bar(adf, x="Reason", y="Count", text="Count", color="Count",
                  color_continuous_scale="purples", title="Lý do Worker muốn giữ con người")
    fig2.update_traces(texttemplate="%{text} (%{customdata}%)", textposition="outside",
                       customdata=adf[["%"]])
    st.plotly_chart(fig2, use_container_width=True)

elif choice == "Gap Analysis":
    st.title("Gap: Worker Desire vs Expert Capacity")
    st.markdown("**Gap dương** = Worker muốn nhiều hơn khả năng thực tế | **Gap âm** = Worker chưa nhận thức đủ tiềm năng")

    all_gap = gap_df.sort_values("Gap")
    fig = px.bar(all_gap, x="Gap", y="Occupation", orientation="h", color="Gap",
                 color_continuous_scale="RdYlGn", text_auto=".2f", height=700,
                 title="Gap Analysis - Tất cả ngành")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("CS Occupations")
    fig2 = px.bar(cs_gap, x="Gap", y="Occupation", orientation="h", color="Gap",
                  color_continuous_scale="RdYlGn", text_auto=".2f")
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)

    st.info("""
    **Gap âm lớn (ưu tiên cao)**: Database Admin (-1.27), Web Dev (-1.02), Computer Network Support (-1.03)
    **Gap dương lớn (chờ công nghệ)**: Research Scientists (+1.17), IT Managers (+0.75)
    """)

elif choice == "CS Deep Dive":
    st.title("CS Occupations - Phân tích chuyên sâu")
    role = st.selectbox("Chọn occupation", CS_ROLES)

    d_sub = desires[desires["Occupation (O*NET-SOC Title)"] == role]
    c_sub = capability[capability["Occupation (O*NET-SOC Title)"] == role]

    m1 = {k: round(d_sub[k].mean(), 2) for k in ["Automation Desire Rating", "Core Skill Rating",
           "Job Security Rating", "Enjoyment Rating", "Involved Uncertainty",
           "Domain Expertise Requirement", "Interpersonal Communication Requirement", "Human Agency Scale Rating"]}
    m2 = {k: round(c_sub[k].mean(), 2) for k in ["Automation Capacity Rating", "Physical Action Requirement",
           "Involved Uncertainty", "Domain Expertise Requirement", "Interpersonal Communication Requirement"]}

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Worker Self-Report")
        st.dataframe(pd.DataFrame([m1]).T.rename(columns={0:"Value"}), use_container_width=True)
    with col2:
        st.subheader("Expert Rating")
        st.dataframe(pd.DataFrame([m2]).T.rename(columns={0:"Value"}), use_container_width=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Worker Desire", x=CS_ROLES,
                         y=[avg_desire.get(r, 0) for r in CS_ROLES], marker_color="royalblue"))
    fig.add_trace(go.Bar(name="Expert Capacity", x=CS_ROLES,
                         y=[avg_cap.get(r, 0) for r in CS_ROLES], marker_color="seagreen"))
    fig.update_layout(title="Desire vs Capacity - CS Occupations", barmode="group", xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True)

elif choice == "Đề xuất AI Agent":
    st.title("6 Đề xuất AI Agent trong CS")

    props = [
        ("SQA & Testing Agent", 3.76, 3.23, -0.53, "#2E86AB",
         "Auto test generation, regression, bug pattern detection", ["Repetitive", "Scale"]),
        ("Database Admin Agent", 3.80, 2.53, -1.27, "#A23B72",
         "Query optimization, auto DBA, NL2SQL, anomaly detection", ["Repetitive", "Human Error"]),
        ("Web Dev Agent", 4.09, 3.07, -1.02, "#F18F01",
         "Figma-to-code, code review, doc generation, accessibility", ["Free Time", "Repetitive"]),
        ("Research Agent", 2.60, 3.77, +1.17, "#F25F5C",
         "Literature review, experiment design, reproducibility", ["Free Time", "Difficulty"]),
        ("Project Mgmt Agent", 2.55, 2.86, +0.31, "#247BA0",
         "Planning, risk monitoring, status reports, meeting assistant", ["Free Time", "Stress"]),
        ("Network Admin Agent", 3.42, 3.65, +0.23, "#70C1B3",
         "Self-healing, security response, capacity planning", ["Repetitive", "Scale"])
    ]

    for title, cap, desire, gap, color, desc, reasons in props:
        with st.container():
            st.subheader(title)
            c1, c2, c3 = st.columns([1, 1, 2])
            c1.metric("Capacity", cap)
            c2.metric("Desire", desire)
            c3.markdown(f"**Gap**: {gap:+}  •  **Lý do**: {', '.join(reasons)}")
            st.markdown(f"{desc}")
            st.divider()

   
