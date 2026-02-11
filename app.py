import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="NFHS Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 All India National Family Health Survey Dashboard")

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("All India National Family Health Survey.csv")
    return df

df = load_data()

st.sidebar.header("Filter Options")

# ---------------------------
# Sidebar Filters
# ---------------------------
# Automatically detect categorical columns
categorical_cols = df.select_dtypes(include='object').columns.tolist()
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

selected_state = None
if "State" in df.columns:
    selected_state = st.sidebar.selectbox(
        "Select State",
        options=["All"] + sorted(df["State"].dropna().unique().tolist())
    )

if selected_state and selected_state != "All":
    df = df[df["State"] == selected_state]

# ---------------------------
# Show Raw Data
# ---------------------------
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# ---------------------------
# KPI Section
# ---------------------------
st.subheader("Key Indicators")

col1, col2, col3 = st.columns(3)

if numeric_cols:
    col1.metric("Total Records", len(df))
    col2.metric("Average Value", round(df[numeric_cols[0]].mean(), 2))
    col3.metric("Maximum Value", round(df[numeric_cols[0]].max(), 2))

# ---------------------------
# Visualization Section
# ---------------------------
st.subheader("Visualizations")

if numeric_cols and categorical_cols:
    selected_numeric = st.selectbox("Select Indicator", numeric_cols)
    selected_category = st.selectbox("Group By", categorical_cols)

    fig = px.bar(
        df,
        x=selected_category,
        y=selected_numeric,
        color=selected_category,
        title=f"{selected_numeric} by {selected_category}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Line Chart (if Year column exists)
# ---------------------------
if "Year" in df.columns and numeric_cols:
    st.subheader("Trend Over Time")

    selected_numeric_trend = st.selectbox(
        "Select Indicator for Trend",
        numeric_cols,
        key="trend"
    )

    fig2 = px.line(
        df,
        x="Year",
        y=selected_numeric_trend,
        color="State" if "State" in df.columns else None,
        markers=True
    )

    st.plotly_chart(fig2, use_container_width=True)

