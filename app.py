import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Live Sales Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- 2. DATA SIMULATION ---
# This function creates a single, random sales record.
def generate_sales_data():
    products = {
        "Quantum Laptop": 1499.99, "Nebula Smartphone": 799.99, "Galaxy Tablet": 675.75,
        "Fusion Smartwatch": 299.00, "Vortex VR Headset": 399.99, "Sonic Earbuds": 149.99
    }
    product_name = np.random.choice(list(products.keys()))
    quantity = np.random.randint(1, 4)
    return {
        "product": product_name,
        "quantity": quantity,
        "revenue": products[product_name] * quantity,
        "timestamp": pd.to_datetime('now')
    }

# --- 3. INITIALIZE SESSION STATE ---
# This creates our sales DataFrame the first time the app runs.
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = pd.DataFrame(columns=["product", "quantity", "revenue", "timestamp"])

# --- 4. ADD NEW DATA ---
# A new row is added to the DataFrame on every script rerun.
new_sale = generate_sales_data()
st.session_state.sales_data = pd.concat(
    [st.session_state.sales_data, pd.DataFrame([new_sale])],
    ignore_index=True
)
st.session_state.sales_data = st.session_state.sales_data.tail(500) # Keep last 500 records

# --- 5. CALCULATIONS ---
# All metrics are recalculated every time the script reruns.
df = st.session_state.sales_data
total_sales_units = df['quantity'].sum()
total_revenue = df['revenue'].sum()

# === LOGIC FOR "TOP PERFORMING PRODUCT" ===
try:
    if not df.empty:
        revenue_by_product = df.groupby('product')['revenue'].sum()
        top_product = revenue_by_product.idxmax()
    else:
        top_product = "N/A"
except Exception:
    top_product = "Calculating..."
# =============================================================

# --- 6. DISPLAY DASHBOARD UI ---
st.title("📈 Real-Time Sales Dashboard")

# Create 3 columns for our KPIs.
kpi1, kpi2, kpi3 = st.columns(3)

# Fill each KPI with its value.
kpi1.metric(label="Total Sales (Units) 📦", value=int(total_sales_units))
kpi2.metric(label="Total Revenue 💵", value=f"${total_revenue:,.2f}")
kpi3.metric(label="Top Performing Product 🔥", value=top_product)

st.markdown("---")

# === GRAPH SECTION ===
st.subheader("Visualizations")
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    # REVENUE OVER TIME (LINE CHART)
    st.markdown("##### Revenue Over Time")
    # Create a copy to add a cumulative sum column for visualization
    df_viz = df.copy()
    df_viz['cumulative_revenue'] = df_viz['revenue'].cumsum()
    fig = px.line(
        df_viz,
        x="timestamp",
        y="cumulative_revenue",
        labels={"cumulative_revenue": "Cumulative Revenue"}
    )
    st.plotly_chart(fig, use_container_width=True)

with fig_col2:
    # PRODUCT PERFORMANCE (BAR CHART)
    st.markdown("##### Product Performance (Top 5)")
    product_performance = df.groupby('product')['revenue'].sum().nlargest(5).reset_index()
    fig2 = px.bar(
        product_performance,
        x="revenue",
        y="product",
        orientation="h",
        labels={"revenue": "Total Revenue", "product": "Product"}
    )
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)
# ======================

st.markdown("---")

# Display a table of the most recent sales data.
st.subheader("Recent Sales Activity")
st.dataframe(
    df.sort_values(by="timestamp", ascending=False),
    use_container_width=True,
    hide_index=True,
    column_config={
        "product": "Product",
        "quantity": "Qty",
        "revenue": st.column_config.NumberColumn(format="$%.2f"),
        "timestamp": st.column_config.DatetimeColumn("Time", format="hh:mm:ss A")
    }
)

# --- 7. AUTO-REFRESH SCRIPT ---
time.sleep(2)
st.rerun()
