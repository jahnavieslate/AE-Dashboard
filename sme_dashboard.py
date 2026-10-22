
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import re
import io
from datetime import time, timedelta

# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SME Employee Hike Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# 2. DASHBOARD CSS - TEXT COLOR FIX
# ============================================================

st.markdown("""
<style>
.stApp {
    background-color: #0e1117 !important;
    color: #ffffff !important;
}

.stApp p,
.stApp label,
.stApp span,
.stApp li,
.stApp strong,
.stMarkdown,
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"] {
    color: #ffffff !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 700 !important;
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

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
}

[data-testid="stMetricLabel"] * {
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] * {
    font-size: 25px !important;
    font-weight: 800 !important;
}

/* Data tables */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] *,
[data-testid="stTable"],
[data-testid="stTable"] * {
    color: #ffffff !important;
}

/* Text inputs */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea {
    background-color: #1b2430 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #607d8b !important;
    border-radius: 6px !important;
}

.stApp input::placeholder,
.stApp textarea::placeholder {
    color: #cfd8dc !important;
    -webkit-text-fill-color: #cfd8dc !important;
    opacity: 1 !important;
}

/* ============================================================
   DROPDOWN COLOR FIX
   Selected value and popup options must be readable.
   ============================================================ */

[data-baseweb="select"] > div {
    background-color: #1b2430 !important;
    border-color: #607d8b !important;
}

/* Selected employee name */
[data-baseweb="select"] *,
[data-baseweb="select"] input {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Dropdown popup */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="popover"] ul,
[data-baseweb="popover"] [role="listbox"] {
    background-color: #1b2430 !important;
}

/* Employee options */
[data-baseweb="popover"] [role="option"] {
    background-color: #1b2430 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Highlighted option */
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [role="option"][aria-selected="true"] {
    background-color: #26374a !important;
    color: #64b5f6 !important;
    -webkit-text-fill-color: #64b5f6 !important;
}

/* File uploader */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] * {
    color: #ffffff !important;
}

/* Make the upload area and upload icon clearly visible */
[data-testid="stFileUploader"] {
    background: #162536 !important;
    border: 2px dashed #64b5f6 !important;
    border-radius: 14px !important;
    padding: 16px !important;
}
[data-testid="stFileUploader"] section,
[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {
    background: #162536 !important;
    border: 1px dashed #90caf9 !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] svg {
    color: #90caf9 !important;
    fill: #90caf9 !important;
    stroke: #90caf9 !important;
    opacity: 1 !important;
}
[data-testid="stFileUploader"] button {
    background: #1565c0 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #90caf9 !important;
    font-weight: 800 !important;
}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] label {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    opacity: 1 !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button,
.stFormSubmitButton button {
    background-color: #1565c0 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 1px solid #64b5f6 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.stButton button:hover,
.stDownloadButton button:hover,
.stFormSubmitButton button:hover {
    background-color: #1976d2 !important;
    color: #ffffff !important;
    border-color: #90caf9 !important;
}

/* Captions, alerts and checkboxes */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] *,
[data-testid="stAlert"],
[data-testid="stAlert"] *,
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

/* Forms */
[data-testid="stForm"] {
    background-color: #141b24 !important;
    border: 1px solid #34495e !important;
    border-radius: 10px !important;
    padding: 16px !important;
}

.stApp input:disabled {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Chart labels */
[data-testid="stVegaLiteChart"] svg text,
[data-testid="stVegaLiteChart"] svg tspan,
.vega-embed svg text,
.vega-embed svg tspan {
    fill: #ffffff !important;
    color: #ffffff !important;
}

/* Individual employee panel */
.employee-details-panel {
    background-color: #141b24 !important;
    border: 1px solid #455a64 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    margin: 10px 0 16px 0 !important;
}

.employee-details-panel h3,
.employee-details-panel p,
.employee-details-panel span {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# CHART HELPER - HIGH CONTRAST LABELS AND VISIBLE X/Y AXES
# ============================================================

def show_labeled_bar_chart(data, category_col, value_col, color, x_title, y_title, height=360, numeric_format=",.0f"):
    """Render a readable horizontal bar chart with explicitly titled axes."""
    chart_data = data[[category_col, value_col]].copy()
    chart_data[category_col] = chart_data[category_col].astype(str)
    chart_data[value_col] = pd.to_numeric(chart_data[value_col], errors="coerce").fillna(0)

    chart = (
        alt.Chart(chart_data)
        .mark_bar(color=color, cornerRadiusEnd=4)
        .encode(
            x=alt.X(
                f"{value_col}:Q",
                title=x_title,
                axis=alt.Axis(
                    labelColor="#ffffff", titleColor="#ffffff",
                    gridColor="#455a64", domainColor="#90a4ae",
                    tickColor="#90a4ae", labelFontSize=12, titleFontSize=14,
                    format=numeric_format
                )
            ),
            y=alt.Y(
                f"{category_col}:N",
                title=y_title,
                sort="-x",
                axis=alt.Axis(
                    labelColor="#ffffff", titleColor="#ffffff",
                    domainColor="#90a4ae", tickColor="#90a4ae",
                    labelFontSize=12, titleFontSize=14, labelLimit=220
                )
            ),
            tooltip=[
                alt.Tooltip(f"{category_col}:N", title=y_title),
                alt.Tooltip(f"{value_col}:Q", title=x_title, format=".2f")
            ]
        )
        .properties(height=height, background="#0e1117", padding={"left": 8, "right": 12, "top": 8, "bottom": 8})
        .configure_view(stroke="#455a64")
        .configure_axis(grid=True)
    )
    st.altair_chart(chart, use_container_width=True, theme=None)


# ============================================================
# 3. PROVIDED SME EMPLOYEE DATA
# ============================================================

sme_data = {
    "Employee Name": [
        "Jahnavi Valiveti",
        "Rakesh Kumar",
        "Ravali",
        "Naresh",
        "Pallavi N",
        "Lahari",
        "Keerthika",
        "Sarath Kalyan",
        "Sujeeth Nakka",
        "Rishita Kumari",
        "Vaishnavi",
        "Jahnavi D"
    ],
    "Leaves": [
        12.5, 42, 22.5, 17, 14, 17,
        27, 28, 7.5, 0, 38.5, 15
    ],
    "Total Working Days": [
        283.5, 254, 273.5, 279, 282, 279,
        269, 268, 138.5, 5, 257.5, 281
    ],
    "Given Target": [
        243, 218, 235, 240, 242, 240,
        231, 230, 120, 6, 296, 281
    ],
    "Completed Target": [
        243, 212, 126, 215, 248, 138,
        135, 168, 105, 4, 187, 244
    ],
    "Still Pending": [
        0, 6, 109, 25, -6, 102,
        96, 62, 15, 2, 109, 37
    ],
    "Total Video Count": [
        103, 55, 55, 109, 73, 75,
        65, 30, 10, 0, 34, 91
    ],
    "Total Video Duration": [
        "17:04:23",
        "16:49:26",
        "15:10:16",
        "31:52:29",
        "17:53:57",
        "17:09:12",
        "21:37:31",
        "05:25:32",
        "03:21:57",
        "00:00:00",
        "11:04:11",
        "26:28:16"
    ]
}

sample_df = pd.DataFrame(sme_data)

PRODUCTIVITY = "Productivity (As per 100 %)"
PRODUCTIVITY_50 = "Productivity (As per 50 %)"
DURATION_SECONDS = "_Video Duration Seconds"


# ============================================================
# 4. DURATION HELPER FUNCTIONS
# ============================================================

def duration_to_seconds(value):
    """Convert HH:MM:SS or Excel duration values into seconds."""

    if value is None or pd.isna(value):
        return 0

    if isinstance(value, time):
        return (
            value.hour * 3600
            + value.minute * 60
            + value.second
        )

    if isinstance(value, timedelta):
        return max(0, int(value.total_seconds()))

    if isinstance(value, (int, float, np.integer, np.floating)):
        number = float(value)

        # Excel stores time-only values as fractions of a day.
        if 0 <= number < 1:
            return int(round(number * 86400))

        return max(0, int(round(number)))

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "nat"}:
        return 0

    match = re.fullmatch(
        r"(\d+):([0-5]?\d):([0-5]?\d)",
        text
    )

    if match:
        hours, minutes, seconds = map(int, match.groups())
        return hours * 3600 + minutes * 60 + seconds

    try:
        result = pd.to_timedelta(text, errors="raise")
        return max(0, int(result.total_seconds()))
    except (ValueError, TypeError, OverflowError):
        return 0


def format_duration(seconds):
    """Format seconds as HH:MM:SS without wrapping after 24 hours."""

    seconds = max(0, int(round(float(seconds))))
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"


# ============================================================
# 5. UPLOAD SCREEN
# ============================================================

st.markdown(
    '<div class="main-title">'
    '📊 SME Employee Productivity & Hike Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your employee performance sheet'
    '</div>',
    unsafe_allow_html=True
)

with st.container(border=True):
    st.subheader("📁 Upload SME Employee Sheet")
    st.markdown(
        "<div style='background:#162536;border:1px solid #64b5f6;"
        "border-radius:10px;padding:12px;color:#ffffff;font-weight:600;'>"
        "⬆️ Select <b>Browse files</b> or drag and drop your Excel/CSV file below."
        "</div>",
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "📂 Choose an Excel or CSV file",
        type=["xlsx", "xls", "csv"],
        label_visibility="visible",
        help="Click Browse files to choose .xlsx, .xls or .csv from your computer."
    )

    st.caption(
        "Required columns: Employee Name, Leaves, Total Working Days, "
        "Given Target and Completed Target. "
        "Video Count and Video Duration columns are also supported."
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
# 6. LOAD DATA
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
# 7. NORMALIZE COLUMN NAMES
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
    "totalvideocount": "Total Video Count",
    "videocount": "Total Video Count",
    "totalvideos": "Total Video Count",
    "totalvideoduration": "Total Video Duration",
    "videoduration": "Total Video Duration",
    "totalduration": "Total Video Duration",
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

if df.empty:
    st.error("No employee records were found in the uploaded file.")
    st.stop()

# Optional columns
if "Still Pending" not in df.columns:
    df["Still Pending"] = np.nan

if "Total Video Count" not in df.columns:
    df["Total Video Count"] = 0

if "Total Video Duration" not in df.columns:
    df["Total Video Duration"] = "00:00:00"


# ============================================================
# 8. CONVERT NUMERIC DATA
# ============================================================

numeric_columns = [
    "Leaves",
    "Total Working Days",
    "Given Target",
    "Completed Target",
    "Still Pending",
    "Total Video Count"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

missing_pending = df["Still Pending"].isna()

df.loc[missing_pending, "Still Pending"] = (
    df.loc[missing_pending, "Given Target"]
    - df.loc[missing_pending, "Completed Target"]
)

df[numeric_columns] = df[numeric_columns].fillna(0)
df["Total Video Count"] = df["Total Video Count"].clip(lower=0)

df[DURATION_SECONDS] = df["Total Video Duration"].apply(
    duration_to_seconds
)

df["Total Video Duration"] = df[DURATION_SECONDS].apply(
    format_duration
)


# ============================================================
# 9. AUTOMATIC PRODUCTIVITY CALCULATIONS
# ============================================================

df[PRODUCTIVITY] = np.where(
    
    df["Given Target"] > 0,
    (df["Completed Target"] / df["Given Target"]) * 100,
    0.0
)

df[PRODUCTIVITY_50] = df[PRODUCTIVITY] / 2

df["Pending Percentage"] = np.where(
    df["Given Target"] > 0,
    (
        df["Still Pending"].clip(lower=0)
        / df["Given Target"]
    ) * 100,
    0.0
)


# ============================================================
# 10. DASHBOARD SUMMARY
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

total_video_count = int(df["Total Video Count"].sum())
total_video_seconds = int(df[DURATION_SECONDS].sum())

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

st.divider()
st.subheader("🎬 Team Video Summary")

v1, v2, v3 = st.columns(3)

v1.metric("Total Video Count", f"{total_video_count:,}")
v2.metric("Total Video Duration", format_duration(total_video_seconds))
v3.metric(
    "Average Videos per Employee",
    f"{df['Total Video Count'].mean():.1f}"
)


# ============================================================
# 11. VIDEO PERFORMANCE INSIGHTS
# ============================================================

st.divider()
st.header("📊 Video Performance Insights")
st.caption(
    "Team-wide video production and duration insights calculated from the "
    "currently loaded employee sheet."
)

# Team-wide video metrics
insights_total_videos = int(df["Total Video Count"].sum())
insights_total_seconds = int(df[DURATION_SECONDS].sum())
insights_average_videos = float(df["Total Video Count"].mean()) if not df.empty else 0.0
insights_average_duration_seconds = (
    insights_total_seconds / insights_total_videos
    if insights_total_videos > 0 else 0
)

# Top contributors; the uploaded data is validated as non-empty above.
top_video_employee = df.loc[df["Total Video Count"].idxmax()]
top_duration_employee = df.loc[df[DURATION_SECONDS].idxmax()]

iv1, iv2, iv3, iv4 = st.columns(4)
iv1.metric("🎬 Total Videos Produced", f"{insights_total_videos:,}")
iv2.metric("⏱️ Total Video Duration", format_duration(insights_total_seconds))
iv3.metric("📹 Average Videos per Employee", f"{insights_average_videos:.1f}")
iv4.metric(
    "⏳ Average Duration per Video",
    format_duration(insights_average_duration_seconds)
)

st.subheader("🏆 Video Production Highlights")
highlight1, highlight2 = st.columns(2)
with highlight1:
    if insights_total_videos > 0:
        st.success(
            f"**Highest video count:** {top_video_employee['Employee Name']} — "
            f"{int(top_video_employee['Total Video Count']):,} videos"
        )
    else:
        st.info("No videos have been recorded in the loaded data.")
with highlight2:
    if insights_total_seconds > 0:
        st.info(
            f"**Longest total video duration:** {top_duration_employee['Employee Name']} — "
            f"{top_duration_employee['Total Video Duration']}"
        )
    else:
        st.info("No video duration has been recorded in the loaded data.")

# Employee-wise comparison. Duration is shown in decimal hours for chart readability.
video_insights_df = df[
    ["Employee Name", "Total Video Count", DURATION_SECONDS, "Total Video Duration"]
].copy()
video_insights_df["Duration (Hours)"] = video_insights_df[DURATION_SECONDS] / 3600
video_insights_df = video_insights_df.sort_values(
    "Total Video Count", ascending=False
)

video_chart1, video_chart2 = st.columns(2)
with video_chart1:
    st.subheader("🎬 Video Count by Employee")
    show_labeled_bar_chart(
        video_insights_df, "Employee Name", "Total Video Count", "#64b5f6",
        x_title="Video Count (X-axis)", y_title="Employee Name (Y-axis)", height=390
    )
with video_chart2:
    st.subheader("⏱️ Total Video Duration by Employee")
    show_labeled_bar_chart(
        video_insights_df, "Employee Name", "Duration (Hours)", "#26a69a",
        x_title="Total Video Duration (Hours) (X-axis)",
        y_title="Employee Name (Y-axis)", height=390, numeric_format=",.1f"
    )

st.caption(
    "The duration chart uses decimal hours for easier comparison. "
    "The team total and employee summary retain HH:MM:SS format."
)

st.subheader("📋 Employee Video Summary")
video_summary_df = video_insights_df[
    ["Employee Name", "Total Video Count", "Total Video Duration", "Duration (Hours)"]
].copy()
video_summary_df = video_summary_df.rename(columns={
    "Total Video Count": "Total Videos",
    "Total Video Duration": "Total Video Duration (HH:MM:SS)"
})
st.dataframe(
    video_summary_df.style.format({
        "Total Videos": "{:,.0f}",
        "Duration (Hours)": "{:.2f}"
    }),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 12. EMPLOYEE DETAILS TABLE
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
    "Total Video Count",
    "Total Video Duration",
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
        "Total Video Count": "{:,.0f}",
        PRODUCTIVITY: "{:.2f}%",
        PRODUCTIVITY_50: "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 13. INDIVIDUAL EMPLOYEE PERFORMANCE
# ============================================================

st.divider()
st.subheader("👤 Individual Employee Performance")

selected_employee = st.selectbox(
    "Select an Employee",
    df["Employee Name"].tolist(),
    key="individual_employee_select"
)

employee = df[df["Employee Name"] == selected_employee].iloc[0]

st.markdown(
    f'<div class="employee-details-panel">'
    f'<h3>👤 {selected_employee}</h3>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown("#### 📈 Productivity & Attendance")

a, b, c, d = st.columns(4)

a.metric("Productivity (100%)", f"{employee[PRODUCTIVITY]:.2f}%")
b.metric("Productivity (50%)", f"{employee[PRODUCTIVITY_50]:.2f}%")
c.metric("Leaves", f"{employee['Leaves']:.1f}")
d.metric("Working Days", f"{employee['Total Working Days']:.1f}")

st.markdown("#### 🎯 Target Details")

x, y, z = st.columns(3)

x.metric("Given Target", f"{employee['Given Target']:,.0f}")
y.metric("Completed Target", f"{employee['Completed Target']:,.0f}")
z.metric("Still Pending", f"{employee['Still Pending']:,.0f}")

st.markdown("#### 🎬 Video Performance")

video1, video2 = st.columns(2)

video1.metric("Total Video Count", f"{int(employee['Total Video Count']):,}")
video2.metric("Total Video Duration", employee["Total Video Duration"])


# ============================================================
# 14. INDIVIDUAL TARGET CHART
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

show_labeled_bar_chart(
    target_chart.reset_index(), "Target Type", "Target", "#64b5f6",
    x_title="Target Value (X-axis)", y_title="Target Type (Y-axis)", height=240
)


# ============================================================
# 15. TEAM PRODUCTIVITY CHART
# ============================================================

st.divider()
st.subheader("📈 SME Team Productivity")

productivity_chart = filtered_df[
    ["Employee Name", PRODUCTIVITY]
].set_index("Employee Name")

show_labeled_bar_chart(
    productivity_chart.reset_index(), "Employee Name", PRODUCTIVITY, "#26a69a",
    x_title="Productivity (%) (X-axis)", y_title="Employee Name (Y-axis)", height=390
)

st.caption(
    "100% means the target was achieved. Values above 100% mean "
    "the employee exceeded the target."
)


# ============================================================
# 16. PENDING TARGET CHART
# ============================================================

st.divider()
st.subheader("⏳ Employee Pending Targets")

pending_chart = filtered_df[
    ["Employee Name", "Still Pending"]
].set_index("Employee Name")

show_labeled_bar_chart(
    pending_chart.reset_index(), "Employee Name", "Still Pending", "#ffb74d",
    x_title="Pending Target Count (X-axis)", y_title="Employee Name (Y-axis)", height=390
)

st.caption(
    "Negative pending values indicate that the employee exceeded "
    "the given target."
)


# ============================================================
# 17. VIDEO COUNT CHART
# ============================================================

st.divider()
st.subheader("🎬 Employee Video Count")

video_count_chart = filtered_df[
    ["Employee Name", "Total Video Count"]
].set_index("Employee Name")

show_labeled_bar_chart(
    video_count_chart.reset_index(), "Employee Name", "Total Video Count", "#64b5f6",
    x_title="Video Count (X-axis)", y_title="Employee Name (Y-axis)", height=390
)


# ============================================================
# 18. PRODUCTIVITY RANKING
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
# 19. HIKE REVIEW FORM
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
# 20. DOWNLOAD EMPLOYEE REPORTS
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
    "Total Video Count",
    "Total Video Duration",
    PRODUCTIVITY,
    PRODUCTIVITY_50,
    "Pending Percentage"
]

report_df = df[report_columns].copy()

st.download_button(
    "Download SME Report as CSV",
    data=report_df.to_csv(index=False).encode("utf-8"),
    file_name="SME_employee_productivity_report.csv",
    mime="text/csv"
)

excel_buffer = io.BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    report_df.to_excel(
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
# 21. FOOTER
# ============================================================

st.divider()

st.markdown(
    '<div class="subtitle">'
    'SME Employee Productivity & Hike Dashboard'
    '</div>',
    unsafe_allow_html=True
)
