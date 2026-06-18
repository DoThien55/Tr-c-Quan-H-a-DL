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

    col1, col2, col3 = st.columns(3)
    col1.metric("Worker Desire", f"{len(desires):,}")
    col2.metric("Expert Capacity", f"{len(capability):,}")
    col3.metric("CS Occupations", len(CS_ROLES))

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
    st.title("Đề xuất AI Agent theo từng ngành trong CS")
    st.markdown("Mỗi ngành trong Khoa học Máy tính sẽ phù hợp với một hoặc nhiều AI Agent khác nhau, dựa trên nhu cầu và khả năng tự động hóa.")

    recommendations = [
        {
            "occupation": "Computer Programmers",
            "desire": 2.93, "capacity": 3.84, "gap": -0.91,
            "agents": ["Code Generation Agent", "Code Review Agent", "Documentation Agent"],
            "reason": "Lập trình viên viết đi viết lại code boilerplate, cần review code và sinh tài liệu. AI Agent giúp tăng tốc độ lập trình và giảm lỗi.",
            "icon": "💻"
        },
        {
            "occupation": "Software Quality Assurance Analysts and Testers",
            "desire": 3.23, "capacity": 3.76, "gap": -0.53,
            "agents": ["Test Automation Agent", "Bug Detection Agent", "Test Case Generator"],
            "reason": "Viết và chạy test case là công việc lặp lại, tốn thời gian. AI Agent có thể tự sinh test, phát hiện bug và chạy regression.",
            "icon": "✅"
        },
        {
            "occupation": "Web Developers",
            "desire": 3.07, "capacity": 4.09, "gap": -1.02,
            "agents": ["Web Dev Agent", "UI-to-Code Agent", "Accessibility Agent"],
            "reason": "Chuyển thiết kế Figma sang code, kiểm tra accessibility và sinh tài liệu web. AI làm rất tốt (4.09/5) nhưng developer chưa tận dụng hết.",
            "icon": "🌐"
        },
        {
            "occupation": "Database Administrators",
            "desire": 2.53, "capacity": 3.80, "gap": -1.27,
            "agents": ["DBA Agent", "Query Optimization Agent", "NL2SQL Agent"],
            "reason": "Tối ưu query, backup, monitoring là công việc lặp lại và dễ sai sót. AI có thể làm hoàn toàn tự động (3.80/5) nhưng DBA chưa muốn (2.53/5).",
            "icon": "🗄️"
        },
        {
            "occupation": "Network and Computer Systems Administrators",
            "desire": 3.65, "capacity": 3.42, "gap": +0.23,
            "agents": ["Network Admin Agent", "Self-healing Agent", "Security Response Agent"],
            "reason": "Quản trị mạng cần giám sát 24/7, phát hiện và xử lý sự cố. AI Agent giúp tự động hóa các tác vụ lặp lại và phản ứng nhanh với sự cố.",
            "icon": "🌍"
        },
        {
            "occupation": "Computer Network Support Specialists",
            "desire": 2.71, "capacity": 3.74, "gap": -1.03,
            "agents": ["Helpdesk Agent", "Troubleshooting Agent", "Network Monitoring Agent"],
            "reason": "Hỗ trợ người dùng về mạng là công việc lặp lại. AI Agent có thể chẩn đoán và hướng dẫn sửa lỗi cơ bản, giảm tải cho nhân viên.",
            "icon": "📞"
        },
        {
            "occupation": "Computer User Support Specialists",
            "desire": 2.95, "capacity": 3.89, "gap": -0.94,
            "agents": ["IT Helpdesk Agent", "FAQ Bot", "Remote Troubleshooting Agent"],
            "reason": "Hỗ trợ người dùng cuối giải quyết các vấn đề máy tính. AI Agent có thể trả lời tự động các câu hỏi thường gặp và chẩn đoán lỗi cơ bản.",
            "icon": "🖥️"
        },
        {
            "occupation": "Computer and Information Research Scientists",
            "desire": 3.77, "capacity": 2.60, "gap": +1.17,
            "agents": ["Research Agent", "Literature Review Agent", "Experiment Design Agent"],
            "reason": "Nhà nghiên cứu mong muốn tự động hóa nhất (3.77/5) nhưng công nghệ hiện tại chưa đáp ứng được (2.60/5). Agent hỗ trợ tìm tài liệu, thiết kế thí nghiệm.",
            "icon": "🔬"
        },
        {
            "occupation": "Computer Systems Analysts",
            "desire": 2.60, "capacity": 3.41, "gap": -0.81,
            "agents": ["Requirement Analysis Agent", "System Design Agent", "Documentation Agent"],
            "reason": "Phân tích hệ thống cần thu thập yêu cầu, thiết kế và lập tài liệu. AI Agent hỗ trợ phân tích dữ liệu và tạo tài liệu tự động.",
            "icon": "📊"
        },
        {
            "occupation": "Computer Systems Engineers/Architects",
            "desire": 3.23, "capacity": 3.04, "gap": +0.19,
            "agents": ["Architecture Review Agent", "Design Validation Agent", "Tech Stack Advisor"],
            "reason": "Kiến trúc sư hệ thống cần đánh giá và tư vấn giải pháp. AI Agent hỗ trợ đánh giá thiết kế, đề xuất công nghệ phù hợp.",
            "icon": "🏗️"
        },
        {
            "occupation": "Information Security Analysts",
            "desire": 3.18, "capacity": 3.00, "gap": +0.18,
            "agents": ["Security Monitoring Agent", "Threat Detection Agent", "Compliance Checker"],
            "reason": "Bảo mật thông tin cần giám sát liên tục và phát hiện xâm nhập. AI Agent giúp phát hiện bất thường và kiểm tra tuân thủ quy định.",
            "icon": "🔒"
        },
        {
            "occupation": "Information Technology Project Managers",
            "desire": 2.86, "capacity": 2.55, "gap": +0.31,
            "agents": ["Project Planning Agent", "Risk Monitoring Agent", "Report Generator"],
            "reason": "Quản lý dự án cần lập kế hoạch, theo dõi rủi ro và báo cáo. AI Agent hỗ trợ phân tích tiến độ và tự động tạo báo cáo.",
            "icon": "📋"
        },
        {
            "occupation": "Computer and Information Systems Managers",
            "desire": 3.31, "capacity": 2.56, "gap": +0.75,
            "agents": ["Dashboard Agent", "Resource Planning Agent", "Decision Support Agent"],
            "reason": "Quản lý hệ thống thông tin cần tổng hợp báo cáo và hỗ trợ ra quyết định. AI Agent giúp phân tích dữ liệu và đề xuất phương án.",
            "icon": "📈"
        }
    ]

    for r in recommendations:
        with st.container():
            st.subheader(f"{r['icon']} {r['occupation']}")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.metric("Gap", f"{r['gap']:+}")
                st.markdown(f"**Muốn**: {r['desire']}/5 • **Được**: {r['capacity']}/5")
            with col2:
                st.markdown(f"**🤖 AI Agent phù hợp:** {', '.join(r['agents'])}")
                st.markdown(f"**💡 Giải thích:** {r['reason']}")
            st.divider()

   
