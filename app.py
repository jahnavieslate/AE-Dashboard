
import streamlit as st
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="After Effects Employee Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ==========================================
# 2. CUSTOM DASHBOARD DESIGN
# ==========================================

st.markdown("""
<style>
    .stApp {
        background-color: #111827;
        color: white;
    }

    h1, h2, h3, p, label {
        color: white;
    }

    div[data-testid="stMetric"] {
        background-color: #1F2937;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #374151;
    }

    div[data-testid="stMetricValue"] {
        color: #60A5FA;
    }

    div[data-testid="stMetricLabel"] {
        color: #D1D5DB;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. EMPLOYEE DATA
# ==========================================

data = [
    ["Nivrutha", 11, 285, "28:27:30", "23:26:06", "5:01:24", 82, 18, 41],
    ["Anil", 22.5, 273.5, "27:34:30", "27:44:46", "0:00:00", 101, -1, 50],
    ["Likhith", 6.5, 289.5, "26:42:30", "28:30:34", "0:00:00", 107, -7, 53],
    ["Balaji", 16, 280, "28:31:30", "23:08:36", "5:22:54", 81, 19, 41],
    ["Sudhakar", 44.5, 251.5, "22:48:45", "16:58:35", "5:50:10", 74, 26, 37],
    ["Srinivas", 24, 271, "27:25:26", "22:04:44", "5:20:42", 81, 19, 40],
    ["Vijay", 10, 286, "28:47:30", "29:57:53", "0:00:00", 104, -4, 52],
    ["Mohammad Farhan Ali", 2.5, 83.5, "7:18:45", "6:45:04", "0:33:41", 92, 8, 46],
    ["Irfan", 15, 107, "17:19:30", "5:22:11", "11:57:19", 31, 69, 15],
    ["Aravind", 28, 268, "27:15:00", "9:37:18", "17:37:42", 35, 65, 18],
    ["Prajwal", 0, 10, "1:15:00", "0:57:20", "0:17:40", 76, 24, 38],
    ["Abhishek", 32.5, 263.5, "26:42:00", "6:25:36", "20:16:24", 24, 76, 12],
    ["Santhosh Chary P", 37, 259, "26:38:30", "8:50:27", "17:48:03", 33, 67, 17]
]

columns = [
    "Employee Name",
    "Leaves",
    "Total Working Days",
    "Given Target",
    "Completed Target",
    "Still Pending",
    "Productivity (%)",
    "Pending Percentage (%)",
    "Productivity at 50 (%)"
]

df = pd.DataFrame(data, columns=columns)

# ==========================================
# 4. DASHBOARD HEADER
# ==========================================

st.title("🎬 AFTER EFFECTS")
st.subheader("Employee Performance & Hike Dashboard")

st.caption(
    "Monitor employee productivity, target completion, "
    "pending work and performance reviews."
)

st.divider()

# ==========================================
# 5. TEAM OVERVIEW
# ==========================================

st.header("📊 Team Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Employees",
    len(df)
)

col2.metric(
    "Average Productivity",
    f"{df['Productivity (%)'].mean():.1f}%"
)

col3.metric(
    "Above 100% Target",
    int((df["Productivity (%)"] > 100).sum())
)

col4.metric(
    "Below 50% Productivity",
    int((df["Productivity (%)"] < 50).sum())
)

st.divider()

# ==========================================
# 6. EMPLOYEE PERFORMANCE TABLE
# ==========================================

st.header("👥 Employee Performance List")

search_name = st.text_input(
    "🔍 Search employee by name",
    placeholder="Enter employee name..."
)

filtered_df = df[
    df["Employee Name"].str.contains(
        search_name,
        case=False,
        na=False
    )
]

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 7. SELECT AN EMPLOYEE
# ==========================================

st.divider()

st.header("👤 Individual Employee Dashboard")

employee = st.selectbox(
    "Select an employee to view their performance",
    df["Employee Name"].tolist()
)

person = df[
    df["Employee Name"] == employee
].iloc[0]

st.markdown(f"### Performance Report: {employee}")

# ==========================================
# 8. INDIVIDUAL PERFORMANCE CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Productivity",
    f"{person['Productivity (%)']}%"
)

col2.metric(
    "Pending Percentage",
    f"{person['Pending Percentage (%)']}%"
)

col3.metric(
    "Leaves Taken",
    str(person["Leaves"])
)

col4.metric(
    "Working Days",
    str(person["Total Working Days"])
)

# ==========================================
# 9. TARGET AND COMPLETION DETAILS
# ==========================================

st.divider()

st.subheader("⏱️ Work Target Details")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Given Target",
    person["Given Target"]
)

col2.metric(
    "Completed Work",
    person["Completed Target"]
)

col3.metric(
    "Still Pending",
    person["Still Pending"]
)

# ==========================================
# 10. PRODUCTIVITY PROGRESS
# ==========================================

st.divider()

st.subheader("📈 Productivity Progress")

productivity = int(person["Productivity (%)"])

st.progress(
    min(max(productivity, 0), 100)
)

st.write(f"**Reported Productivity: {productivity}%**")

if productivity >= 100:
    st.success("The employee has achieved or exceeded the target.")
elif productivity >= 75:
    st.info("The employee has achieved at least 75% of the target.")
elif productivity >= 50:
    st.warning("The employee has achieved between 50% and 74% of the target.")
else:
    st.error("The employee has completed less than 50% of the target.")

# ==========================================
# 11. WORK HOURS COMPARISON CHART
# ==========================================

def time_to_hours(time_string):
    hours, minutes, seconds = map(
        int, time_string.split(":")
    )

    return (
        hours
        + minutes / 60
        + seconds / 3600
    )


st.divider()

st.subheader("📊 Given Target vs Completed Work")

chart_data = pd.DataFrame({
    "Work Category": [
        "Given Target",
        "Completed Work",
        "Still Pending"
    ],
    "Hours": [
        time_to_hours(person["Given Target"]),
        time_to_hours(person["Completed Target"]),
        time_to_hours(person["Still Pending"])
    ]
})

st.bar_chart(
    chart_data,
    x="Work Category",
    y="Hours",
    color="#60A5FA"
)

# ==========================================
# 12. TEAM PRODUCTIVITY COMPARISON
# ==========================================

st.divider()

st.header("🏆 Team Productivity Comparison")

team_chart = df[
    ["Employee Name", "Productivity (%)"]
].set_index("Employee Name")

st.bar_chart(
    team_chart,
    color="#34D399"
)

# ==========================================
# 13. TOP PERFORMERS
# ==========================================

st.divider()

st.subheader("🌟 Employee Productivity Ranking")

ranking = df[
    ["Employee Name", "Productivity (%)"]
].sort_values(
    by="Productivity (%)",
    ascending=False
).reset_index(drop=True)

ranking.index = ranking.index + 1
ranking.index.name = "Rank"

st.dataframe(
    ranking,
    use_container_width=True
)

# ==========================================
# 14. H I K E  R E V I E W
# ==========================================

st.divider()

st.header("💼 Employee Hike Review")

st.write(f"**Employee Name:** {employee}")

st.write(
    f"**Productivity at 50% scale:** "
    f"{person['Productivity at 50 (%)']}%"
)

st.write(
    f"**Completed Target:** "
    f"{person['Completed Target']}"
)

st.write(
    f"**Pending Target:** "
    f"{person['Still Pending']}"
)

review_status = st.selectbox(
    "Performance Review Status",
    [
        "Not Reviewed",
        "Under Review",
        "Recommended for Hike",
        "No Hike Recommended Yet"
    ]
)

hike_percentage = st.number_input(
    "Proposed Hike Percentage (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0
)

comments = st.text_area(
    "Manager's Review Comments",
    placeholder=(
        "Enter work quality, creativity, "
        "project contributions, consistency and feedback..."
    )
)

if st.button("Generate Review Summary"):
    st.subheader("Review Summary")

    st.write(f"**Employee:** {employee}")
    st.write(f"**Productivity:** {productivity}%")
    st.write(f"**Review Status:** {review_status}")
    st.write(f"**Proposed Hike:** {hike_percentage:.1f}%")
    st.write(f"**Manager Comments:** {comments or 'No comments entered'}")

    st.info(
        "This is a proposed review summary, not an approved salary decision."
    )

# ==========================================
# 15. FOOTER
# ==========================================

st.divider()

st.caption(
    "After Effects Employee Dashboard | "
    "Performance figures are based on the supplied dataset."
)

st.caption(
    "Review work quality, responsibilities, project complexity "
    "and consistency alongside productivity before making hike decisions."
)
