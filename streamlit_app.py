import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="AI Agent trong Khoa học Máy tính", layout="wide")
st.title("Phân tích & Đề xuất AI Agent trong Khoa học Máy tính")

DATA_DIR = "."

@st.cache_data
def load_data():
    desires = pd.read_csv(os.path.join(DATA_DIR, "domain_worker_desires.csv"))
    metadata = pd.read_csv(os.path.join(DATA_DIR, "domain_worker_metadata.csv"))
    capability = pd.read_csv(os.path.join(DATA_DIR, "expert_rated_technological_capability.csv"))
    tasks = pd.read_csv(os.path.join(DATA_DIR, "task_statement_with_metadata.csv"))
    return desires, metadata, capability, tasks

desires, metadata, capability, tasks = load_data()

CS_ROLES = [
    "Computer Programmers", "Computer Systems Analysts",
    "Computer Systems Engineers/Architects", "Computer Network Support Specialists",
    "Computer User Support Specialists", "Computer and Information Systems Managers",
    "Computer and Information Research Scientists", "Software Quality Assurance Analysts and Testers",
    "Web Developers", "Database Administrators", "Information Security Analysts",
    "Information Technology Project Managers", "Network and Computer Systems Administrators"
]

st.sidebar.title("Điều hướng")
pages = [
    "1. Tổng quan dữ liệu",
    "2. Worker Automation Desire",
    "3. Expert Automation Capacity",
    "4. Gap Analysis (Desire vs Capacity)",
    "5. Human Agency Analysis",
    "6. CS Occupations - Deep Dive",
    "7. LLM Usage & AI Readiness",
    "8. Đề xuất AI Agent",
]
choice = st.sidebar.radio("Chọn trang", pages)

