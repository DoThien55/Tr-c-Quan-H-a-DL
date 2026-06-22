import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os

st.set_page_config(page_title="AI Agent trong CS", layout="wide")

# --- ĐOẠN CSS ĐỂ PHÓNG TO TOÀN BỘ CHỮ TRÊN STREAMLIT ---
st.markdown("""
<style>
    /* Phóng to chữ văn bản bình thường (Markdown, text) */
    html, body, [class*="st-"] p, li {
        font-size: 22px !important;
    }
    
    /* Phóng to các tiêu đề con (Subheader) */
    h3 {
        font-size: 30px !important;
    }

    /* Phóng to phần con số bự trong thẻ st.metric */
    [data-testid="stMetricValue"] {
        font-size: 45px !important;
        font-weight: bold !important;
    }
    
    /* Phóng to chữ tiêu đề nhỏ phía trên con số trong thẻ st.metric */
    [data-testid="stMetricLabel"] {
        font-size: 24px !important;
    }
</style>
""", unsafe_allow_html=True)


DATA_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    # Thêm bọc try-except để tránh app bị sập đỏ màn hình nếu file dữ liệu gặp sự cố
    try:
        d = pd.read_csv(os.path.join(DATA_DIR, "domain_worker_desires.csv"))
        c = pd.read_csv(os.path.join(DATA_DIR, "expert_rated_technological_capability.csv"))
        return d, c
    except FileNotFoundError:
        st.error("Không tìm thấy các file dữ liệu CSV trong thư mục. Vui lòng kiểm tra lại!")
        st.stop()

desires, capability = load_data()

CS_ROLES = [
    "Computer Programmers", "Computer Systems Analysts",
    "Computer Systems Engineers/Architects", "Computer Network Support Specialists",
    "Computer User Support Specialists", "Computer and Information Systems Managers",
    "Computer and Information Research Scientists", "Software Quality Assurance Analysts and Testers",
    "Web Developers", "Database Administrators", "Information Security Analysts",
    "Information Technology Project Managers", "Network and Computer Systems Administrators"
]

