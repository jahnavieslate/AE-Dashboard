import streamlit as st
import pandas as pd
import numpy as np
import re
import io

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SME Employee Hike Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# 2. DASHBOARD STYLE - WHITE TEXT / DARK BACKGROUND
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0e1117 !important;
    color: #ffffff !important;
}

/* General text */
.stApp p,
.stApp label,
.stApp span,
.stApp li,
.stApp strong,
.stMarkdown,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p {
    color: #ffffff !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Dashboard title */
.main-title {
    font-size: 32px;
    font-weight: 800;
    color: #64b5f6 !important;
    text-align: center;
    padding: 12px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #ffffff !important;
    font-size: 16px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #1b2430 !important;
    border: 1px solid #455a64 !important;
    padding: 18px !important;
    border-radius: 12px !important;
}

/* Metric labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #ffffff !important;
    font-weight: 600 !important;
}

/* Metric values */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #64b5f6 !important;
    font-weight: 800 !important;
}

/* Metric delta */
[data-testid="stMetricDelta"] {
    color: #ffffff !important;
}

/* Dataframes */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] *,
[data-testid="stTable"],
[data-testid="stTable"] * {
    color: #ffffff !important;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea {
    background-color: #1b2430 !important;
    color: #ffffff !important;
    border: 1px solid #607d8b !important;
    border-radius: 6px !important;
}

/* Input placeholders */
.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #cfd8dc !important;
    opacity: 1 !important;
}

/* Selectboxes */
[data-baseweb="select"] > div {
    background-color: #1b2430 !important;
    color: #ffffff !important;
    border-color: #607d8b !important;
}

[data-baseweb="select"] *,
[data-baseweb="popover"] *,
[role="option"] {
    color: #ffffff !important;
}

/* File uploader */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] * {
    color: #ffffff !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button,
.stFormSubmitButton button {
    background-color: #1565c0 !important;
    color: #ffffff !important;
    border: 1px solid #64b5f6 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

/* Button hover */
.stButton button:hover,
.stDownloadButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #1976d2 !important;
    color: #ffffff !important;
    border-color: #90caf9 !important;
}

/* Captions */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
    color: #ffffff !important;
}

/* Alerts */
[data-testid="stAlert"],
[data-testid="stAlert"] * {
    color: #ffffff !important;
}

/* Checkboxes */
.stCheckbox label,
.stCheckbox label * {
    color: #ffffff !important;
}

/* Dividers */
hr {
    border-color: #455a64 !important;
}

/* Expanders */
[data-testid="stExpander"] {
    border-color: #455a64 !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #ffffff !important;
}

/* Form containers */
[data-testid="stForm"] {
    background-color: #141b24 !important;
    border: 1px solid #34495e !important;
    border-radius: 10px !important;
    padding: 16px !important;
}

