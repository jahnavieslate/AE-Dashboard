import io
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Illustrator Team Analytics",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. CUSTOM CSS
# =========================================================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117 !important;
    color: #ffffff !important;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #151b24 !important;
}

h1, h2, h3, h4, h5, h6,
p, label, li, strong, small,
.stMarkdown, .stCaption,
[data-testid="stWidgetLabel"],
[data-testid="stMarkdownContainer"] {
    color: #ffffff !important;
}

h1 {
    font-size: 2.1rem !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 1.5rem !important;
}

div[data-testid="stMetric"] {
    background-color: #1b2430 !important;
    border: 1px solid #334155 !important;
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
}

[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background-color: #1b2430 !important;
}

.stButton > button,
.stDownloadButton > button {
    background-color: #1976d2 !important;
    color: #ffffff !important;
    border: 1px solid #64b5f6 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.stButton > button *,
.stDownloadButton > button * {
    color: #ffffff !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #1565c0 !important;
}

input, textarea {
    background-color: #1b2430 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

[data-baseweb="select"] * {
    color: #ffffff !important;
}

[data-baseweb="select"] > div {
    background-color: #1b2430 !important;
}

[data-testid="stFileUploader"] * {
    color: #ffffff !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #1b2430 !important;
    border: 1px dashed #64b5f6 !important;
}

[data-testid="stAlert"] * {
    color: #ffffff !important;
}

[data-testid="stCheckbox"] *,
[data-testid="stRadio"] * {
    color: #ffffff !important;
}

hr {
    border-color: #334155 !important;
}

.dashboard-note {
    background-color: #1b2430;
    border-left: 4px solid #64b5f6;
    padding: 16px;
    border-radius: 8px;
    color: #ffffff;
    margin-bottom: 18px;
}

.section-caption {
    color: #ffffff !important;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. REQUIRED COLUMNS
# =========================================================
REQUIRED_COLUMNS = [
    "Employee Name",
    "Leaves",
    "Total Working Days",
    "Given Targets illustrations",
    "Given Targets Same BG",
    "Given Targets Multiple BG",
    "Completed illustrations",
    "Completed Same BG",
    "Completed Multiple BG"
]

NUMERIC_COLUMNS = [
    col for col in REQUIRED_COLUMNS
    if col != "Employee Name"
]

# =========================================================
# 4. COLUMN NAME ALIASES
# =========================================================
ALIASES = {
    "employee name": "Employee Name",
    "employee": "Employee Name",
    "name": "Employee Name",
    "leaves": "Leaves",
    "total working days": "Total Working Days",
    "working days": "Total Working Days",

    "given targets illustrations": "Given Targets illustrations",
    "given target illustrations": "Given Targets illustrations",
    "given illustrations": "Given Targets illustrations",
    "illustrations target": "Given Targets illustrations",

    "given targets same bg": "Given Targets Same BG",
    "given target same bg": "Given Targets Same BG",
    "same bg target": "Given Targets Same BG",

    "given targets multiple bg": "Given Targets Multiple BG",
    "given target multiple bg": "Given Targets Multiple BG",
    "multiple bg target": "Given Targets Multiple BG",

    "completed illustrations": "Completed illustrations",
    "illustrations completed": "Completed illustrations",

    "completed same bg": "Completed Same BG",
    "same bg completed": "Completed Same BG",

    "completed multiple bg": "Completed Multiple BG",
    "multiple bg completed": "Completed Multiple BG"
}

# =========================================================
# 5. WORK CATEGORY CONFIGURATION
# =========================================================
CATEGORIES = {
    "Normal Illustrations": {
        "target": "Given Targets illustrations",
        "completed": "Completed illustrations",
        "color": "#64b5f6"
    },
    "Story Scenes - Same BG": {
        "target": "Given Targets Same BG",
        "completed": "Completed Same BG",
        "color": "#81c784"
    },
    "Story Scenes - Multiple BG": {
        "target": "Given Targets Multiple BG",
        "completed": "Completed Multiple BG",
        "color": "#ffb74d"
    }
}

# =========================================================
# 6. HELPER FUNCTIONS
# =========================================================
def productivity_percentage(completed, target):
    """Calculate productivity percentage safely."""
    if pd.isna(target) or target <= 0:
        return np.nan

    return (completed / target) * 100


def format_percentage(value):
    """Format a percentage for display."""
    if pd.isna(value):
        return "N/A"

    return f"{value:.2f}%"


def style_chart(fig, height=420):
    """Apply consistent dark theme and white chart text."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#ffffff", size=12),
        title_font=dict(color="#ffffff", size=18),
        legend_title_font=dict(color="#ffffff"),
        height=height,
        margin=dict(l=20, r=25, t=65, b=40)
    )

    fig.update_xaxes(
        color="#ffffff",
        gridcolor="#334155",
        title_font_color="#ffffff",
        tickfont_color="#ffffff"
    )

    fig.update_yaxes(
        color="#ffffff",
        gridcolor="#334155",
        title_font_color="#ffffff",
        tickfont_color="#ffffff"
    )

    return fig


def prepare_employee_data(raw_df):
    """Clean uploaded data and calculate productivity metrics."""
    df = raw_df.copy()

    rename_map = {}

    for col in df.columns:
        normalized = str(col).strip().lower()

        if normalized in ALIASES:
            rename_map[col] = ALIASES[normalized]

    df = df.rename(columns=rename_map)

    if df.columns.duplicated().any():
        raise ValueError(
            "Duplicate column names found. Please correct the spreadsheet."
        )

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    df = df[REQUIRED_COLUMNS].copy()

    df["Employee Name"] = (
        df["Employee Name"].astype("string").str.strip()
    )

    if (
        df["Employee Name"].isna().any()
        or (df["Employee Name"] == "").any()
    ):
        raise ValueError(
            "Every employee record must contain an employee name."
        )

    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[NUMERIC_COLUMNS].isna().any().any():
        invalid_cols = df[NUMERIC_COLUMNS].columns[
            df[NUMERIC_COLUMNS].isna().any()
        ].tolist()

        raise ValueError(
            "Blank or non-numeric values found in: "
            + ", ".join(invalid_cols)
        )

    if (df[NUMERIC_COLUMNS] < 0).any().any():
        raise ValueError("Negative values are not allowed.")

    if df["Employee Name"].duplicated().any():
        duplicate_names = df.loc[
            df["Employee Name"].duplicated(keep=False),
            "Employee Name"
        ].unique().tolist()

        raise ValueError(
            "Duplicate employee names found: "
            + ", ".join(duplicate_names)
            + ". Combine duplicate rows before uploading."
        )

    # Calculate each category
    for category, config in CATEGORIES.items():
        target_col = config["target"]
        completed_col = config["completed"]

        df[f"{category} - Given Target"] = df[target_col]
        df[f"{category} - Completed"] = df[completed_col]

        df[f"{category} - Pending"] = (
            df[target_col] - df[completed_col]
        ).clip(lower=0)

        df[f"{category} - Productivity (%)"] = [
            productivity_percentage(completed, target)
            for completed, target in zip(
                df[completed_col],
                df[target_col]
            )
        ]

        df[f"{category} - Target Difference"] = (
            df[completed_col] - df[target_col]
        )

    target_cols = [
        config["target"] for config in CATEGORIES.values()
    ]

    completed_cols = [
        config["completed"] for config in CATEGORIES.values()
    ]

    df["Total Given Target"] = df[target_cols].sum(axis=1)
    df["Total Completed"] = df[completed_cols].sum(axis=1)

    df["Total Pending"] = (
        df["Total Given Target"] - df["Total Completed"]
    ).clip(lower=0)

    df["Overall Productivity (%)"] = [
        productivity_percentage(completed, target)
        for completed, target in zip(
            df["Total Completed"],
            df["Total Given Target"]
        )
    ]

    df["Targets Exceeded"] = (
        df["Total Completed"] > df["Total Given Target"]
    )

    return df


def build_category_summary(df):
    """Build category-level target, completed, pending, and productivity."""
    rows = []

    for category, config in CATEGORIES.items():
        target = df[config["target"]].sum()
        completed = df[config["completed"]].sum()

        rows.append({
            "Category": category,
            "Given Target": target,
            "Completed": completed,
            "Pending": max(target - completed, 0),
            "Productivity (%)": productivity_percentage(
                completed, target
            )
        })

    return pd.DataFrame(rows)


# =========================================================
# 7. DASHBOARD HEADER
# =========================================================
st.title("🎨 Illustrator Team Analytics Dashboard")

st.markdown(
    """
    <div class="dashboard-note">
        <b>Employee performance and productivity analytics</b><br>
        Track Normal Illustrations, Same BG Story Scenes, and
        Multiple BG Story Scenes separately. Compare targets,
        completed work, pending work, and productivity.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 8. UPLOAD FILE FIRST
# =========================================================
st.subheader("📂 Upload Employee Data")

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help="Upload a spreadsheet containing all required employee columns."
)

if uploaded_file is None:
    st.info("Upload your employee data file to open the dashboard.")

    with st.expander("View required spreadsheet columns"):
        st.code(
            "\n".join(REQUIRED_COLUMNS),
            language="text"
        )

    st.stop()

# =========================================================
# 9. READ AND VALIDATE FILE
# =========================================================
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

    df = prepare_employee_data(raw_df)

except Exception as error:
    st.error(f"Unable to load your file: {error}")
    st.stop()

if df.empty:
    st.warning("The uploaded file contains no employee records.")
    st.stop()

st.success(
    f"Successfully loaded {len(df)} employee records."
)

# =========================================================
# 10. SIDEBAR FILTERS
# =========================================================
st.sidebar.title("🔎 Dashboard Filters")

employee_list = sorted(df["Employee Name"].tolist())

selected_employees = st.sidebar.multiselect(
    "Select employees",
    options=employee_list,
    default=employee_list
)

st.sidebar.divider()

st.sidebar.caption(
    "Productivity = Completed ÷ Given Target × 100"
)

st.sidebar.caption(
    "Pending work = Target − Completed, with a minimum of zero."
)

if not selected_employees:
    st.warning("Select at least one employee from the sidebar.")
    st.stop()

filtered_df = df[
    df["Employee Name"].isin(selected_employees)
].copy()

# =========================================================
# 11. OVERALL TEAM OVERVIEW
# =========================================================
st.header("📊 Overall Team Overview")

employee_count = len(filtered_df)
total_leaves = filtered_df["Leaves"].sum()
total_working_days = filtered_df["Total Working Days"].sum()

total_target = filtered_df["Total Given Target"].sum()
total_completed = filtered_df["Total Completed"].sum()
total_pending = filtered_df["Total Pending"].sum()

overall_pct = productivity_percentage(
    total_completed, total_target
)

exceeded_count = int(filtered_df["Targets Exceeded"].sum())

row1 = st.columns(4)

row1[0].metric("Total Employees", f"{employee_count:,}")
row1[1].metric("Total Leaves", f"{total_leaves:,.1f}")
row1[2].metric("Total Working Days", f"{total_working_days:,.1f}")
row1[3].metric("Total Given Target", f"{total_target:,.0f}")

row2 = st.columns(4)

row2[0].metric("Total Completed", f"{total_completed:,.0f}")
row2[1].metric("Total Pending", f"{total_pending:,.0f}")
row2[2].metric("Overall Productivity", format_percentage(overall_pct))
row2[3].metric("Employees Exceeding Total Target", f"{exceeded_count}")

st.caption(
    "Overall productivity uses total completed work divided by total "
    "target, rather than the simple average of employee percentages."
)

st.divider()

# =========================================================
# 12. NORMAL ILLUSTRATIONS ANALYTICS
# =========================================================
st.header("🖼️ Normal Illustrations Analytics")

normal_target = filtered_df["Given Targets illustrations"].sum()
normal_completed = filtered_df["Completed illustrations"].sum()

normal_pending = max(normal_target - normal_completed, 0)

normal_pct = productivity_percentage(
    normal_completed, normal_target
)

normal_metrics = st.columns(4)

normal_metrics[0].metric("Given Illustrations", f"{normal_target:,.0f}")
normal_metrics[1].metric("Completed Illustrations", f"{normal_completed:,.0f}")
normal_metrics[2].metric("Pending Illustrations", f"{normal_pending:,.0f}")
normal_metrics[3].metric("Productivity", format_percentage(normal_pct))

normal_chart_data = filtered_df[
    [
        "Employee Name",
        "Given Targets illustrations",
        "Completed illustrations"
    ]
].melt(
    id_vars="Employee Name",
    var_name="Work Type",
    value_name="Illustration Count"
)

normal_fig = px.bar(
    normal_chart_data,
    x="Employee Name",
    y="Illustration Count",
    color="Work Type",
    barmode="group",
    title="Normal Illustrations: Given vs Completed",
    color_discrete_map={
        "Given Targets illustrations": "#64b5f6",
        "Completed illustrations": "#81c784"
    },
    text_auto=True
)

st.plotly_chart(
    style_chart(normal_fig, 430),
    use_container_width=True
)

st.divider()

# =========================================================
# 13. STORY SCENES ANALYTICS
# =========================================================
st.header("🎬 Story Scenes Analytics")

st.markdown(
    """
    <p class="section-caption">
    Same BG and Multiple BG Story Scenes have separate target,
    completed, pending, and productivity metrics.
    </p>
    """,
    unsafe_allow_html=True
)

same_bg_target = filtered_df["Given Targets Same BG"].sum()
same_bg_completed = filtered_df["Completed Same BG"].sum()
same_bg_pending = max(same_bg_target - same_bg_completed, 0)

same_bg_pct = productivity_percentage(
    same_bg_completed, same_bg_target
)

multi_bg_target = filtered_df["Given Targets Multiple BG"].sum()
multi_bg_completed = filtered_df["Completed Multiple BG"].sum()
multi_bg_pending = max(multi_bg_target - multi_bg_completed, 0)

multi_bg_pct = productivity_percentage(
    multi_bg_completed, multi_bg_target
)

same_tab, multi_tab = st.tabs([
    "🟢 Same BG Story Scenes",
    "🟠 Multiple BG Story Scenes"
])

with same_tab:
    st.subheader("Same BG Story Scenes")

    same_metrics = st.columns(4)

    same_metrics[0].metric("Given Target", f"{same_bg_target:,.0f}")
    same_metrics[1].metric("Completed", f"{same_bg_completed:,.0f}")
    same_metrics[2].metric("Pending", f"{same_bg_pending:,.0f}")
    same_metrics[3].metric("Productivity", format_percentage(same_bg_pct))

    same_chart_data = filtered_df[
        [
            "Employee Name",
            "Given Targets Same BG",
            "Completed Same BG"
        ]
    ].melt(
        id_vars="Employee Name",
        var_name="Work Type",
        value_name="Scene Count"
    )

    same_fig = px.bar(
        same_chart_data,
        x="Employee Name",
        y="Scene Count",
        color="Work Type",
        barmode="group",
        title="Same BG: Given vs Completed",
        color_discrete_map={
            "Given Targets Same BG": "#64b5f6",
            "Completed Same BG": "#81c784"
        },
        text_auto=True
    )

    st.plotly_chart(
        style_chart(same_fig, 420),
        use_container_width=True
    )

with multi_tab:
    st.subheader("Multiple BG Story Scenes")

    multi_metrics = st.columns(4)

    multi_metrics[0].metric("Given Target", f"{multi_bg_target:,.0f}")
    multi_metrics[1].metric("Completed", f"{multi_bg_completed:,.0f}")
    multi_metrics[2].metric("Pending", f"{multi_bg_pending:,.0f}")
    multi_metrics[3].metric("Productivity", format_percentage(multi_bg_pct))

    multi_chart_data = filtered_df[
        [
            "Employee Name",
            "Given Targets Multiple BG",
            "Completed Multiple BG"
        ]
    ].melt(
        id_vars="Employee Name",
        var_name="Work Type",
        value_name="Scene Count"
    )

    multi_fig = px.bar(
        multi_chart_data,
        x="Employee Name",
        y="Scene Count",
        color="Work Type",
        barmode="group",
        title="Multiple BG: Given vs Completed",
        color_discrete_map={
            "Given Targets Multiple BG": "#64b5f6",
            "Completed Multiple BG": "#ffb74d"
        },
        text_auto=True
    )

    st.plotly_chart(
        style_chart(multi_fig, 420),
        use_container_width=True
    )

st.divider()

# =========================================================
# 14. CATEGORY SUMMARY
# =========================================================
st.header("📌 Category Summary")

summary_df = build_category_summary(filtered_df)

summary_display = summary_df.copy()
summary_display["Productivity (%)"] = (
    summary_display["Productivity (%)"].round(2)
)

st.dataframe(
    summary_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Given Target": st.column_config.NumberColumn(format="%d"),
        "Completed": st.column_config.NumberColumn(format="%d"),
        "Pending": st.column_config.NumberColumn(format="%d"),
        "Productivity (%)": st.column_config.NumberColumn(format="%.2f%%")
    }
)

summary_chart_data = summary_df.melt(
    id_vars="Category",
    value_vars=["Given Target", "Completed", "Pending"],
    var_name="Metric",
    value_name="Count"
)

summary_fig = px.bar(
    summary_chart_data,
    x="Category",
    y="Count",
    color="Metric",
    barmode="group",
    title="Given Target vs Completed vs Pending by Category",
    color_discrete_map={
        "Given Target": "#64b5f6",
        "Completed": "#81c784",
        "Pending": "#ffb74d"
    },
    text_auto=True
)

st.plotly_chart(
    style_chart(summary_fig, 430),
    use_container_width=True
)

st.divider()

# =========================================================
# 15. EMPLOYEE PERFORMANCE RANKINGS
# =========================================================
st.header("🏆 Employee Performance Rankings")

ranking_df = filtered_df[
    [
        "Employee Name",
        "Total Given Target",
        "Total Completed",
        "Total Pending",
        "Overall Productivity (%)",
        "Targets Exceeded"
    ]
].copy()

ranking_df = ranking_df.sort_values(
    "Overall Productivity (%)",
    ascending=False,
    na_position="last"
)

valid_rankings = ranking_df.dropna(
    subset=["Overall Productivity (%)"]
)

left, right = st.columns(2)

with left:
    st.subheader("Highest Productivity")

    if not valid_rankings.empty:
        best = valid_rankings.iloc[0]

        st.metric(
            str(best["Employee Name"]),
            format_percentage(best["Overall Productivity (%)"])
        )
    else:
        st.info("No valid target data is available.")

with right:
    st.subheader("Lowest Productivity")

    if not valid_rankings.empty:
        lowest = valid_rankings.iloc[-1]

        st.metric(
            str(lowest["Employee Name"]),
            format_percentage(lowest["Overall Productivity (%)"])
        )
    else:
        st.info("No valid target data is available.")

ranking_display = ranking_df.copy()

ranking_display["Overall Productivity (%)"] = (
    ranking_display["Overall Productivity (%)"].round(2)
)

st.dataframe(
    ranking_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Total Given Target": st.column_config.NumberColumn(format="%d"),
        "Total Completed": st.column_config.NumberColumn(format="%d"),
        "Total Pending": st.column_config.NumberColumn(format="%d"),
        "Overall Productivity (%)": st.column_config.NumberColumn(format="%.2f%%"),
        "Targets Exceeded": st.column_config.CheckboxColumn()
    }
)

