
# ============================================================
# AFTER EFFECTS EMPLOYEE PRODUCTIVITY & HIKE DASHBOARD
# Upload Excel/CSV -> Calculate Metrics -> Display Analytics
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import re
import io
from datetime import time, timedelta, datetime

# ============================================================
# STEP 1: PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Employee Productivity & Hike Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# STEP 2: CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>
/* Dashboard background and default text */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"], [data-testid="stSidebar"] {
    background-color: #0e1117 !important;
    color: #ffffff !important;
}
[data-testid="stMainBlockContainer"] {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
}
p, li, small, strong, em, label,
.stMarkdown, .stMarkdown p, [data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *, [data-testid="stCaptionContainer"],
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] * {
    color: #ffffff !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #90caf9 !important;
}
.main-title {
    font-size: 32px;
    font-weight: 800;
    color: #64b5f6 !important;
    text-align: center;
    padding: 12px;
}
.subtitle {
    text-align: center;
    color: #e0e7ef !important;
    font-size: 16px;
}

/* White metric cards: dark, readable labels and values */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    border-radius: 12px !important;
    padding: 18px !important;
}
[data-testid="stMetric"] label,
[data-testid="stMetric"] label *,
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"], [data-testid="stMetricValue"] *,
[data-testid="stMetricDelta"], [data-testid="stMetricDelta"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}

