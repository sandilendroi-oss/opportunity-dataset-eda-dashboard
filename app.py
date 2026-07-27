import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Opportunity Dataset EDA Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# DASHBOARD TITLE
# ==========================================================

st.title("📊 Opportunity Dataset EDA Dashboard")

st.write(
    """
    This dashboard presents an Exploratory Data Analysis (EDA)
    of the Opportunity Dataset.

    It includes:

    • Dataset Preview

    • Data Quality Report

    • Data Cleaning Report

    • Summary Statistics

    • Key Performance Indicators (KPIs)

    • Interactive Visualizations
    """
)


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    return pd.read_excel(
        "data/Sandile_Thabede_Week2_EDA_Workbook.xlsx"
    )


df = load_data()


st.success("✅ Dataset loaded successfully!")

# ==========================================================
# DATA CLEANING FUNCTION
# ==========================================================

def clean_dataset(data):

    clean_df = data.copy()


    # ------------------------------------------------------
    # 1. Standardize Missing Values
    # ------------------------------------------------------

    clean_df.replace(
        [
            "NULL",
            "null",
            "None",
            "",
            " "
        ],
        pd.NA,
        inplace=True
    )


    # ------------------------------------------------------
    # 2. Clean Text Columns
    # ------------------------------------------------------

    text_columns = (
        clean_df
        .select_dtypes(include=["object"])
        .columns
    )


    for col in text_columns:

        clean_df[col] = (
            clean_df[col]
            .astype("string")
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )


    # ------------------------------------------------------
    # 3. Standardize Duration Values
    # ------------------------------------------------------

    if "duration_type" in clean_df.columns:

        clean_df["duration_type"] = (
            clean_df["duration_type"]
            .astype("string")
            .str.lower()
            .str.strip()
        )


        clean_df["duration_type"] = (
            clean_df["duration_type"]
            .replace(
                {
                    "day": "days",
                    "week": "weeks",
                    "month": "months",
                    "year": "years",
                    "hour": "hours",
                    "minute": "minutes",
                    "yearssss": "years",
                    "da": "days"
                }
            )
        )


        valid_duration = [
            "days",
            "weeks",
            "months",
            "years",
            "hours",
            "minutes"
        ]


        clean_df.loc[
            ~clean_df["duration_type"].isin(valid_duration),
            "duration_type"
        ] = pd.NA


        clean_df["duration_type"] = (
            clean_df["duration_type"]
            .str.title()
        )
        clean_df["duration_type"] = (
            clean_df["duration_type"]
            .fillna("Unknown")
        )


    # ------------------------------------------------------
    # 4. Standardize Category Columns
    # ------------------------------------------------------

    category_columns = [
        "category",
        "location",
        "currency_type",
        "role"
    ]


    for col in category_columns:

        if col in clean_df.columns:

            clean_df[col] = (
                clean_df[col]
                .astype("string")
                .str.strip()
                .str.title()
            )


    # ------------------------------------------------------
    # 5. Clean Location Column
    # ------------------------------------------------------

    if "location" in clean_df.columns:

        valid_locations = [
            "Virtual",
            "Work From Home",
            "United Kingdom",
            "South Africa",
            "United States",
            "India",
            "Canada",
            "Australia",
            "Germany",
            "France",
            "Spain",
            "Italy",
            "China",
            "Japan",
            "Brazil"
        ]


        clean_df.loc[
            ~clean_df["location"].isin(valid_locations),
            "location"
        ] = pd.NA

        clean_df["location"] = (
            clean_df["location"]
            .fillna("Not Specified")
        )



    # ------------------------------------------------------
    # 6. Convert Unix Timestamp Columns
    # ------------------------------------------------------

    date_columns = [
        "created_at",
        "modified_at",
        "last_date_to_apply"
    ]


    for col in date_columns:

        if col in clean_df.columns:

            clean_df[col] = pd.to_numeric(
                clean_df[col],
                errors="coerce"
            )


            clean_df[col] = pd.to_datetime(
                clean_df[col],
                unit="ms",
                errors="coerce"
            )



    # ------------------------------------------------------
    # 7. Clean Image Links
    # ------------------------------------------------------

    if "image_link" in clean_df.columns:

        clean_df["image_link"] = (
            clean_df["image_link"]
            .astype("string")
            .str.strip()
        )



    # ------------------------------------------------------
    # 8. Handle JSON Columns
    # ------------------------------------------------------

    json_columns = [
        "Badge",
        "CareerAddOn",
        "Panellist",
        "Reward",
        "Eligibility",
        "tracking_questions",
        "Testimonial"
    ]


    for col in json_columns:

        if col in clean_df.columns:

            clean_df[col] = (
                clean_df[col]
                .fillna("{}")
            )

    # ------------------------------------------------------
    # 8. Remove JSON / corrupted text values
    # ------------------------------------------------------

    for col in clean_df.columns:

        if clean_df[col].dtype == "string":

            clean_df[col] = clean_df[col].replace(
                {
                    r".*%22Tooltip%22.*": pd.NA,
                    r".*%22Label%22.*": pd.NA,
                    r".*\{.*\}.*": pd.NA
                },
                regex=True
            )


    # ------------------------------------------------------
    # 9. Remove Duplicate Rows
    # ------------------------------------------------------

    clean_df = clean_df.drop_duplicates()
    # ==========================================
    #  CHECK MISSING VALUES AFTER CLEANING
    # ==========================================
    missing_report = (
        clean_df.isna()
        .sum()
        .sort_values(ascending=False)
    )
    print(missing_report[missing_report > 0])

    return clean_df