ranking_chart_df = ranking_df.sort_values(
    "Overall Productivity (%)",
    ascending=True,
    na_position="first"
)

ranking_fig = px.bar(
    ranking_chart_df,
    x="Overall Productivity (%)",
    y="Employee Name",
    orientation="h",
    color="Overall Productivity (%)",
    color_continuous_scale=[
        "#ffb74d",
        "#64b5f6",
        "#81c784"
    ],
    title="Overall Productivity by Employee",
    text="Overall Productivity (%)"
)

ranking_fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

st.plotly_chart(
    style_chart(ranking_fig, max(420, len(ranking_df) * 32)),
    use_container_width=True
)

st.divider()

# =========================================================
# 16. INDIVIDUAL EMPLOYEE REPORT
# =========================================================
st.header("👤 Individual Employee Performance")

individual_name = st.selectbox(
    "Choose an employee",
    options=sorted(filtered_df["Employee Name"].tolist()),
    key="individual_employee"
)

employee = filtered_df[
    filtered_df["Employee Name"] == individual_name
].iloc[0]

st.subheader(f"Employee Report: {individual_name}")

emp_row1 = st.columns(4)

emp_row1[0].metric("Leaves", f"{employee['Leaves']:,.1f}")
emp_row1[1].metric("Working Days", f"{employee['Total Working Days']:,.1f}")
emp_row1[2].metric("Total Given Target", f"{employee['Total Given Target']:,.0f}")
emp_row1[3].metric("Total Completed", f"{employee['Total Completed']:,.0f}")