if choice == "1. Tổng quan dữ liệu":
    st.header("Tổng quan bộ dữ liệu")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Worker Desires", f"{len(desires):,} tasks")
    col2.metric("Worker Metadata", f"{len(metadata):,} workers")
    col3.metric("Expert Capability", f"{len(capability):,} tasks")
    col4.metric("Task Metadata", f"{len(tasks):,} tasks")

    st.subheader("Các occupation được khảo sát")
    occs = desires["Occupation (O*NET-SOC Title)"].unique()
    st.dataframe(pd.DataFrame({"Occupation": occs, "Count": [len(desires[desires["Occupation (O*NET-SOC Title)"] == o]) for o in occs]}).sort_values("Count", ascending=False).reset_index(drop=True), use_container_width=True)

    st.subheader("Phân bố Self-reported Expertise")
    fig = px.pie(desires, names="Self-reported Expertise", title="Expertise Level", color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

elif choice == "2. Worker Automation Desire":
    st.header("Worker Automation Desire Analysis")
    st.markdown("**Worker tự đánh giá mức độ mong muốn tự động hóa cho từng task (1-5)**")

    avg_desire = desires.groupby("Occupation (O*NET-SOC Title)")["Automation Desire Rating"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(avg_desire.head(20), x="Automation Desire Rating", y="Occupation (O*NET-SOC Title)", orientation="h",
                 title="Top 20 ngành muốn tự động hóa nhất", color="Automation Desire Rating",
                 color_continuous_scale="blues", text_auto=".2f")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Lý do worker muốn tự động hóa")
    reasons_cols = ["Reasons for Automation Desire - Free Time", "Reasons for Automation Desire - Repetitive",
                    "Reasons for Automation Desire - Human Error", "Reasons for Automation Desire - Stress",
                    "Reasons for Automation Desire - Difficulty", "Reasons for Automation Desire - Scale"]
    reasons_data = {c.split(" - ")[1]: desires[c].eq("True").sum() for c in reasons_cols}
    reasons_df = pd.DataFrame({"Reason": list(reasons_data.keys()), "Count": list(reasons_data.values())})
    reasons_df["Percentage"] = (reasons_df["Count"] / len(desires) * 100).round(1)
    fig = px.bar(reasons_df, x="Reason", y="Percentage", text="Percentage", color="Percentage",
                 color_continuous_scale="reds", title="Tỷ lệ tasks có lý do muốn tự động hóa")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Tương quan: Automation Desire vs các yếu tố khác")
    corr = desires[["Automation Desire Rating", "Core Skill Rating", "Job Security Rating",
                    "Enjoyment Rating", "Involved Uncertainty", "Domain Expertise Requirement",
                    "Interpersonal Communication Requirement", "Human Agency Scale Rating"]].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto",
                    title="Ma trận tương quan")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "3. Expert Automation Capacity":
    st.header("Expert Automation Capacity Analysis")
    st.markdown("**Chuyên gia đánh giá khả năng tự động hóa của từng task (1-5)**")

    avg_cap = capability.groupby("Occupation (O*NET-SOC Title)")["Automation Capacity Rating"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(avg_cap.head(20), x="Automation Capacity Rating", y="Occupation (O*NET-SOC Title)", orientation="h",
                 title="Top 20 ngành có khả năng tự động hóa cao nhất", color="Automation Capacity Rating",
                 color_continuous_scale="greens", text_auto=".2f")
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Phân bố Automation Capacity Rating")
    fig = px.histogram(capability, x="Automation Capacity Rating", nbins=5, title="Phân bố điểm năng lực tự động hóa",
                       color_discrete_sequence=["seagreen"], text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Yếu tố ảnh hưởng đến Automation Capacity")
    corr_cap = capability[["Automation Capacity Rating", "Physical Action Requirement",
                           "Involved Uncertainty", "Domain Expertise Requirement",
                           "Interpersonal Communication Requirement", "Human Agency Scale Rating"]].corr()
    fig = px.imshow(corr_cap, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto",
                    title="Tương quan giữa Capacity và các yếu tố đầu vào")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "4. Gap Analysis (Desire vs Capacity)":
    st.header("Gap Analysis: Worker Desire vs Expert Capacity")
    st.markdown("**Gap = Worker Desire - Expert Capacity. Gap dương: worker muốn nhiều hơn khả năng thực tế. Gap âm: worker chưa nhận thức đủ tiềm năng.**")

    avg_desire = desires.groupby("Occupation (O*NET-SOC Title)")["Automation Desire Rating"].mean()
    avg_cap = capability.groupby("Occupation (O*NET-SOC Title)")["Automation Capacity Rating"].mean()
    common_occs = avg_desire.index.intersection(avg_cap.index)
    gap_df = pd.DataFrame({"Occupation": common_occs, "Worker Desire": avg_desire[common_occs].values,
                           "Expert Capacity": avg_cap[common_occs].values})
    gap_df["Gap"] = (gap_df["Worker Desire"] - gap_df["Expert Capacity"]).round(2)
    gap_df = gap_df.sort_values("Gap")

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Worker Desire", x=gap_df["Occupation"], y=gap_df["Worker Desire"],
                         marker_color="royalblue"))
    fig.add_trace(go.Bar(name="Expert Capacity", x=gap_df["Occupation"], y=gap_df["Expert Capacity"],
                         marker_color="seagreen"))
    fig.update_layout(title="Worker Desire vs Expert Capacity theo ngành", barmode="group",
                      xaxis_tickangle=-45, height=600)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(gap_df, x="Gap", y="Occupation", orientation="h", color="Gap",
                  color_continuous_scale="RdYlGn", title="Gap (Desire - Capacity) theo ngành",
                  text_auto=".2f")
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("CS Occupations - Gap Detail")
    cs_gap = gap_df[gap_df["Occupation"].isin(CS_ROLES)].sort_values("Gap")
    fig3 = px.bar(cs_gap, x="Gap", y="Occupation", orientation="h", color="Gap",
                  color_continuous_scale="RdYlGn", text_auto=".2f",
                  title="Gap Analysis cho CS Occupations")
    fig3.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig3, use_container_width=True)

    st.info("""
    - **Gap âm lớn nhất**: Database Admin (-1.27), Computer Network Support (-1.03), Web Developers (-1.02) → Worker chưa nhận thức đủ tiềm năng, capacity sẵn sàng.
    - **Gap dương lớn nhất**: Computer Research Scientists (+1.17), Computer Info Systems Managers (+0.75) → Worker muốn nhiều nhưng technology chưa đủ chín.
    """)