# Lọc riêng bảng dữ liệu mong muốn của nhân viên, chỉ giữ lại 13 ngành Khoa học máy tính
cs_desires_filtered = desires[desires["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]
# Tính điểm số mong muốn tự động hóa trung bình cho riêng 13 ngành IT này thôi
avg_desire = cs_desires_filtered.groupby("Occupation (O*NET-SOC Title)")["Automation Desire Rating"].mean()

# Lọc riêng bảng dữ liệu đánh giá của chuyên gia, chỉ giữ lại 13 ngành Khoa học máy tính
cs_capability_filtered = capability[capability["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]
# Tính điểm số năng lực tự động hóa thực tế trung bình cho riêng 13 ngành IT này thôi
avg_cap = cs_capability_filtered.groupby("Occupation (O*NET-SOC Title)")["Automation Capacity Rating"].mean()

# Tìm những ngành nghề có mặt ở cả 2 file dữ liệu để đối chiếu (ở đây sẽ ra chính xác 13 ngành IT)
common = avg_desire.index.intersection(avg_cap.index)

# Gộp các điểm số trung bình tính được ở trên thành một bảng Excel mới để dễ so sánh chênh lệch
gap_df = pd.DataFrame({"Occupation": common, "Worker Desire": avg_desire[common].values,
                       "Expert Capacity": avg_cap[common].values})
# Tính điểm lệch (Gap) = (Điểm nhân viên thèm muốn) TRỪ ĐI (Điểm công nghệ thực tế làm được) và làm tròn 2 chữ số thập phân
gap_df["Gap"] = (gap_df["Worker Desire"] - gap_df["Expert Capacity"]).round(2)
# Sắp xếp điểm lệch từ thấp đến cao để chuẩn bị vẽ biểu đồ
cs_gap = gap_df.sort_values("Gap")

# Khai báo tên của 4 trang nội dung mà người dùng có thể bấm vào xem
pages = ["Tổng quan", "Gap Analysis", "CS Deep Dive", "Đề xuất AI Agent"]
# Hiện ra các nút tròn (Radio button) để người dùng tích chọn trang muốn xem, kết quả chọn lưu vào biến 'choice'
choice = st.sidebar.radio("Chọn", pages)

if choice == "Tổng quan":
    st.title("AI Agent trong Khoa học Máy tính")
    
    # Lọc dữ liệu chuẩn cho khối ngành công nghệ
    cs_desires = desires[desires["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]
    cs_capability = capability[capability["Occupation (O*NET-SOC Title)"].isin(CS_ROLES)]

    st.markdown("**Dataset**: Phân tích các tác vụ từ người lao động và đánh giá từ chuyên gia AI")

    col1, col2, col3 = st.columns(3)
    col1.metric("Khảo sát Người lao động", f"{len(cs_desires):,}")
    col2.metric("Đánh giá từ Chuyên gia", f"{len(cs_capability):,}")
    col3.metric("Số Ngành IT Phân tích", len(CS_ROLES))

    st.divider()

    # ==========================================
    # BIỂU ĐỒ 1: LÝ DO MUỐN DÙNG AI
    # ==========================================
    st.subheader("1. Tại sao kỹ sư IT khao khát dùng AI?")
    st.markdown("Thay vì ôm việc, người lao động muốn giao việc cho AI để giải quyết những nỗi đau thực tế sau:")

    reason_map = {
        "Reasons for Automation Desire - Free Time": "Giải phóng thời gian rảnh rỗi  ",
        "Reasons for Automation Desire - Scale": "Giúp xử lý lượng dữ liệu khổng lồ  ",
        "Reasons for Automation Desire - Human Error": "Tránh con người làm sai sót lặt vặt  ",
        "Reasons for Automation Desire - Repetitive": "Thoát khỏi việc copy-paste lặp đi lặp lại  ",
        "Reasons for Automation Desire - Stress": "Giảm bớt áp lực, căng thẳng  ",
        "Reasons for Automation Desire - Difficulty": "Đỡ phải tính toán quá phức tạp  "
    }

    rc = {label: int(cs_desires[col].sum()) for col, label in reason_map.items()}
    rdf = pd.DataFrame({"Reason": list(rc.keys()), "Count": list(rc.values())})
    rdf["%"] = (rdf["Count"] / len(cs_desires) * 100).round(1)
    
    rdf = rdf.sort_values("Count").reset_index(drop=True)
    fig1 = px.bar(rdf, x="Count", y="Reason", orientation="h", color="Count", color_continuous_scale="Blues")
    
    fig1.update_traces(
        texttemplate="%{x} người (%{customdata}%)", 
        textposition="outside",
        customdata=rdf[["%"]], 
        textfont=dict(color="black", size=16)
    ) 
    
    fig1.update_layout(
        title="Top lý do muốn tự động hóa công việc",
        title_font_size=22, height=550, margin=dict(r=250)
    )
    fig1.update_yaxes(title="", tickfont=dict(size=18, color="black"))
    fig1.update_xaxes(title="Số lượng người", tickfont=dict(size=18, color="black"), title_font=dict(size=18, color="black"))
    
    st.plotly_chart(fig1, use_container_width=True, theme=None)

    # ==========================================
    # BIỂU ĐỒ 2: LÝ DO KHÔNG DÁM GIAO 100% CHO AI
    # ==========================================
    st.subheader("2. Tại sao lại sợ giao phó 100% cho AI?")
    st.markdown("Dù AI rất giỏi, nhưng con người vẫn kiên quyết phải giữ lại quyền can thiệp vì những lo lắng sau:")

    agency_map = {
        "Reasons for Human Agency - Quality Oversight": "Phải có người duyệt chất lượng cuối cùng  ",
        "Reasons for Human Agency - Control": "Sợ mất quyền kiểm soát hệ thống  ",
        "Reasons for Human Agency - Ethical": "Ai sẽ chịu trách nhiệm pháp lý/đạo đức khi có lỗi  ",
        "Reasons for Human Agency - Domain Knowledge": "AI không hiểu sâu ngữ cảnh kinh doanh công ty  ",
        "Reasons for Human Agency - Dynamic": "Khách hàng thay đổi liên tục, AI không linh hoạt bằng  ",
        "Reasons for Human Agency - Empathy": "Cần sự thấu cảm, dỗ dành khách hàng  "
    }

    ac = {label: int(cs_desires[col].sum()) for col, label in agency_map.items()}
    adf = pd.DataFrame({"Reason": list(ac.keys()), "Count": list(ac.values())})
    adf["%"] = (adf["Count"] / len(cs_desires) * 100).round(1)
    
    adf = adf.sort_values("Count", ascending=True).reset_index(drop=True)

    fig2 = px.bar(adf, x="Count", y="Reason", color="Count", color_continuous_scale="Reds")
    
    fig2.update_traces(
        texttemplate="%{x} người (%{customdata}%)", 
        textposition="outside",
        customdata=adf[["%"]], 
        textfont=dict(color="black", size=16)
    )
    
    fig2.update_layout(
        title="Top lý do kiên quyết phải giữ lại con người",
        title_font_size=22, height=550, margin=dict(r=250)
    )
    fig2.update_yaxes(title="", tickfont=dict(size=20, color="black"))
    fig2.update_xaxes(title="Số lượng người", tickfont=dict(size=18, color="black"), title_font=dict(size=18, color="black"))
    
    st.plotly_chart(fig2, use_container_width=True, theme=None)

elif choice == "Gap Analysis":
    st.title("Phân tích Độ Lệch: Giữa 'Giấc Mơ' và 'Thực Tế'")
    st.markdown("""
    Lấy **Mức độ nhân viên muốn** trừ đi **Năng lực thực tế AI làm được**. 
    Kết quả sinh ra 2 trường hợp:
    * 🛑 **Độ lệch Âm (Vùng E Dè):** AI làm dư sức, nhưng con người sợ hãi không dám giao việc.
    * 🟢 **Độ lệch Dương (Vùng Chờ Đợi):** Con người rất khát khao tự động hóa, nhưng AI hiện tại chưa đáp ứng được.
    """)

    fig2 = px.bar(cs_gap, x="Gap", y="Occupation", color="Gap", color_continuous_scale="RdYlGn")
    
    fig2.update_traces(
        texttemplate="%{x:.2f}", 
        textposition="outside",
        textfont=dict(size=16, color="black")
    )
    fig2.update_layout(height=750, margin=dict(r=100))
    fig2.update_yaxes(title="", categoryorder="total ascending", tickfont=dict(size=18, color="black"))
    fig2.update_xaxes(title="Điểm Gap (Mong muốn - Năng lực)", tickfont=dict(size=18, color="black"), title_font=dict(size=18, color="black"))
    st.plotly_chart(fig2, use_container_width=True)

    
    st.markdown("---")
    st.subheader("Bản Đồ Định Vị")
    st.markdown("""
    Bản đồ này chia làm 4 khu vực. Trục ngang là sức mạnh của AI, trục dọc là khao khát của con người. 
    Chấm tròn (ngành nghề) rơi vào góc nào sẽ quyết định chiến lược đó:
    """)
    
    cs_gap['Category'] = cs_gap['Gap'].apply(lambda x: 'Nhóm E dè (Đỏ)' if x < 0 else 'Nhóm Chờ đợi (Xanh)')
    
    fig_scatter = px.scatter(
        cs_gap, 
        x="Expert Capacity", 
        y="Worker Desire", 
        color="Category",
        color_discrete_sequence=["#ef553b", "#00cc96"], 
        size=[12]*len(cs_gap), 
        hover_name="Occupation", 
        text="Occupation",
        title="Bản Đồ 4 Góc Phần Tư (Desire vs Capacity)"
    )
    
    # CHỈNH SỬA: Chuẩn hóa đường chia mốc về điểm trung vị 3.5 để phân loại chính xác, trực quan
    mean_cap = 3.5
    mean_des = 3.5
    
    fig_scatter.update_traces(
        marker=dict(line=dict(width=3, color='black')), 
        textposition='top center', 
        textfont=dict(size=16, color="black") 
    )
    
    fig_scatter.add_hline(y=mean_des, line_dash="dash", line_color="black", line_width=2, annotation_text="Mốc trung bình: Mong muốn (3.5)", annotation_font_size=16)
    fig_scatter.add_vline(x=mean_cap, line_dash="dash", line_color="black", line_width=2, annotation_text="Mốc trung bình: Năng lực AI (3.5)", annotation_font_size=16)
    
    fig_scatter.update_layout(
        height=800, 
        font=dict(color="black", size=18), 
        title_font_size=26
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
elif choice == "CS Deep Dive":
    st.title("Phân tích xem nhân viên Ngành Khoa Học Máy Tính nghĩ gì?")
    st.markdown("Nỗi lo lớn nhất của nhân viên các ngành thuộc Khoa Học Máy Tính là gì:")

    role = st.selectbox("Lựa Chọn Nghề Nghiệp:", CS_ROLES)

    diem_gap = cs_gap[cs_gap["Occupation"] == role]["Gap"].values[0]
    diem_muon = avg_desire.get(role, 0)
    diem_may_gioi = avg_cap.get(role, 0)
    d_sub = desires[desires["Occupation (O*NET-SOC Title)"] == role]

    dong_luc = {
        "Muốn có thời gian nghỉ ngơi  ": d_sub["Reasons for Automation Desire - Free Time"].sum(),
        "Việc nhiều quá, làm tay không nổi  ": d_sub["Reasons for Automation Desire - Scale"].sum(),
        "Máy làm sẽ ít sai vặt hơn người  ": d_sub["Reasons for Automation Desire - Human Error"].sum(),
        "Chán phải làm đi làm lại một việc  ": d_sub["Reasons for Automation Desire - Repetitive"].sum(),
        "Công việc hiện tại quá mệt mỏi  ": d_sub["Reasons for Automation Desire - Stress"].sum()
    }
    thich_nhat = max(dong_luc, key=dong_luc.get)

    rao_can = {
        "Sợ máy làm sai, phải có người kiểm tra ": d_sub["Reasons for Human Agency - Quality Oversight"].sum(),
        "Sợ máy tự làm hỏng hệ thống ": d_sub["Reasons for Human Agency - Control"].sum(),
        "Nếu máy sai ai đền? Cần người chịu trách nhiệm ": d_sub["Reasons for Human Agency - Ethical"].sum(),
        "Máy không hiểu tình hình thực tế của công ty ": d_sub["Reasons for Human Agency - Domain Knowledge"].sum()
    }
    so_nhat = max(rao_can, key=rao_can.get)

    st.markdown("---")
    if diem_gap < -0.5:
        nhan_xet = "Nhóm Cẩn Thận (Máy làm dư sức nhưng nhân viên không dám giao)"
        loi_khuyen = "Tuyệt đối không để máy tự làm tự quyết. Phải bắt máy làm nháp, người kiểm tra xong mới được chạy."
    elif diem_gap > 0.5:
        nhan_xet = "Nhóm Mệt Mỏi (Đang làm việc quá sức, rất muốn có máy làm thay)"
        loi_khuyen = "Cứ mạnh dạn giao khoán hết mấy việc lặt vặt cho máy làm để nhân viên được nghỉ ngơi."
    else:
        nhan_xet = "Nhóm Cân Bằng (Biết chia việc hợp lý)"
        loi_khuyen = "Chia việc đôi bên cùng làm. Máy xử lý dữ liệu thô, con người ra quyết định."

    st.subheader(f"Kết quả phân tích nghề: {role}")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Điểm Gap (Mong muốn - Năng lực AI hiện tại)", f"{diem_gap:+.2f}")
        st.write(f"**Điểm nhân viên mong muốn:** {diem_muon:.2f} / 5.0")
        st.write(f"**Điểm năng lực của AI hiện tại:** {diem_may_gioi:.2f} / 5.0")
    
    with col2:
        st.markdown(f"**Nhận xét:  họ thuộc** {nhan_xet}")
        st.markdown(f"**Lý do muốn dùng AI :** {thich_nhat}")
        st.markdown(f"**Lý do sợ giao việc cho AI:** {so_nhat}")
        st.markdown(f"**Lời Khuyên:** {loi_khuyen}")

    # =================================================================
    # CHIA LÀM 2 CỘT SONG SONG ĐỂ BIỂU ĐỒ KHÔNG BỊ TRỘN LẪN MÀU SẮC
    # =================================================================
    st.markdown("---")
    st.subheader("Biểu đồ chi tiết: Động lực thúc đẩy vs Rào cản tâm lý")
    
    df_dong_luc = pd.DataFrame({
        "Lý do": list(dong_luc.keys()),
        "Số người chọn": list(dong_luc.values())
    }).sort_values("Số người chọn", ascending=True)
    
    df_rao_can = pd.DataFrame({
        "Lý do": list(rao_can.keys()),
        "Số người chọn": list(rao_can.values())
    }).sort_values("Số người chọn", ascending=True)
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_muon = px.bar(df_dong_luc, x="Số người chọn", y="Lý do", orientation="h", 
                          title="Các lý do khuyến khích muốn dùng AI",
                          color_discrete_sequence=["#1E88E5"])
        fig_muon.update_traces(texttemplate="%{x} người", textposition="outside", textfont=dict(size=16, color="black"))
        fig_muon.update_layout(height=450, font=dict(size=16, color="black"), margin=dict(r=100))
        fig_muon.update_yaxes(title="")
        st.plotly_chart(fig_muon, use_container_width=True, theme=None)
        
    with chart_col2:
        fig_so = px.bar(df_rao_can, x="Số người chọn", y="Lý do", orientation="h", 
                         title="Các nỗi lo ngăn cản giao việc cho AI",
                         color_discrete_sequence=["#D32F2F"])
        fig_so.update_traces(texttemplate="%{x} người", textposition="outside", textfont=dict(size=16, color="black"))
        fig_so.update_layout(height=450, font=dict(size=16, color="black"), margin=dict(r=100))
        fig_so.update_yaxes(title="")
        st.plotly_chart(fig_so, use_container_width=True, theme=None)

elif choice == "Đề xuất AI Agent":
    st.title("Đề Xuất AI Agent")
    st.markdown("Dựa vào điểm chênh lệch ở trang trước, máy tính sẽ đưa ra lời khuyên xem **nên dùng AI Agent nào**.")

    agent_configs = {
        "Computer Programmers": {
            "agents": ["Code Generation Agent", "Code Review Agent", "Documentation Agent"],
            "reason": "Lập trình viên thường chán nản khi viết đi viết lại những đoạn code cơ bản. Các AI Agent này sẽ giúp viết nháp, tự dò lỗi sai và tự động viết tài liệu giải thích code."
        },
        "Software Quality Assurance Analysts and Testers": {
            "agents": ["Test Automation Agent", "Bug Detection Agent", "Test Case Generator"],
            "reason": "Việc bấm thử phần mềm hàng ngàn lần rất tốn thời gian. AI Agent có thể tự động viết kịch bản test, chạy thử ngầm mỗi đêm và báo cáo lỗi (bug)."
        },
        "Web Developers": {
            "agents": ["Web Dev Agent", "UI-to-Code Agent", "Accessibility Agent"],
            "reason": "Giúp tiết kiệm thời gian bằng cách nhìn vào bản vẽ thiết kế và tự động gõ ra thành code trang web hoàn chỉnh."
        },
        "Database Administrators": {
            "agents": ["DBA Agent", "Query Optimization Agent", "NL2SQL Agent"],
            "reason": "AI đọc dữ liệu siêu nhanh, giúp tìm ra nguyên nhân làm trang web bị chậm, tự động dọn dẹp và sao lưu (backup) dữ liệu mỗi ngày."
        },
        "Network and Computer Systems Administrators": {
            "agents": ["Network Admin Agent", "Self-healing Agent", "Security Response Agent"],
            "reason": "Con người không thể thức 24/7 để canh máy chủ. AI Agent sẽ trực thay, nếu thấy mạng nghẽn thì tự động phân luồng lại cho hết nghẽn."
        },
        "Computer Network Support Specialists": {
            "agents": ["Helpdesk Agent", "Troubleshooting Agent", "Network Monitoring Agent"],
            "reason": "Đỡ đần việc trả lời tin nhắn của nhân viên. AI có thể chẩn đoán mạng lỗi do đâu và chỉ cho người dùng cách khởi động lại."
        },
        "Computer User Support Specialists": {
            "agents": ["IT Helpdesk Agent", "FAQ Bot", "Remote Troubleshooting Agent"],
            "reason": "Tự động hướng dẫn người dùng cuối giải quyết mấy lỗi vặt như quên mật khẩu, máy in không chạy, màn hình xanh."
        },
        "Computer and Information Research Scientists": {
            "agents": ["Research Agent", "Literature Review Agent", "Experiment Design Agent"],
            "reason": "Nhà nghiên cứu mất rất nhiều thời gian đọc tài liệu. AI sẽ đọc hộ hàng ngàn bài báo khoa học, tóm tắt lại và gợi ý cách làm thí nghiệm."
        },
        "Computer Systems Analysts": {
            "agents": ["Requirement Analysis Agent", "System Design Agent", "Documentation Agent"],
            "reason": "Giúp nghe và ghi chép lại yêu cầu của khách hàng, sau đó tự động vẽ sơ đồ thiết kế hệ thống."
        },
        "Computer Systems Engineers/Architects": {
            "agents": ["Architecture Review Agent", "Design Validation Agent", "Tech Stack Advisor"],
            "reason": "Kiểm tra lại xem bản thiết kế hệ thống có bị hổng bảo mật hay không, gợi ý xem nên dùng công nghệ gì thì rẻ và tốt nhất."
        },
        "Information Security Analysts": {
            "agents": ["Security Monitoring Agent", "Threat Detection Agent", "Compliance Checker"],
            "reason": "Đọc hàng triệu lịch sử thao tác trên máy chủ để báo động ngay lập tức nếu có dấu hiệu hacker xâm nhập."
        },
        "Information Technology Project Managers": {
            "agents": ["Project Planning Agent", "Risk Monitoring Agent", "Report Generator"],
            "reason": "Tự động gom số liệu công việc từ các phòng ban, đoán xem dự án có bị trễ hạn không và tự động vẽ báo cáo cho Sếp."
        },
        "Computer and Information Systems Managers": {
            "agents": ["Dashboard Agent", "Resource Planning Agent", "Decision Support Agent"],
            "reason": "Phân tích dữ liệu lớn để giúp Giám đốc quyết định xem nên đầu tư thêm tiền vào đâu, cắt giảm chi phí chỗ nào."
        }
    }

    role = st.selectbox("Lựa chọn nghề nghiệp:", list(agent_configs.keys()))

    config = agent_configs[role]
    
    diem_gap = cs_gap[cs_gap["Occupation"] == role]["Gap"].values[0]
    diem_muon = avg_desire.get(role, 0)
    diem_may_gioi = avg_cap.get(role, 0)

    st.markdown("---")
    st.subheader(f"Các AI Agent phù hợp cho nghề: {role}")

    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.metric("Điểm chênh lệch", f"{diem_gap:+.2f}")
        st.write(f"**Nhân viên mong muốn:** {diem_muon:.2f}/5")
        st.write(f"**AI làm được:** {diem_may_gioi:.2f}/5")
    with col2:
        st.markdown(f"**AI Agent:** {', '.join(config['agents'])}")
        st.markdown(f"**Lý do khuyên dùng:** {config['reason']}")