emp_row2 = st.columns(4)

emp_row2[0].metric("Total Pending", f"{employee['Total Pending']:,.0f}")

emp_row2[1].metric(
    "Overall Productivity",
    format_percentage(employee["Overall Productivity (%)"])
)

emp_row2[2].metric(
    "Normal Illustration Productivity",
    format_percentage(
        employee["Normal Illustrations - Productivity (%)"]
    )
)

emp_row2[3].metric(
    "Total Target Exceeded",
    "Yes" if employee["Targets Exceeded"] else "No"
)

individual_rows = []

for category, config in CATEGORIES.items():
    target = employee[config["target"]]
    completed = employee[config["completed"]]

    individual_rows.append({
        "Category": category,
        "Given Target": target,
        "Completed": completed,
        "Pending": max(target - completed, 0),
        "Productivity (%)": productivity_percentage(completed, target),
        "Target Difference": completed - target
    })

individual_df = pd.DataFrame(individual_rows)

individual_display = individual_df.copy()
individual_display["Productivity (%)"] = (
    individual_display["Productivity (%)"].round(2)
)

st.subheader("Category-wise Performance Details")

st.dataframe(
    individual_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Given Target": st.column_config.NumberColumn(format="%d"),
        "Completed": st.column_config.NumberColumn(format="%d"),
        "Pending": st.column_config.NumberColumn(format="%d"),
        "Productivity (%)": st.column_config.NumberColumn(format="%.2f%%"),
        "Target Difference": st.column_config.NumberColumn(format="%d")
    }
)