elif choice == "5. Human Agency Analysis":
    st.header("Human Agency Analysis")
    st.markdown("**Lý do worker muốn giữ con người trong quy trình (Human Agency Scale 1-5)**")

    agency_cols = ["Reasons for Human Agency - Physical", "Reasons for Human Agency - Control",
                   "Reasons for Human Agency - Domain Knowledge", "Reasons for Human Agency - Empathy",
                   "Reasons for Human Agency - Quality Oversight", "Reasons for Human Agency - Dynamic",
                   "Reasons for Human Agency - Ethical"]
    agency_data = {c.split(" - ")[1]: desires[c].eq("True").sum() for c in agency_cols}
    agency_df = pd.DataFrame({"Reason": list(agency_data.keys()), "Count": list(agency_data.values())})
    agency_df["Percentage"] = (agency_df["Count"] / len(desires) * 100).round(1)
    fig = px.bar(agency_df, x="Reason", y="Percentage", text="Percentage", color="Percentage",
                 color_continuous_scale="purples", title="Lý do worker muốn giữ con người trong loop")
    fig.update_traces(texttemplate="%{text}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Human Agency Scale theo ngành")
    avg_agency = desires.groupby("Occupation (O*NET-SOC Title)")["Human Agency Scale Rating"].mean().sort_values(ascending=False).reset_index()
    fig2 = px.bar(avg_agency.head(20), x="Human Agency Scale Rating", y="Occupation (O*NET-SOC Title)", orientation="h",
                  title="Top 20 ngành có Human Agency cao nhất", color="Human Agency Scale Rating",
                  color_continuous_scale="purples", text_auto=".2f")
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Tác động của Interpersonal Communication đến Human Agency")
    fig3 = px.scatter(desires, x="Interpersonal Communication Requirement", y="Human Agency Scale Rating",
                      color="Automation Desire Rating", hover_data=["Occupation (O*NET-SOC Title)"],
                      title="Interpersonal Communication vs Human Agency",
                      labels={"Interpersonal Communication Requirement": "Interpersonal Requirement (1-5)",
                              "Human Agency Scale Rating": "Human Agency (1-5)"})
    st.plotly_chart(fig3, use_container_width=True)

