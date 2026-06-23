import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Factory Reallocation & Shipping Optimization",
    layout="wide"
)

st.title("🏭 Factory Reallocation & Shipping Optimization System")
st.markdown("### Nassau Candy Distributor")

# -----------------------------
# LOAD DATA
# -----------------------------
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

recommendations = pd.read_csv(
    BASE_DIR / "outputs" / "final_recommendations.csv"
)

model_data = pd.read_csv(
    BASE_DIR / "data" / "model_ready" / "model_ready_data.csv"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("Filters")

selected_product = st.sidebar.selectbox(
    "Select Product",
    sorted(recommendations["Product"].unique())
)

# -----------------------------
# EXECUTIVE SUMMARY
# -----------------------------
st.header("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Products",
    recommendations["Product"].nunique()
)

col2.metric(
    "Total Orders",
    model_data["Order ID"].nunique()
)

col3.metric(
    "Total Sales",
    f"${model_data['Sales'].sum():,.0f}"
)

col4.metric(
    "Average Improvement %",
    f"{recommendations['Improvement_%'].mean():.2f}%"
)

st.divider()

# -----------------------------
# FACTORY OPTIMIZATION SIMULATOR
# -----------------------------
st.header("🏭 Factory Optimization Simulator")

product_data = recommendations[
    recommendations["Product"] == selected_product
]

st.dataframe(product_data)

if len(product_data) > 0:

    row = product_data.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Current Factory",
        row["Current_Factory"]
    )

    col2.metric(
        "Recommended Factory",
        row["Recommended_Factory"]
    )

    col3.metric(
        "Improvement %",
        f"{row['Improvement_%']:.2f}%"
    )

st.divider()

# -----------------------------
# RECOMMENDATION DASHBOARD
# -----------------------------
st.header("✅ Top Recommendations")

st.dataframe(
    recommendations.sort_values(
        "Improvement_%",
        ascending=False
    ),
    use_container_width=True
)

st.divider()

# -----------------------------
# TOP IMPROVEMENTS CHART
# -----------------------------
st.header("📈 Improvement Analysis")

top10 = recommendations.sort_values(
    "Improvement_%",
    ascending=False
).head(10)

fig = px.bar(
    top10,
    x="Product",
    y="Improvement_%",
    title="Top Product Reallocation Opportunities"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# FACTORY DISTRIBUTION
# -----------------------------
st.header("🏭 Recommended Factory Distribution")

factory_count = (
    recommendations["Recommended_Factory"]
    .value_counts()
    .reset_index()
)

factory_count.columns = [
    "Factory",
    "Count"
]

fig2 = px.pie(
    factory_count,
    names="Factory",
    values="Count",
    title="Factory Recommendation Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------
# RISK PANEL
# -----------------------------
st.header("⚠️ Risk & Impact Panel")

high_risk = recommendations[
    recommendations["Improvement_%"] < 5
]

st.write(
    "Products with low improvement potential:"
)

st.dataframe(
    high_risk,
    use_container_width=True
)

st.success(
    "Dashboard Loaded Successfully"
)
