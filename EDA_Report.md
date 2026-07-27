# Opportunity Dataset Exploratory Data Analysis (EDA)

## 1. Project Overview

This project analyzes the Opportunity Dataset using Python, Pandas, Plotly, and Streamlit.

The objectives were to:

- Clean the dataset
- Handle missing values
- Standardize date formats
- Remove duplicate records
- Explore numerical and categorical variables
- Build an interactive dashboard

---

# 2. Dataset Overview

| Metric | Value |
|---------|-------|
| Records | 5733 |
| Columns | 33 |

The dataset contains information about educational opportunities including internships, scholarships, events, competitions, and programs.

---

# 3. Data Cleaning

The following cleaning steps were performed:

- Removed duplicate rows
- Standardized date columns
- Converted timestamps
- Handled missing values
- Corrected data types
- Fixed inconsistent values

---

# 4. Missing Values Analysis

Several columns contained missing values.

Examples include:

- image_link
- location
- PanelList
- Reward
- Tracking Questions

Missing values were retained where appropriate because they represent unavailable information rather than incorrect data.

---

# 5. Summary Statistics

Summary statistics were generated for all numerical columns.

Metrics include:

- Count
- Mean
- Standard Deviation
- Minimum
- Quartiles
- Maximum

---

# 6. Dashboard Features

The Streamlit dashboard includes:

- Dataset Preview
- Dataset Information
- Cleaning Summary
- KPI Cards
- Summary Statistics
- Missing Value Analysis
- Duplicate Analysis
- Interactive Charts

---

# 7. Key Findings

- Dataset contains 5733 records.
- No duplicate records were detected after cleaning.
- Several optional fields contain missing values.
- Date fields were successfully standardized.
- Most opportunity durations are less than one month.

---

# 8. Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit

---

# 9. Conclusion

The dataset was successfully cleaned and explored using Python.

The resulting dashboard provides an interactive way to inspect the data, identify missing values, view summary statistics, and explore opportunity distributions.