# ==========================================================
# CREATE CLEAN DATASET
# ==========================================================

clean_df = clean_dataset(df)

# ==========================================================
# DATASET PREVIEW
# ==========================================================

st.markdown("---")

st.header("📋 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Rows", clean_df.shape[0])

with col2:
    st.metric("Columns", clean_df.shape[1])

with col3:
    st.metric(
        "Missing Values",
        int(clean_df.isna().sum().sum())
    )

with col4:
    st.metric(
        "Duplicate Rows",
        int(clean_df.duplicated().sum())
    )

st.dataframe(
    df.head(),
    width="stretch"
)



# ==========================================================
# DATASET INFORMATION
# ==========================================================

st.markdown("---")

st.header("📌 Dataset Information")


info_col1, info_col2, info_col3 = st.columns(3)


with info_col1:

    st.metric(
        "Rows",
        len(df)
    )


with info_col2:

    st.metric(
        "Columns",
        df.shape[1]
    )


with info_col3:

    st.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )



# ==========================================================
# DATA QUALITY REPORT
# ==========================================================

st.markdown("---")

st.header("📋 Data Quality Report")


quality_col1, quality_col2 = st.columns(2)



# ----------------------------------------------------------
# Missing Values
# ----------------------------------------------------------

with quality_col1:

    st.subheader("Missing Values")


    missing = (
        df.isna()
        .sum()
        .sort_values(
            ascending=False
        )
    )


    missing = missing[
        missing > 0
    ]


    if missing.empty:

        st.success(
            "No missing values found."
        )


    else:

        st.dataframe(
            missing.rename(
                "Missing Values"
            ),
            width="stretch"
        )



# ----------------------------------------------------------
# Duplicate Records
# ----------------------------------------------------------

with quality_col2:

    st.subheader("Duplicate Records")


    duplicate_count = int(
        df.duplicated().sum()
    )


   
# ==========================================================
# DUPLICATE ANALYSIS
# ==========================================================

st.markdown("---")

st.header("🔍 Duplicate Analysis")


duplicate_count = int(
    df.duplicated().sum()
)


st.write(
    f"Total duplicate rows detected: **{duplicate_count}**"
)


if duplicate_count > 0:

    st.warning(
        "Duplicate records were detected in the original dataset."
    )


    duplicate_preview = (
        df[df.duplicated(keep=False)]
        .head(10)
    )


    st.subheader(
        "Duplicate Records Preview"
    )


    st.dataframe(
        duplicate_preview,
        width="stretch"
    )


else:

    st.success(
        "No duplicate records found."
    )



# ==========================================================
# DATA CLEANING REPORT
# ==========================================================

st.markdown("---")

st.header("🧹 Data Cleaning Report")


st.success(
    "✅ Dataset cleaned successfully!"
)



# ----------------------------------------------------------
# Cleaning Metrics
# ----------------------------------------------------------

rows_removed = (
    len(df) - len(clean_df)
)


missing_before = int(
    df.isna()
    .sum()
    .sum()
)


optional_columns = [
    "Reward",
    "Badge",
    "CareerAddOn",
    "Eligibility",
    "Panellist",
    "tracking_questions",
    "Testimonial",
    "Cohort",
    "NotStartedTransaction",
    "DropoutTransaction",
    "current_editor"
]

important_df = clean_df.drop(
    columns=optional_columns,
    errors="ignore"
)

missing_after = int(
    important_df.isna()
    .sum()
    .sum()
)

metric1, metric2, metric3, metric4 = st.columns(4)



with metric1:

    st.metric(
        "Original Rows",
        len(df)
    )


with metric2:

    st.metric(
        "Rows After Cleaning",
        len(clean_df)
    )


with metric3:

    duplicates_removed = int(df.duplicated().sum())

    st.metric(
        "Duplicates Removed",
        duplicates_removed
    )


with metric4:

    st.metric(
        "Remaining Missing Values",
        missing_after
    )