individual_chart_data = individual_df.melt(
    id_vars="Category",
    value_vars=["Given Target", "Completed", "Pending"],
    var_name="Metric",
    value_name="Work Count"
)

individual_fig = px.bar(
    individual_chart_data,
    x="Category",
    y="Work Count",
    color="Metric",
    barmode="group",
    title=f"{individual_name}: Target vs Completed vs Pending",
    color_discrete_map={
        "Given Target": "#64b5f6",
        "Completed": "#81c784",
        "Pending": "#ffb74d"
    },
    text_auto=True
)

st.plotly_chart(
    style_chart(individual_fig, 430),
    use_container_width=True
)

st.divider()

# =========================================================
# 17. COMPLETE TEAM DATA SHEET - CLEANED COLUMNS
# =========================================================
st.header("📋 Complete Team Data Sheet")

st.caption(
    "Original employee details and productivity percentages. "
    "Redundant target, completed, and target-difference columns "
    "are hidden from this table."
)

# Remove the extra category target/completed/difference columns
columns_to_remove = [
    "Normal Illustrations - Given Target",
    "Normal Illustrations - Completed",
    "Normal Illustrations - Target Difference",

    "Story Scenes - Same BG - Given Target",
    "Story Scenes - Same BG - Completed",
    "Story Scenes - Same BG - Target Difference",

    "Story Scenes - Multiple BG - Given Target",
    "Story Scenes - Multiple BG - Completed",
    "Story Scenes - Multiple BG - Target Difference"
]