elif choice == "6. CS Occupations - Deep Dive":
    st.header("CS Occupations - Phân tích chuyên sâu")
    selected_role = st.selectbox("Chọn occupation để phân tích", CS_ROLES)

    col1, col2 = st.columns(2)
    with col1:
        d_sub = desires[desires["Occupation (O*NET-SOC Title)"] == selected_role]
        st.metric("Số tasks khảo sát", len(d_sub))
        if len(d_sub) > 0:
            metrics = {
                "Automation Desire": d_sub["Automation Desire Rating"].mean(),
                "Core Skill": d_sub["Core Skill Rating"].mean(),
                "Job Security": d_sub["Job Security Rating"].mean(),
                "Enjoyment": d_sub["Enjoyment Rating"].mean(),
                "Uncertainty": d_sub["Involved Uncertainty"].mean(),
                "Domain Expertise": d_sub["Domain Expertise Requirement"].mean(),
                "Interpersonal": d_sub["Interpersonal Communication Requirement"].mean(),
                "Human Agency": d_sub["Human Agency Scale Rating"].mean()
            }
            st.dataframe(pd.DataFrame([metrics]).T.rename(columns={0: "Value"}).round(2), use_container_width=True)

    with col2:
        c_sub = capability[capability["Occupation (O*NET-SOC Title)"] == selected_role]
        if len(c_sub) > 0:
            c_metrics = {
                "Automation Capacity": c_sub["Automation Capacity Rating"].mean(),
                "Physical Requirement": c_sub["Physical Action Requirement"].mean(),
                "Uncertainty": c_sub["Involved Uncertainty"].mean(),
                "Domain Expertise": c_sub["Domain Expertise Requirement"].mean(),
                "Interpersonal": c_sub["Interpersonal Communication Requirement"].mean(),
                "Human Agency (Expert)": c_sub["Human Agency Scale Rating"].mean()
            }
            st.dataframe(pd.DataFrame([c_metrics]).T.rename(columns={0: "Value"}).round(2), use_container_width=True)

    if len(d_sub) > 0:
        st.subheader("Lý do Automation Desire")
        reasons = ["Free Time", "Repetitive", "Human Error", "Stress", "Difficulty", "Scale"]
        vals = [d_sub[f"Reasons for Automation Desire - {r}"].eq("True").sum() for r in reasons]
        fig = px.bar(x=reasons, y=vals, text=vals, color=vals, color_continuous_scale="reds",
                     title=f"Lý do Automation Desire - {selected_role}")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Lý do Human Agency")
        agency_items = ["Control", "Domain Knowledge", "Empathy", "Quality Oversight", "Dynamic", "Ethical"]
        agency_vals = [d_sub[f"Reasons for Human Agency - {a}"].eq("True").sum() for a in agency_items]
        fig2 = px.bar(x=agency_items, y=agency_vals, text=agency_vals, color=agency_vals,
                      color_continuous_scale="purples", title=f"Lý do Human Agency - {selected_role}")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("So sánh tất cả CS Occupations")
    cs_metrics = []
    for role in CS_ROLES:
        d_r = desires[desires["Occupation (O*NET-SOC Title)"] == role]
        c_r = capability[capability["Occupation (O*NET-SOC Title)"] == role]
        if len(d_r) > 0 and len(c_r) > 0:
            cs_metrics.append({
                "Occupation": role,
                "Desire": d_r["Automation Desire Rating"].mean(),
                "Capacity": c_r["Automation Capacity Rating"].mean(),
                "Uncertainty": d_r["Involved Uncertainty"].mean(),
                "Domain Expertise": d_r["Domain Expertise Requirement"].mean(),
                "Interpersonal": d_r["Interpersonal Communication Requirement"].mean(),
                "Human Agency": d_r["Human Agency Scale Rating"].mean()
            })
    cs_df = pd.DataFrame(cs_metrics).round(2)
    fig3 = px.scatter(cs_df, x="Desire", y="Capacity", size="Human Agency", color="Occupation",
                      hover_data=["Uncertainty", "Domain Expertise"],
                      title="CS Occupations: Desire vs Capacity (size = Human Agency)")
    fig3.add_hline(y=3, line_dash="dash", line_color="gray", annotation_text="Capacity=3")
    fig3.add_vline(x=3, line_dash="dash", line_color="gray", annotation_text="Desire=3")
    st.plotly_chart(fig3, use_container_width=True)