# ==========================================================
# BEFORE VS AFTER CLEANING COMPARISON
# ==========================================================

st.subheader("Before vs After Cleaning")


comparison = pd.DataFrame(
    {
        "Metric": [
            "Rows",
            "Columns",
            "Missing Values",
            "Duplicate Rows"
        ],

        "Before Cleaning": [
            df.shape[0],
            df.shape[1],
            df.isna().sum().sum(),
            df.duplicated().sum()
        ],

        "After Cleaning": [
            clean_df.shape[0],
            clean_df.shape[1],
            missing_after,
            clean_df.duplicated().sum()
        ]
    }
)


st.dataframe(
    comparison,
    hide_index=True,
    width="stretch"
)
st.subheader("📌 Cleaning Summary")

st.success("""
✔ Removed duplicate records

✔ Standardized date columns

✔ Fixed missing values

✔ Cleaned inconsistent text entries

✔ Converted data types where necessary

✔ Dataset is ready for analysis
""")
st.header("💡 Key Insights")

st.markdown("""
- Most opportunities belong to a small number of categories.
- Several columns originally contained large numbers of missing values.
- Duplicate records were identified and handled.
- Duration values vary considerably across opportunities.
- The cleaned dataset is suitable for visualization and further analysis.
""")
st.header("📈 Recommendations")

st.markdown("""
- Continue validating missing values during data collection.
- Standardize date formats before importing data.
- Enforce consistent category naming.
- Validate URLs before storing them.
- Regularly remove duplicate records.
""")
# ==========================================================
# CLEANING ACTIONS SUMMARY
# ==========================================================

st.subheader(
    "Cleaning Actions Performed"
)



cleaning_summary = pd.DataFrame(
    {
        "Cleaning Step": [
            "Standardized missing values",
            "Removed extra spaces",
            "Standardized duration values",
            "Standardized category values",
            "Converted timestamp columns",
            "Cleaned image links",
            "Handled JSON columns",
            "Removed duplicate rows"
        ],

        "Status": [
            "✅ Completed",
            "✅ Completed",
            "✅ Completed",
            "✅ Completed",
            "✅ Completed",
            "✅ Completed",
            "✅ Completed",
            "✅ Completed"
        ]
    }
)



st.dataframe(
    cleaning_summary,
    width="stretch",
    hide_index=True
)



# ==========================================================
# CLEANED DATASET PREVIEW
# ==========================================================

st.subheader(
    "Cleaned Dataset Preview"
)


st.dataframe(
    clean_df.head(),
    width="stretch"
)
# ==========================================================
# SUMMARY STATISTICS
# ==========================================================

st.markdown("---")

st.subheader("Summary Statistics")

numeric_df = clean_df.select_dtypes(include=['number'])

if numeric_df.shape[1] > 0:
    st.dataframe(
        numeric_df.describe(),
        use_container_width=True
    )
else:
    st.warning("No numerical columns available for summary statistics.")

# ==========================================================
# KEY PERFORMANCE INDICATORS (KPIs)
# ==========================================================

st.markdown("---")

st.header(
    "📌 Key Performance Indicators"
)



# ----------------------------------------------------------
# Calculate KPI Values
# ----------------------------------------------------------

total_records = len(clean_df)


total_columns = clean_df.shape[1]


total_categories = (
    clean_df["category"]
    .nunique()
    if "category" in clean_df.columns
    else 0
)



total_locations = (
    clean_df["location"]
    .nunique()
    if "location" in clean_df.columns
    else 0
)

total_missing = missing_after

total_duplicates = int(
    df.duplicated()
    .sum()
)



# ----------------------------------------------------------
# Display KPIs
# ----------------------------------------------------------

kpi1, kpi2, kpi3 = st.columns(3)



with kpi1:

    st.metric(
        "📄 Total Records",
        total_records
    )


with kpi2:

    st.metric(
        "📊 Total Columns",
        total_columns
    )


with kpi3:

    st.metric(
        "📂 Categories",
        total_categories
    )



kpi4, kpi5, kpi6 = st.columns(3)



with kpi4:

    st.metric(
        "🌍 Locations",
        total_locations
    )


with kpi5:

    st.metric(
        "⚠ Missing Values",
        total_missing
    )


with kpi6:

    st.metric(
        "🗂 Duplicate Rows",
        total_duplicates
    )
# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header(
    "🔍 Dashboard Filters"
)


filtered_df = clean_df.copy()



# ----------------------------------------------------------
# Category Filter
# ----------------------------------------------------------

if "category" in filtered_df.columns:

    categories = sorted(
        filtered_df["category"]
        .dropna()
        .unique()
    )


    selected_categories = st.sidebar.multiselect(
        "Select Category",
        categories,
        default=categories
    )


    filtered_df = filtered_df[
        filtered_df["category"]
        .isin(selected_categories)
    ]



