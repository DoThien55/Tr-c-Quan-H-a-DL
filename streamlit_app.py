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
pages = ["Tổng quan", "Gap Analysis", "CS Deep Dive", "Đề xuất AI Agent"]
choice = st.sidebar.radio("Chọn", pages)

if choice == "Tổng quan":
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

   