elif choice == "7. LLM Usage & AI Readiness":
    st.header("LLM Usage & AI Readiness")
    st.markdown("**Mức độ sẵn sàng ứng dụng AI trong lực lượng lao động CS**")

    st.subheader("LLM Use in Work Distribution")
    llm_counts = metadata["LLM Use in Work"].value_counts().reset_index()
    llm_counts.columns = ["Level", "Count"]
    fig = px.bar(llm_counts, x="Level", y="Count", text="Count", color="Count",
                 color_continuous_scale="blues", title="Phân bố mức độ sử dụng LLM trong công việc")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("AI Attitude Distribution")
    attitudes = ["AI Tedious Work Attitude", "AI Job Importance Attitude",
                 "AI Daily Interest Attitude", "AI Suffering Attitude"]
    for att in attitudes:
        col = st.columns([1, 3])
        with col[0]:
            st.markdown(f"**{att}**")
        with col[1]:
            counts = metadata[att].value_counts()
            fig = px.pie(values=counts.values, names=counts.index, title=att,
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("LLM Usage in CS Occupations")
    cs_meta = metadata[metadata["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]
    llm_by_cs = cs_meta.groupby(["Occupation (O*NET-SOC Title)", "LLM Use in Work"]).size().reset_index(name="Count")
    fig = px.bar(llm_by_cs, x="Occupation (O*NET-SOC Title)", y="Count", color="LLM Use in Work",
                 title="LLM Adoption trong CS Occupations", barmode="stack",
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("LLM Usage by Type (CS Workers)")
    usage_types = ["LLM Usage by Type - Information Access", "LLM Usage by Type - Edit",
                   "LLM Usage by Type - Idea Generation", "LLM Usage by Type - Communication",
                   "LLM Usage by Type - Analysis", "LLM Usage by Type - Decision",
                   "LLM Usage by Type - Coding", "LLM Usage by Type - System Design",
                   "LLM Usage by Type - Data Processing"]
    usage_data = []
    for ut in usage_types:
        ut_name = ut.split(" - ")[1]
        daily = (cs_meta[ut] == "Daily").sum()
        weekly = (cs_meta[ut] == "Weekly").sum()
        monthly = (cs_meta[ut] == "Monthly").sum()
        never = (cs_meta[ut] == "Never").sum() if "Never" in cs_meta[ut].values else 0
        usage_data.append({"Type": ut_name, "Daily": daily, "Weekly": weekly, "Never": never})
    usage_df = pd.DataFrame(usage_data)
    fig = px.bar(usage_df, x="Type", y=["Daily", "Weekly", "Never"], title="Tần suất sử dụng LLM theo loại task trong CS",
                 barmode="group", color_discrete_sequence=["#2E86AB", "#A23B72", "#F18F01"])
    st.plotly_chart(fig, use_container_width=True)

elif choice == "8. Đề xuất AI Agent":
    st.header("Đề xuất ứng dụng AI Agent trong Khoa học Máy tính")
    st.markdown("""
    Dựa trên phân tích 4 bộ dữ liệu (worker desires, expert capability, worker metadata, task metadata),
    tôi đề xuất **6 hướng ứng dụng AI Agent ưu tiên cao** dựa trên:
    - **Gap analysis**: Khoảng cách giữa worker desire và expert capacity
    - **Reason analysis**: Lý do worker muốn/hay không muốn tự động hóa
    - **Readiness**: Mức độ sẵn sàng của worker và technology
    """)

    proposals = [
        {
            "title": "1. AI Agent cho Software Quality Assurance & Testing",
            "capacity": 3.76,
            "desire": 3.23,
            "gap": -0.53,
            "reasons": ["Repetitive", "Human Error", "Scale"],
            "color": "#2E86AB",
            "desc": """
            **Cơ sở dữ liệu**: SQA workers có automation capacity 3.76 (cao), desire 3.23. Lý do chính: repetitive, scale, human error.
            """,
            "applications": [
                "Tự động sinh test case từ requirement specification",
                "Agent tự động chạy regression test và phân tích code coverage",
                "AI Agent phát hiện bug pattern từ lịch sử bug",
                "Self-healing test scripts khi UI thay đổi"
            ]
        },
        {
            "title": "2. AI Agent cho Database Administration",
            "capacity": 3.80,
            "desire": 2.53,
            "gap": -1.27,
            "reasons": ["Repetitive", "Scale", "Human Error"],
            "color": "#A23B72",
            "desc": """
            **Cơ sở dữ liệu**: Khoảng cách lớn nhất trong CS (gap -1.27). Worker chưa nhận thức đủ tiềm năng. Uncertainty thấp (2.13) + Physical thấp (1.2) = task lý tưởng.
            """,
            "applications": [
                "Agent tự động tối ưu query (phát hiện slow query, đề xuất index)",
                "AI DBA Agent - backup, monitoring, scaling, failover tự động",
                "Natural Language to SQL Agent cho non-technical users",
                "Anomaly Detection Agent - phát hiện data bất thường"
            ]
        },
        {
            "title": "3. AI Agent cho Web Development",
            "capacity": 4.09,
            "desire": 3.07,
            "gap": -1.02,
            "reasons": ["Free Time", "Repetitive", "Human Error"],
            "color": "#F18F01",
            "desc": """
            **Cơ sở dữ liệu**: Capacity 4.09 (cao nhất CS), desire 3.07 (gap -1.02). LLM daily usage cao nhất (17 users).
            """,
            "applications": [
                "Agent lập trình front-end từ mockup/figma sang code",
                "AI Code Review Agent - tự động review PR, phát hiện vulnerabilities",
                "Documentation Generation Agent - tự sinh API docs, README",
                "Accessibility Compliance Agent - kiểm tra và sửa lỗi WCAG"
            ]
        },
        {
            "title": "4. AI Agent cho Computer & Info Research Scientists",
            "capacity": 2.60,
            "desire": 3.77,
            "gap": 1.17,
            "reasons": ["Free Time", "Difficulty", "Scale"],
            "color": "#F25F5C",
            "desc": """
            **Cơ sở dữ liệu**: Desire cao nhất CS (3.77) vs Capacity thấp (2.60). Gap dương lớn nhất → demand vượt supply.
            """,
            "applications": [
                "Research Agent - literature review, tổng hợp papers, phát hiện research gaps",
                "Experiment Design Agent - đề xuất thiết kế thí nghiệm, chọn hyperparameters",
                "Code Generation for Research - viết code prototype từ mô tả thuật toán",
                "Reproducibility Agent - kiểm tra và đảm bảo kết quả reproducible"
            ]
        },
        {
            "title": "5. AI Agent cho IT Project Management",
            "capacity": 2.55,
            "desire": 2.86,
            "gap": 0.31,
            "reasons": ["Free Time", "Scale", "Stress"],
            "color": "#247BA0",
            "desc": """
            **Cơ sở dữ liệu**: Interpersonal requirement cao nhất CS (3.82). Task phù hợp: risk assessment, progress tracking, reporting.
            """,
            "applications": [
                "Agent lập kế hoạch dự án - WBS, phân bổ resource, critical path analysis",
                "Risk Monitoring Agent - phát hiện sớm risks từ progress data",
                "Status Report Generator - tổng hợp từ Jira, Slack, git commits",
                "Meeting Assistant Agent - ghi chú, action items, follow-up"
            ]
        },
        {
            "title": "6. AI Agent cho Network & Systems Administration",
            "capacity": 3.42,
            "desire": 3.65,
            "gap": 0.23,
            "reasons": ["Repetitive", "Human Error", "Scale"],
            "color": "#70C1B3",
            "desc": """
            **Cơ sở dữ liệu**: Desire 3.65 (rất cao), Capacity 3.42. Cả 3 lý do (repetitive 29.4%, human error 29.4%, scale 29.4%) đều cao.
            """,
            "applications": [
                "Self-healing Network Agent - phát hiện và tự khắc phục sự cố",
                "Security Incident Response Agent - intrusion detection, tự động isolate",
                "Capacity Planning Agent - dự báo resource usage, đề xuất scaling",
                "Config Management Agent - kiểm tra và sửa configuration drift"
            ]
        }
    ]

    for p in proposals:
        with st.container():
            st.subheader(p["title"])
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Expert Capacity", p["capacity"])
            col2.metric("Worker Desire", p["desire"])
            col3.metric("Gap", f"{p['gap']:+}")
            col4.markdown(f"**Lý do chính**: " + ", ".join(p["reasons"]))
            st.markdown(p["desc"])
            for app in p["applications"]:
                st.markdown(f"- {app}")
            st.divider()

    st.header("Kiến trúc AI Agent đề xuất")
    st.markdown("""
    ```
    ┌──────────────────────────────────────────────┐
    │                   Human                       │
    │  (Domain Expert - Quality Oversight - Control)│
    └──────────────────┬───────────────────────────┘
                       │  Feedback / Approval
                       ▼
    ┌──────────────────────────────────────────────┐
    │           Orchestrator Agent                  │
    │  (Task decomposition, Planning, Monitoring)  │
    └──┬──────────┬──────────┬──────────┬──────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
    ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐
    │Code  │ │Test  │ │Doc   │ │Analysis  │
    │Agent │ │Agent │ │Agent │ │Agent     │
    └──────┘ └──────┘ └──────┘ └──────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
    ┌──────────────────────────────────────────────┐
    │         Tool Layer (APIs, DB, Cloud, Git)    │
    └──────────────────────────────────────────────┘
    ```
    """)

    st.header("Nguyên tắc thiết kế")
    col1, col2 = st.columns(2)
    with col1:
        st.success("**Full automation** cho tasks có Capacity > 4.0 (Web Dev, DBA)")
        st.success("**Progressive autonomy** - từ suggest → auto dựa trên trust")
    with col2:
        st.warning("**Human-in-the-loop** cho Uncertainty > 3.0 hoặc Domain Expertise > 3.5")
        st.warning("**Transparent reasoning** - agent giải thích được quyết định")
