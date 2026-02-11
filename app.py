import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(
    page_title="NFHS-5 Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS-5) Dashboard")
st.markdown("Interactive Dashboard for Health Indicators Analysis")

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey5.xlsx")
    return df

df = load_data()

# ------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------
st.sidebar.header("🔎 Filter Options")

# Detect columns
categorical_cols = df.select_dtypes(include="object").columns.tolist()
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

# State Filter (if exists)
if "State" in df.columns:
    selected_state = st.sidebar.selectbox(
        "Select State",
        ["All"] + sorted(df["State"].dropna().unique().tolist())
    )
    if selected_state != "All":
        df = df[df["State"] == selected_state]

# Year Filter (if exists)
if "Year" in df.columns:
    selected_year = st.sidebar.selectbox(
        "Select Year",
        ["All"] + sorted(df["Year"].dropna().unique().tolist())
    )
    if selected_year != "All":
        df = df[df["Year"] == selected_year]

# ------------------------------------------------
# KPI SECTION
# ------------------------------------------------
st.subheader("📌 Key Indicators")

col1, col2, col3 = st.columns(3)

if numeric_cols:
    col1.metric("Total Records", len(df))
    col2.metric("Average Value", round(df[numeric_cols[0]].mean(), 2))
    col3.metric("Highest Value", round(df[numeric_cols[0]].max(), 2))

# ------------------------------------------------
# BAR CHART SECTION
# ------------------------------------------------
st.subheader("📊 Indicator Comparison")

if numeric_cols and categorical_cols:
    selected_indicator = st.selectbox("Select Indicator", numeric_cols)
    selected_group = st.selectbox("Group By", categorical_cols)

    fig = px.bar(
        df,
        x=selected_group,
        y=selected_indicator,
        color=selected_group,
        title=f"{selected_indicator} by {selected_group}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------
# TREND ANALYSIS
# ------------------------------------------------
if "Year" in df.columns and numeric_cols:
    st.subheader("📈 Trend Analysis")

    selected_trend = st.selectbox(
        "Select Indicator for Trend",
        numeric_cols,
        key="trend"
    )

    fig2 = px.line(
        df,
        x="Year",
        y=selected_trend,
        color="State" if "State" in df.columns else None,
        markers=True,
        title=f"Trend of {selected_trend}"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------
# DATA TABLE + DOWNLOAD
# ------------------------------------------------
st.subheader("📄 Filtered Data")

st.dataframe(df)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Filtered Data as CSV",
    data=csv,
    file_name="nfhs_filtered_data.csv",
    mime="text/csv",
)

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.markdown("---")
st.markdown("Developed using Streamlit | NFHS-5 Data Dashboard")