/* Employee and hike dropdown: black selected text on white */
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #60a5fa !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stSelectbox"] [data-baseweb="select"] input,
[data-testid="stSelectbox"] [data-baseweb="select"] span {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}
[data-baseweb="popover"], [data-baseweb="popover"] > div,
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] [role="option"] * {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [role="option"][aria-selected="true"] {
    background: #dbeafe !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Other inputs */
.stTextInput input, .stNumberInput input, .stDateInput input,
.stTextArea textarea, [data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 1px solid #9ca3af !important;
    caret-color: #111827 !important;
}
input::placeholder, textarea::placeholder {
    color: #6b7280 !important;
    -webkit-text-fill-color: #6b7280 !important;
    opacity: 1 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #151d29 !important;
    border: 1px solid #456078 !important;
    border-radius: 12px !important;
    padding: 10px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: #1b2430 !important;
    border: 2px dashed #64b5f6 !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] *, [data-testid="stFileUploaderDropzone"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
[data-testid="stFileUploader"] button,
.stButton button, .stDownloadButton button, .stFormSubmitButton button {
    background: #1565c0 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #64b5f6 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

/* Tables */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background: #ffffff !important;
}
[data-testid="stDataFrame"] *, [data-testid="stTable"] * {
    color: #111827 !important;
}

/* Charts: dark labels on white chart canvas */
[data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"],
.vega-embed {
    background: #ffffff !important;
    border-radius: 8px !important;
}
.vega-embed svg text,
.vega-embed svg .role-axis text,
.vega-embed svg .role-legend text,
.vega-embed svg .role-title text {
    fill: #111827 !important;
    color: #111827 !important;
}
.vega-embed svg .role-axis-grid line {
    stroke: #e5e7eb !important;
}
.vega-embed svg .role-axis-domain,
.vega-embed svg .role-axis-tick {
    stroke: #6b7280 !important;
}
/* Hover tooltip: white background with black text */
.vega-tooltip, .vg-tooltip, [role="tooltip"] {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.18) !important;
}
.vega-tooltip *, .vg-tooltip *, [role="tooltip"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Alerts and expanders */
[data-testid="stAlert"] {
    background: #1b2430 !important;
    border: 1px solid #456078 !important;
}
[data-testid="stAlert"] * {
    color: #ffffff !important;
}
hr { border-color: #455a64 !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# STEP 3: DASHBOARD TITLE AND FILE UPLOAD
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📊 Employee Productivity & Hike Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your employee performance sheet to view analytics'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

with st.container(border=True):
    st.subheader("📁 Upload Employee Sheet")

    uploaded_file = st.file_uploader(
        "Choose an Excel or CSV file",
        type=["xlsx", "xls", "csv"],
        help="Upload your employee performance spreadsheet."
    )

    st.caption(
        "Required columns: Employee Name, Leaves, Total Working Days, "
        "Given Target, Completed Target and Still Pending. "
        "Total Video Count is also supported."
    )

if uploaded_file is None:
    st.info(
        "Please upload your employee sheet. "
        "Your dashboard will appear after uploading."
    )
    st.stop()


# ============================================================
# STEP 4: READ AND CLEAN UPLOADED FILE
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

    "totalvideocount": "Total Video Count",
    "videocount": "Total Video Count",
    "totalvideos": "Total Video Count",
    "videoscount": "Total Video Count",
    "numberofvideos": "Total Video Count",

    "giventarget": "Given Target",
    "targetgiven": "Given Target",

    "completedtarget": "Completed Target",
    "targetcompleted": "Completed Target",

    "stillpending": "Still Pending",
    "pending": "Still Pending",

    "productivity": "Productivity (As per 100 %)",
    "productivitypercentage": "Productivity (As per 100 %)",
    "productivityasper100": "Productivity (As per 100 %)",
    "productivityasper100percent": "Productivity (As per 100 %)",

    "pendingpercentage": "Pending Percentage",

    "productivityat50": "Productivity (As per 50 %)",
    "productivityasper50": "Productivity (As per 50 %)",
    "productivityasper50percent": "Productivity (As per 50 %)"
}

try:
    if uploaded_file.name.lower().endswith(".csv"):
        try:
            raw_df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            raw_df = pd.read_csv(
                uploaded_file,
                encoding="latin-1"
            )
    else:
        raw_df = pd.read_excel(uploaded_file)

    if raw_df.empty:
        st.error("The uploaded spreadsheet is empty.")
        st.stop()

    raw_df.columns = raw_df.columns.astype(str).str.strip()

    rename_columns = {}

    for column in raw_df.columns:
        key = normalize_column(column)

        if key in aliases:
            rename_columns[column] = aliases[key]

    df = raw_df.rename(columns=rename_columns)
    df = df.dropna(how="all").copy()

    if df.columns.duplicated().any():
        st.error(
            "Duplicate column names were found after normalizing "
            "the spreadsheet headings. Please check your file."
        )
        st.stop()

    required_columns = [
        "Employee Name",
        "Leaves",
        "Total Working Days",
        "Given Target",
        "Completed Target",
        "Still Pending"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        st.error(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

        st.write("Columns found in your file:")
        st.write(list(df.columns))
        st.stop()

    df = df.dropna(subset=["Employee Name"]).copy()

    df["Employee Name"] = (
        df["Employee Name"].astype(str).str.strip()
    )

    df = df[df["Employee Name"] != ""].copy()

    if df.empty:
        st.error("No employee records were found.")
        st.stop()

    # NEW COLUMN: TOTAL VIDEO COUNT
    # Supports spreadsheets with or without this column.
    if "Total Video Count" not in df.columns:
        df["Total Video Count"] = 0

    df["Total Video Count"] = pd.to_numeric(
        df["Total Video Count"],
        errors="coerce"
    )

    if df["Total Video Count"].isna().any():
        st.error(
            "Total Video Count must contain valid numeric values."
        )
        st.stop()

    if (df["Total Video Count"] < 0).any():
        st.error("Total Video Count cannot be negative.")
        st.stop()

    if (df["Total Video Count"] % 1 != 0).any():
        st.error("Total Video Count must contain whole numbers.")
        st.stop()

    df["Total Video Count"] = (
        df["Total Video Count"].astype(int)
    )

except Exception as error:
    st.error(f"Unable to read the uploaded file: {error}")
    st.stop()


# ============================================================
# STEP 5: CONVERT TIME DURATIONS TO SECONDS
# ============================================================

def time_to_seconds(value):
    """
    Convert spreadsheet durations to seconds.

    Supports:
    - HH:MM:SS strings
    - MM:SS strings
    - Excel/Pandas Timedelta values
    - Python time and datetime values
    - Excel fractions of a day
    - Numeric strings interpreted as hours
    """

    if value is None or value is pd.NaT:
        return np.nan

    try:
        if pd.isna(value):
            return np.nan
    except (TypeError, ValueError):
        pass

    if isinstance(value, (pd.Timedelta, timedelta)):
        return value.total_seconds()

    if isinstance(value, (time, datetime, pd.Timestamp)):
        return (
            value.hour * 3600
            + value.minute * 60
            + value.second
            + value.microsecond / 1_000_000
        )

    if isinstance(value, (int, float, np.integer, np.floating)):
        # Excel time values are fractions of a day.
        return float(value) * 86400

    value = str(value).strip()

    if value.lower() in {"", "none", "nan", "nat", "null"}:
        return np.nan

    parts = value.split(":")

    try:
        if len(parts) == 3:
            hours, minutes, seconds = map(float, parts)

            if minutes >= 60 or seconds >= 60:
                return np.nan

            return hours * 3600 + minutes * 60 + seconds

        if len(parts) == 2:
            minutes, seconds = map(float, parts)

            if seconds >= 60:
                return np.nan

            return minutes * 60 + seconds

        # A standalone numeric string is treated as hours.
        return float(value) * 3600

    except (ValueError, TypeError):
        return np.nan


def format_duration(value):
    """Format seconds as HH:MM:SS without a 24-hour limit."""

    if pd.isna(value):
        return "—"

    total_seconds = int(round(float(value)))
    sign = "-" if total_seconds < 0 else ""
    total_seconds = abs(total_seconds)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return (
        f"{sign}{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )


duration_columns = [
    "Given Target",
    "Completed Target",
    "Still Pending"
]

for column in duration_columns:
    df[column + " (Seconds)"] = (
        df[column].apply(time_to_seconds)
    )

    df[column + " (Hours)"] = (
        df[column + " (Seconds)"] / 3600
    )

    if df[column + " (Seconds)"].isna().any():
        st.error(
            f"Invalid or missing duration found in '{column}'. "
            "Please check the spreadsheet values."
        )
        st.stop()

# Validate durations.
for column in duration_columns:
    if (df[column + " (Seconds)"] < 0).any():
        st.error(
            f"Negative durations are not allowed in '{column}'."
        )
        st.stop()

# Display durations in HH:MM:SS format.
for column in duration_columns:
    df[column] = df[column + " (Seconds)"].apply(
        format_duration
    )


# ============================================================
# STEP 6: CALCULATE PRODUCTIVITY METRICS
# ============================================================

for column in ["Leaves", "Total Working Days"]:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

if df[["Leaves", "Total Working Days"]].isna().any().any():
    st.error(
        "Leaves and Total Working Days must contain valid numbers."
    )
    st.stop()

if (df[["Leaves", "Total Working Days"]] < 0).any().any():
    st.error("Leaves and Total Working Days cannot be negative.")
    st.stop()

given_seconds = df["Given Target (Seconds)"]
completed_seconds = df["Completed Target (Seconds)"]
pending_seconds = df["Still Pending (Seconds)"]

# Productivity = Completed Target / Given Target * 100
df["Productivity (As per 100 %)"] = np.where(
    given_seconds > 0,
    completed_seconds / given_seconds * 100,
    0.0
)

# Pending Percentage = Still Pending / Given Target * 100
df["Pending Percentage"] = np.where(
    given_seconds > 0,
    pending_seconds / given_seconds * 100,
    0.0
)

# Productivity at 50% = Productivity at 100% / 2
df["Productivity (As per 50 %)"] = (
    df["Productivity (As per 100 %)"] / 2
)

productivity_col = "Productivity (As per 100 %)"
pending_pct_col = "Pending Percentage"
half_productivity_col = "Productivity (As per 50 %)"


# ============================================================
# STEP 7: DASHBOARD HEADER
# ============================================================

st.divider()

st.markdown(
    '<div class="main-title">'
    'Employee Performance Overview'
    '</div>',
    unsafe_allow_html=True
)

st.caption(f"Uploaded file: {uploaded_file.name}")

st.divider()


# ============================================================
# STEP 8: TEAM SUMMARY ANALYTICS
# ============================================================

st.header("📊 Team Summary Analytics")

total_employees = len(df)
average_productivity = df[productivity_col].mean()
average_pending_percentage = df[pending_pct_col].mean()
average_half_productivity = df[half_productivity_col].mean()

total_leaves = df["Leaves"].sum()
average_leaves = df["Leaves"].mean()

# NEW: Total video count across the team.
total_video_count = int(df["Total Video Count"].sum())

employees_above_target = (
    df[productivity_col] >= 100
).sum()

employees_below_target = (
    df[productivity_col] < 100
).sum()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Employees", total_employees)

with col2:
    st.metric(
        "Average Productivity",
        f"{average_productivity:.2f}%"
    )

with col3:
    st.metric(
        "Average Pending %",
        f"{average_pending_percentage:.2f}%"
    )

with col4:
    st.metric(
        "Average Productivity at 50%",
        f"{average_half_productivity:.2f}%"
    )

with col5:
    st.metric("Total Leaves", f"{total_leaves:.1f}")

col6, col7, col8, col9 = st.columns(4)

with col6:
    st.metric("Average Leaves", f"{average_leaves:.1f}")

with col7:
    # NEW METRIC
    st.metric("Total Video Count", f"{total_video_count:,}")

with col8:
    st.metric(
        "At/Above 100% Target",
        int(employees_above_target)
    )

with col9:
    st.metric(
        "Below 100% Target",
        int(employees_below_target)
    )

st.caption(
    "Productivity at 100% is the completed-to-target ratio. "
    "Productivity at 50% is half of the 100% productivity value."
)


# ============================================================
# STEP 9: EMPLOYEE DETAILS TABLE
# ============================================================

st.divider()
st.header("🔎 Employee Details")

search_text = st.text_input(
    "Search employee",
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

# NEW: Total Video Count included in the employee table.
display_columns = [
    "Employee Name",
    "Leaves",
    "Total Working Days",
    "Total Video Count",
    "Given Target",
    "Completed Target",
    "Still Pending",
    productivity_col,
    pending_pct_col,
    half_productivity_col
]

st.caption(
    f"Showing {len(filtered_df)} of {total_employees} employees"
)

st.dataframe(
    filtered_df[display_columns].style.format({
        "Leaves": "{:.1f}",
        "Total Working Days": "{:.1f}",
        "Total Video Count": "{:,.0f}",
        productivity_col: "{:.2f}%",
        pending_pct_col: "{:.2f}%",
        half_productivity_col: "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# STEP 10: INDIVIDUAL EMPLOYEE PERFORMANCE
# ============================================================

st.divider()
st.header("👤 Individual Employee Performance")

selected_employee = st.selectbox(
    "Select an employee",
    options=df["Employee Name"].tolist(),
    key="individual_employee_select"
)

employee = df[
    df["Employee Name"] == selected_employee
].iloc[0]

st.subheader(f"Employee Report: {selected_employee}")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Productivity (100%)",
        f"{employee[productivity_col]:.2f}%"
    )

with c2:
    st.metric(
        "Pending Percentage",
        f"{employee[pending_pct_col]:.2f}%"
    )

with c3:
    st.metric(
        "Productivity (50%)",
        f"{employee[half_productivity_col]:.2f}%"
    )

with c4:
    st.metric("Leaves", f"{employee['Leaves']:.1f}")

# NEW: Individual video count and working days.
video_col1, video_col2 = st.columns(2)

with video_col1:
    st.metric(
        "Total Video Count",
        f"{int(employee['Total Video Count']):,}"
    )

with video_col2:
    st.metric(
        "Total Working Days",
        f"{employee['Total Working Days']:.1f}"
    )

st.subheader("⏱️ Target Details")

target_col1, target_col2, target_col3 = st.columns(3)

with target_col1:
    st.metric("Given Target", employee["Given Target"])

with target_col2:
    st.metric("Completed Target", employee["Completed Target"])

with target_col3:
    st.metric("Still Pending", employee["Still Pending"])

st.subheader("📈 Employee Productivity Breakdown")

individual_chart_df = pd.DataFrame({
    "Metric": [
        "Productivity (100%)",
        "Pending Percentage",
        "Productivity (50%)"
    ],
    "Percentage": [
        employee[productivity_col],
        employee[pending_pct_col],
        employee[half_productivity_col]
    ]
})

st.bar_chart(
    individual_chart_df.set_index("Metric"),
    y="Percentage",
    color="#64b5f6"
)


# ============================================================
# STEP 11: GIVEN VS COMPLETED TARGET CHART
# ============================================================

st.divider()
st.header("⏱️ Given Target vs Completed Target")

target_chart_df = pd.DataFrame({
    "Target Type": [
        "Given Target",
        "Completed Target",
        "Still Pending"
    ],
    "Hours": [
        employee["Given Target (Hours)"],
        employee["Completed Target (Hours)"],
        employee["Still Pending (Hours)"]
    ]
})

st.bar_chart(
    target_chart_df.set_index("Target Type"),
    y="Hours",
    color="#64b5f6"
)

st.caption(
    "Durations are converted to hours for charting. "
    "The employee table displays durations in HH:MM:SS format."
)


# ============================================================
# STEP 12: TEAM PRODUCTIVITY COMPARISON
# ============================================================

st.divider()
st.header("📈 Team Productivity Comparison")

productivity_chart_df = filtered_df[
    ["Employee Name", productivity_col]
].set_index("Employee Name")

st.bar_chart(
    productivity_chart_df,
    y=productivity_col,
    color="#26a69a"
)

st.caption(
    "100% means completed work matches the given target. "
    "Above 100% means the employee exceeded the target."
)


# ============================================================
# STEP 13: EMPLOYEE PRODUCTIVITY RANKING
# ============================================================

st.divider()
st.header("🏆 Employee Productivity Ranking")

ranking_df = df[
    [
        "Employee Name",
        productivity_col,
        pending_pct_col,
        half_productivity_col
    ]
].sort_values(
    by=productivity_col,
    ascending=False
).reset_index(drop=True)

ranking_df.index = ranking_df.index + 1
ranking_df.index.name = "Rank"

st.dataframe(
    ranking_df.style.format({
        productivity_col: "{:.2f}%",
        pending_pct_col: "{:.2f}%",
        half_productivity_col: "{:.2f}%"
    }),
    use_container_width=True
)


# ============================================================
# STEP 14: PRODUCTIVITY CATEGORY ANALYTICS
# ============================================================

st.divider()
st.header("📊 Productivity Category Analytics")

category_df = df[
    [
        "Employee Name",
        productivity_col
    ]
].copy()

category_df["Performance Category"] = np.select(
    [
        category_df[productivity_col] >= 100,
        category_df[productivity_col] >= 75,
        category_df[productivity_col] >= 50
    ],
    [
        "At/Above Target (100%+)",
        "Good (75–99.99%)",
        "Needs Improvement (50–74.99%)"
    ],
    default="Below 50%"
)

category_summary = (
    category_df["Performance Category"]
    .value_counts()
    .rename_axis("Performance Category")
    .reset_index(name="Employee Count")
)

st.dataframe(
    category_summary,
    use_container_width=True,
    hide_index=True
)

st.bar_chart(
    category_summary.set_index("Performance Category"),
    y="Employee Count",
    color="#64b5f6"
)


# ============================================================
# STEP 15: EMPLOYEE HIKE REVIEW
# ============================================================

st.divider()
st.header("💼 Employee Hike Review")

with st.form("hike_review_form"):

    review_employee = st.selectbox(
        "Employee for hike review",
        options=df["Employee Name"].tolist(),
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

    manager_comments = st.text_area(
        "Manager Comments",
        placeholder="Enter performance feedback..."
    )

    submit_review = st.form_submit_button("Submit Review")

if submit_review:
    st.session_state["hike_review"] = {
        "Employee Name": review_employee,
        "Hike Recommendation": hike_decision,
        "Proposed Hike Percentage": hike_percentage,
        "Manager Comments": manager_comments
    }

if "hike_review" in st.session_state:
    review = st.session_state["hike_review"]

    st.success("Hike review prepared successfully.")

    st.write("**Employee:**", review["Employee Name"])
    st.write("**Recommendation:**", review["Hike Recommendation"])

    st.write(
        "**Proposed Hike:**",
        f"{review['Proposed Hike Percentage']:.1f}%"
    )

    st.write(
        "**Manager Comments:**",
        review["Manager Comments"] or "No comments entered"
    )

    review_csv = pd.DataFrame([review]).to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ Download Hike Review",
        data=review_csv,
        file_name="employee_hike_review.csv",
        mime="text/csv"
    )


# ============================================================
# STEP 16: DOWNLOAD EMPLOYEE REPORT
# ============================================================

st.divider()
st.header("⬇️ Download Employee Report")

# NEW: Total Video Count included in exported reports.
report_columns = [
    "Employee Name",
    "Leaves",
    "Total Working Days",
    "Total Video Count",
    "Given Target",
    "Completed Target",
    "Still Pending",
    productivity_col,
    pending_pct_col,
    half_productivity_col
]

report_df = df[report_columns].copy()

report_csv = report_df.to_csv(
    index=False
).encode("utf-8-sig")

st.download_button(
    "📥 Download Employee Report as CSV",
    data=report_csv,
    file_name="employee_productivity_report.csv",
    mime="text/csv"
)

# Excel report with multiple sheets.
excel_buffer = io.BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    report_df.to_excel(
        writer,
        sheet_name="Employee Productivity",
        index=False
    )

    ranking_df.reset_index().to_excel(
        writer,
        sheet_name="Productivity Ranking",
        index=False
    )

    category_summary.to_excel(
        writer,
        sheet_name="Performance Categories",
        index=False
    )

st.download_button(
    "📥 Download Complete Excel Report",
    data=excel_buffer.getvalue(),
    file_name="employee_productivity_analytics.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)


# ============================================================
# STEP 17: FOOTER
# ============================================================

st.divider()

st.caption(
    "Employee Productivity & Hike Dashboard | "
    "Productivity (100%) = Completed Target / Given Target × 100 | "
    "Pending Percentage = Still Pending / Given Target × 100 | "
    "Productivity (50%) = Productivity (100%) / 2"
)