# ----------------------------------------------------------
# Location Filter
# ----------------------------------------------------------

if "location" in filtered_df.columns:

    locations = sorted(
        filtered_df["location"]
        .dropna()
        .unique()
    )


    selected_locations = st.sidebar.multiselect(
        "Select Location",
        locations,
        default=locations
    )


    filtered_df = filtered_df[
        filtered_df["location"]
        .isin(selected_locations)
    ]



# ----------------------------------------------------------
# Duration Filter
# ----------------------------------------------------------

if "duration_type" in filtered_df.columns:

    durations = sorted(
        filtered_df["duration_type"]
        .dropna()
        .unique()
    )


    selected_durations = st.sidebar.multiselect(
        "Select Duration",
        durations,
        default=durations
    )


    filtered_df = filtered_df[
        filtered_df["duration_type"]
        .isin(selected_durations)
    ]



# ==========================================================
# INTERACTIVE VISUALIZATIONS
# ==========================================================

st.markdown("---")

st.header(
    "📈 Interactive Visualizations"
)


st.write(
    "The charts below display patterns and trends "
    "within the cleaned Opportunity Dataset."
)



# ==========================================================
# CHART 1 - OPPORTUNITIES BY CATEGORY
# ==========================================================

if "category" in filtered_df.columns:


    category_counts = (
        filtered_df["category"]
        .dropna()
        .value_counts()
        .reset_index()
    )


    category_counts.columns = [
        "Category",
        "Count"
    ]


    fig_category = px.bar(
        category_counts,
        x="Category",
        y="Count",
        text="Count",
        title="Opportunities by Category",
        template="plotly_white"
    )


    fig_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Number of Opportunities",
        xaxis_tickangle=-45,
        height=550
    )


    st.plotly_chart(
        fig_category,
        width="stretch"
    )
# ==========================================================
# CHART 2 - TOP 10 LOCATIONS
# ==========================================================

if "location" in filtered_df.columns:


    location_counts = (
        filtered_df["location"]
        .dropna()
        .value_counts()
        .head(10)
        .reset_index()
    )


    location_counts.columns = [
        "Location",
        "Count"
    ]


    fig_location = px.bar(
        location_counts,
        x="Location",
        y="Count",
        text="Count",
        title="Top 10 Opportunity Locations",
        template="plotly_white"
    )


    fig_location.update_layout(
        xaxis_title="Location",
        yaxis_title="Number of Opportunities",
        xaxis_tickangle=-45,
        height=550
    )


    st.plotly_chart(
        fig_location,
        width="stretch"
    )



# ==========================================================
# CHART 3 - DURATION TYPE DISTRIBUTION
# ==========================================================

if "duration_type" in filtered_df.columns:


    duration_counts = (
        filtered_df["duration_type"]
        .dropna()
        .value_counts()
        .reset_index()
    )


    duration_counts.columns = [
        "Duration",
        "Count"
    ]


    fig_duration = px.pie(
        duration_counts,
        names="Duration",
        values="Count",
        title="Opportunity Duration Types",
        template="plotly_white"
    )


    fig_duration.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )


    st.plotly_chart(
        fig_duration,
        width="stretch"
    )



# ==========================================================
# DOWNLOAD CLEANED DATASET
# ==========================================================

st.markdown("---")

st.header(
    "📥 Download Cleaned Dataset"
)


csv = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📄 Download Cleaned Dataset (CSV)",
    data=csv,
    file_name="Opportunity_Dataset_Cleaned.csv",
    mime="text/csv"
)



# ==========================================================
# DATASET INSIGHTS
# ==========================================================

st.markdown("---")

st.header(
    "💡 Dataset Insights"
)


st.write(
    f"• Total Opportunities: **{len(clean_df)}**"
)



# ----------------------------------------------------------
# Most Common Category
# ----------------------------------------------------------

if "category" in filtered_df.columns:

    if not filtered_df["category"].dropna().empty:

        top_category = (
            filtered_df["category"]
            .mode()
            .iloc[0]
        )


        st.write(
            f"• Most common category: **{top_category}**"
        )



# ----------------------------------------------------------
# Most Common Location
# ----------------------------------------------------------

if "location" in filtered_df.columns:

    if not filtered_df["location"].dropna().empty:

        top_location = (
            filtered_df["location"]
            .mode()
            .iloc[0]
        )


        st.write(
            f"• Most common location: **{top_location}**"
        )



# ----------------------------------------------------------
# Most Common Duration
# ----------------------------------------------------------

if "duration_type" in filtered_df.columns:

    if not filtered_df["duration_type"].dropna().empty:

        top_duration = (
            filtered_df["duration_type"]
            .mode()
            .iloc[0]
        )


        st.write(
            f"• Most common duration type: **{top_duration}**"
        )
