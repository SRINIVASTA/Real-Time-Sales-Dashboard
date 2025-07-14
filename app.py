import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Real-Time Sales Dashboard",
    page_icon="✅",
    layout="wide"
)

# --- Data Simulation ---
# Function to generate a new sales record
def generate_sales_data():
    products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor']
    prices = [1200, 25, 75, 300]
    product = np.random.choice(products)
    price = prices[products.index(product)]
    quantity = np.random.randint(1, 6)
    revenue = price * quantity
    return {"product": product, "quantity": quantity, "revenue": revenue, "timestamp": pd.to_datetime('now')}

# --- Initialize Session State for Data Storage ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = pd.DataFrame(columns=["product", "quantity", "revenue", "timestamp"])

# --- Dashboard Title ---
st.title("Real-Time Sales Dashboard")

# --- Placeholders for Metrics and Charts ---
placeholder = st.empty()

# --- Real-Time Update Loop ---
while True:
    # Generate new data
    new_sale = generate_sales_data()
    new_sale_df = pd.DataFrame([new_sale])

    # Append new data to the session state DataFrame
    st.session_state.sales_data = pd.concat([st.session_state.sales_data, new_sale_df], ignore_index=True)

    with placeholder.container():
        # --- Key Metrics ---
        total_sales = st.session_state.sales_data['quantity'].sum()
        total_revenue = st.session_state.sales_data['revenue'].sum()

        kpi1, kpi2 = st.columns(2)
        kpi1.metric(label="Total Sales (Units)", value=f"{total_sales}")
        kpi2.metric(label="Total Revenue ($)", value=f"${total_revenue:,.2f}")

        # --- Visualizations ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Revenue Over Time")
            # Resample data for a cleaner time-series chart
            revenue_over_time = st.session_state.sales_data.set_index('timestamp').resample('s')['revenue'].sum().reset_index()
            fig_revenue = px.line(revenue_over_time, x='timestamp', y='revenue', title='Real-time Revenue Stream')
            st.plotly_chart(fig_revenue, use_container_width=True)

        with col2:
            st.subheader("Product Performance")
            product_performance = st.session_state.sales_data.groupby('product')['quantity'].sum().reset_index()
            fig_product = px.bar(product_performance, x='product', y='quantity', title='Sales by Product')
            st.plotly_chart(fig_product, use_container_width=True)

        st.subheader("Raw Sales Data")
        st.dataframe(st.session_state.sales_data.sort_values(by="timestamp", ascending=False))

    time.sleep(1)