team_display_df = filtered_df.drop(
    columns=columns_to_remove,
    errors="ignore"
).copy()

# Round percentages
team_percentage_columns = [
    col for col in team_display_df.columns
    if "Productivity (%)" in col
]

for col in team_percentage_columns:
    team_display_df[col] = team_display_df[col].round(2)

st.dataframe(
    team_display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =========================================================
# 18. DOWNLOAD REPORTS
# =========================================================
st.header("⬇️ Download Reports")

# Keep detailed columns in downloads for complete reporting
report_columns = (
    REQUIRED_COLUMNS
    + [
        "Normal Illustrations - Given Target",
        "Normal Illustrations - Completed",
        "Normal Illustrations - Pending",
        "Normal Illustrations - Productivity (%)",
        "Normal Illustrations - Target Difference",

        "Story Scenes - Same BG - Given Target",
        "Story Scenes - Same BG - Completed",
        "Story Scenes - Same BG - Pending",
        "Story Scenes - Same BG - Productivity (%)",
        "Story Scenes - Same BG - Target Difference",

        "Story Scenes - Multiple BG - Given Target",
        "Story Scenes - Multiple BG - Completed",
        "Story Scenes - Multiple BG - Pending",
        "Story Scenes - Multiple BG - Productivity (%)",
        "Story Scenes - Multiple BG - Target Difference",

        "Total Given Target",
        "Total Completed",
        "Total Pending",
        "Overall Productivity (%)",
        "Targets Exceeded"
    ]
)

report_df = filtered_df[report_columns].copy()

for col in report_df.columns:
    if "Productivity (%)" in col:
        report_df[col] = report_df[col].round(2)

csv_data = report_df.to_csv(
    index=False
).encode("utf-8-sig")

download_col1, download_col2 = st.columns(2)

with download_col1:
    st.download_button(
        label="📥 Download Detailed CSV",
        data=csv_data,
        file_name="illustrator_team_analytics.csv",
        mime="text/csv",
        use_container_width=True
    )

with download_col2:
    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:
        report_df.to_excel(
            writer,
            sheet_name="Employee Summary",
            index=False
        )

        summary_display.to_excel(
            writer,
            sheet_name="Category Summary",
            index=False
        )

        ranking_display.to_excel(
            writer,
            sheet_name="Employee Rankings",
            index=False
        )

        individual_display.to_excel(
            writer,
            sheet_name="Selected Employee",
            index=False
        )

    st.download_button(
        label="📥 Download Multi-Sheet Excel",
        data=excel_buffer.getvalue(),
        file_name="illustrator_team_analytics.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )

# =========================================================
# 19. FOOTER
# =========================================================
st.divider()

st.caption(
    "Illustrator Team Analytics Dashboard | "
    "Productivity = Completed Work ÷ Given Target × 100 | "
    "Pending work is capped at zero when the target is exceeded."
)