/* Disabled controls */
.stApp input:disabled {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# 3. PROVIDED SME EMPLOYEE DATA
# ============================================================

sme_data = {
    "Employee Name": [
        "Jahnavi Valiveti", "Rakesh Kumar", "Ravali", "Naresh",
        "Pallavi N", "Lahari", "Keerthika", "Sarath Kalyan",
        "Sujeeth Nakka", "Rishita Kumari", "Vaishnavi",
        "Jahnavi D", "Raghavendra"
    ],
    "Leaves": [
        12.5, 42, 22.5, 17, 14, 17, 27, 28, 7.5, 0, 38.5, 15, 23
    ],
    "Total Working Days": [
        283.5, 254, 273.5, 279, 282, 279, 269, 268,
        138.5, 5, 257.5, 281, 273
    ],
    "Given Target": [
        243, 218, 235, 240, 242, 240, 231, 230,
        120, 6, 296, 281, 312
    ],
    "Completed Target": [
        243, 212, 126, 215, 248, 138, 135, 168,
        105, 4, 151, 244, 208
    ],
    "Still Pending": [
        0, 6, 109, 25, -6, 102, 96, 62,
        15, 2, 145, 37, 104
    ]
}

sample_df = pd.DataFrame(sme_data)

PRODUCTIVITY = "Productivity (As per 100 %)"
PRODUCTIVITY_50 = "Productivity (As per 50 %)"

# ============================================================
# 4. UPLOAD SCREEN
# ============================================================

st.markdown(
    '<div class="main-title">📊 SME Employee Productivity & Hike Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Upload your employee performance sheet</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    st.subheader("📁 Upload SME Employee Sheet")

    uploaded_file = st.file_uploader(
        "Upload an Excel or CSV file",
        type=["xlsx", "xls", "csv"]
    )

    st.caption(
        "Required columns: Employee Name, Leaves, Total Working Days, "
        "Given Target, Completed Target and Still Pending."
    )

    st.download_button(
        "⬇️ Download SME Template",
        data=sample_df.to_csv(index=False).encode("utf-8"),
        file_name="SME_employee_template.csv",
        mime="text/csv"
    )

    if st.button(
        "View Dashboard Using Provided SME Data",
        use_container_width=True
    ):
        st.session_state["use_sme_sample"] = True

# ============================================================
# 5. LOAD DATA
# ============================================================

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

    except Exception as error:
        st.error(f"Unable to read the uploaded file: {error}")
        st.stop()

elif st.session_state.get("use_sme_sample", False):
    df = sample_df.copy()

else:
    st.info(
        "Upload your employee sheet or click "
        "'View Dashboard Using Provided SME Data'."
    )
    st.stop()

# ============================================================
# 6. NORMALIZE COLUMN NAMES
# ============================================================

def normalize_column(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


aliases = {
    "employeename": "Employee Name",
    "employee": "Employee Name",
    "name": "Employee Name",
    "leaves": "Leaves",
    "totalworkingdays": "Total Working Days",
    "workingdays": "Total Working Days",
    "giventarget": "Given Target",
    "targetgiven": "Given Target",
    "completedtarget": "Completed Target",
    "targetcompleted": "Completed Target",
    "stillpending": "Still Pending",
    "pending": "Still Pending",
    "productivityasper100": PRODUCTIVITY,
    "productivityasper100percent": PRODUCTIVITY,
    "productivity100": PRODUCTIVITY,
    "productivity": PRODUCTIVITY,
    "productivitypercentage": PRODUCTIVITY,
    "productivityasper50": PRODUCTIVITY_50,
    "productivityasper50percent": PRODUCTIVITY_50,
    "productivity50": PRODUCTIVITY_50
}

df.columns = df.columns.astype(str).str.strip()

rename_map = {}

for column in df.columns:
    key = normalize_column(column)
    if key in aliases:
        rename_map[column] = aliases[key]

df = df.rename(columns=rename_map)
df = df.dropna(how="all").copy()

required_columns = [
    "Employee Name",
    "Leaves",
    "Total Working Days",
    "Given Target",
    "Completed Target"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error("Missing required columns: " + ", ".join(missing_columns))
    st.write("Columns found:", list(df.columns))
    st.stop()

df = df.dropna(subset=["Employee Name"]).copy()
df["Employee Name"] = df["Employee Name"].astype(str).str.strip()

# ============================================================
# 7. CONVERT TARGET DATA TO NUMBERS
# ============================================================

numeric_columns = [
    "Leaves",
    "Total Working Days",
    "Given Target",
    "Completed Target"
]

if "Still Pending" not in df.columns:
    df["Still Pending"] = np.nan

numeric_columns.append("Still Pending")

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

# Calculate pending only when the source value is missing.
missing_pending = df["Still Pending"].isna()

df.loc[missing_pending, "Still Pending"] = (
    df.loc[missing_pending, "Given Target"]
    - df.loc[missing_pending, "Completed Target"]
)

df[numeric_columns] = df[numeric_columns].fillna(0)

# ============================================================
# 8. AUTOMATIC PRODUCTIVITY CALCULATIONS
# ============================================================

# Productivity (100%) = Completed Target / Given Target * 100

df[PRODUCTIVITY] = np.where(
    df["Given Target"] > 0,
    (df["Completed Target"] / df["Given Target"]) * 100,
    0.0
)

# Productivity (50%) = Productivity (100%) / 2

df[PRODUCTIVITY_50] = df[PRODUCTIVITY] / 2

# Pending percentage excludes negative pending values.
df["Pending Percentage"] = np.where(
    df["Given Target"] > 0,
    (
        df["Still Pending"].clip(lower=0)
        / df["Given Target"]
    ) * 100,
    0.0
)

# ============================================================
# 9. DASHBOARD SUMMARY
# ============================================================

st.divider()
st.markdown(
    '<div class="main-title">SME Performance Overview</div>',
    unsafe_allow_html=True
)

if uploaded_file is not None:
    st.caption(f"Uploaded file: {uploaded_file.name}")
else:
    st.caption("Using the provided SME sample data.")

total_employees = len(df)
average_productivity = df[PRODUCTIVITY].mean()
average_productivity_50 = df[PRODUCTIVITY_50].mean()
total_leaves = df["Leaves"].sum()
average_leaves = df["Leaves"].mean()

at_or_above_target = (df[PRODUCTIVITY] >= 100).sum()
below_target = (df[PRODUCTIVITY] < 100).sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Employees", total_employees)
c2.metric("Average Productivity", f"{average_productivity:.2f}%")
c3.metric("Total Leaves", f"{total_leaves:.1f}")
c4.metric("Average Leaves", f"{average_leaves:.1f}")

c5, c6, c7, c8 = st.columns(4)

c5.metric("Total Given Target", f"{df['Given Target'].sum():,.0f}")
c6.metric("Total Completed Target", f"{df['Completed Target'].sum():,.0f}")
c7.metric("At/Above 100% Target", int(at_or_above_target))
c8.metric("Below 100% Target", int(below_target))

c9, c10 = st.columns(2)

c9.metric(
    "Average Productivity (50%)",
    f"{average_productivity_50:.2f}%"
)

c10.metric(
    "Total Pending Target",
    f"{df['Still Pending'].clip(lower=0).sum():,.0f}"
)

# ============================================================
# 10. EMPLOYEE DETAILS TABLE
# ============================================================

st.divider()
st.subheader("🔎 Employee Details")

search_text = st.text_input(
    "Search Employee",
    placeholder="Enter employee name..."
)

filtered_df = df[
    df["Employee Name"].str.contains(
        search_text,
        case=False,
        na=False,
        regex=False
    )
].copy()

display_columns = [
    "Employee Name",
    "Leaves",
    "Total Working Days",
    "Given Target",
    "Completed Target",
    "Still Pending",
    PRODUCTIVITY,
    PRODUCTIVITY_50
]

st.caption(f"Showing {len(filtered_df)} of {len(df)} employees")

st.dataframe(
    filtered_df[display_columns].style.format({
        "Leaves": "{:.1f}",
        "Total Working Days": "{:.1f}",
        "Given Target": "{:,.0f}",
        "Completed Target": "{:,.0f}",
        "Still Pending": "{:,.0f}",
        PRODUCTIVITY: "{:.2f}%",
        PRODUCTIVITY_50: "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# 11. INDIVIDUAL EMPLOYEE PERFORMANCE
# ============================================================

st.divider()
st.subheader("👤 Individual Employee Performance")

selected_employee = st.selectbox(
    "Select an Employee",
    df["Employee Name"].tolist()
)

employee = df[df["Employee Name"] == selected_employee].iloc[0]

st.markdown(f"### {selected_employee}")

a, b, c, d = st.columns(4)

a.metric("Productivity (100%)", f"{employee[PRODUCTIVITY]:.2f}%")
b.metric("Productivity (50%)", f"{employee[PRODUCTIVITY_50]:.2f}%")
c.metric("Leaves", f"{employee['Leaves']:.1f}")
d.metric("Working Days", f"{employee['Total Working Days']:.1f}")

x, y, z = st.columns(3)

x.metric("Given Target", f"{employee['Given Target']:,.0f}")
y.metric("Completed Target", f"{employee['Completed Target']:,.0f}")
z.metric("Still Pending", f"{employee['Still Pending']:,.0f}")

# ============================================================
# 12. INDIVIDUAL TARGET CHART
# ============================================================

st.divider()
st.subheader("📊 Given Target vs Completed Target")

target_chart = pd.DataFrame({
    "Target Type": ["Given Target", "Completed Target"],
    "Target": [
        employee["Given Target"],
        employee["Completed Target"]
    ]
}).set_index("Target Type")

st.bar_chart(
    target_chart,
    y="Target",
    color="#64b5f6"
)

# ============================================================
# 13. TEAM PRODUCTIVITY CHART
# ============================================================

st.divider()
st.subheader("📈 SME Team Productivity")

productivity_chart = filtered_df[
    ["Employee Name", PRODUCTIVITY]
].set_index("Employee Name")

st.bar_chart(
    productivity_chart,
    y=PRODUCTIVITY,
    color="#26a69a"
)

st.caption(
    "100% means the target was achieved. Values above 100% mean "
    "the employee exceeded the target."
)

# ============================================================
# 14. PENDING TARGET CHART
# ============================================================

st.divider()
st.subheader("⏳ Employee Pending Targets")

pending_chart = filtered_df[
    ["Employee Name", "Still Pending"]
].set_index("Employee Name")

st.bar_chart(
    pending_chart,
    y="Still Pending",
    color="#ffb74d"
)

st.caption(
    "Negative pending values indicate that the employee exceeded "
    "the given target."
)

# ============================================================
# 15. PRODUCTIVITY RANKING
# ============================================================

st.divider()
st.subheader("🏆 SME Employee Productivity Ranking")

ranking_df = df[
    ["Employee Name", PRODUCTIVITY, PRODUCTIVITY_50]
].sort_values(
    PRODUCTIVITY,
    ascending=False
).reset_index(drop=True)

ranking_df.index = ranking_df.index + 1
ranking_df.index.name = "Rank"

st.dataframe(
    ranking_df.style.format({
        PRODUCTIVITY: "{:.2f}%",
        PRODUCTIVITY_50: "{:.2f}%"
    }),
    use_container_width=True
)

# ============================================================
# 16. HIKE REVIEW FORM
# ============================================================

st.divider()
st.subheader("💼 SME Employee Hike Review")

with st.form("sme_hike_review"):

    review_employee = st.selectbox(
        "Employee for Hike Review",
        df["Employee Name"].tolist(),
        key="review_employee"
    )

    hike_decision = st.selectbox(
        "Hike Recommendation",
        [
            "Pending Review",
            "Recommend Hike",
            "Consider After Improvement",
            "No Hike Recommended"
        ]
    )

    hike_percentage = st.number_input(
        "Proposed Hike Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

    manager_comments = st.text_area("Manager Comments")

    submit_review = st.form_submit_button("Submit Review")

if submit_review:
    st.session_state["sme_hike_review"] = {
        "Employee Name": review_employee,
        "Hike Recommendation": hike_decision,
        "Proposed Hike Percentage": hike_percentage,
        "Manager Comments": manager_comments
    }

if "sme_hike_review" in st.session_state:
    review = st.session_state["sme_hike_review"]

    st.success("Hike review prepared successfully.")

    st.write("**Employee:**", review["Employee Name"])
    st.write("**Recommendation:**", review["Hike Recommendation"])
    st.write(
        "**Proposed Hike:**",
        f"{review['Proposed Hike Percentage']:.1f}%"
    )
    st.write(
        "**Manager Comments:**",
        review["Manager Comments"] or "None"
    )

    st.download_button(
        "⬇️ Download Hike Review",
        data=pd.DataFrame([review]).to_csv(index=False).encode("utf-8"),
        file_name="SME_hike_review.csv",
        mime="text/csv"
    )

# ============================================================
# 17. DOWNLOAD EMPLOYEE REPORT
# ============================================================

st.divider()
st.subheader("⬇️ Download SME Employee Report")

report_columns = [
    "Employee Name",
    "Leaves",
    "Total Working Days",
    "Given Target",
    "Completed Target",
    "Still Pending",
    PRODUCTIVITY,
    PRODUCTIVITY_50,
    "Pending Percentage"
]

st.download_button(
    "Download SME Report as CSV",
    data=df[report_columns].to_csv(index=False).encode("utf-8"),
    file_name="SME_employee_productivity_report.csv",
    mime="text/csv"
)

# Excel report
excel_buffer = io.BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    df[report_columns].to_excel(
        writer,
        sheet_name="Employee Report",
        index=False
    )

    ranking_df.reset_index().to_excel(
        writer,
        sheet_name="Productivity Ranking",
        index=False
    )

st.download_button(
    "Download SME Report as Excel",
    data=excel_buffer.getvalue(),
    file_name="SME_employee_productivity_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# ============================================================
# 18. FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="subtitle">SME Employee Productivity & Hike Dashboard</div>',
    unsafe_allow_html=True
)
