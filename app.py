import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Real-Time Sales Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- DATA SIMULATION ---
# Function to generate a new sales record with more realistic product names
def generate_sales_data():
    products = {
        "Quantum Laptop": 1499.99,
        "Nebula Smartphone": 799.99,
        "Galaxy Tablet": 675.75,
        "Fusion Smartwatch": 299.00,
        "Vortex VR Headset": 399.99,
        "Sonic Earbuds": 149.99,
        "Starlight Camera": 999.50
    }
    product_name = np.random.choice(list(products.keys()))
    price = products[product_name]
    quantity = np.random.randint(1, 4)
    revenue = price * quantity
    timestamp = pd.to_datetime('now')
    return {"product": product_name, "quantity": quantity, "revenue": revenue, "timestamp": timestamp}

# --- INITIALIZE SESSION STATE ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = pd.DataFrame(columns=["product", "quantity", "revenue", "timestamp"])

# --- DASHBOARD LAYOUT ---
st.title("📈 Real-Time Sales Dashboard")

# Create a placeholder for the entire dashboard
placeholder = st.empty()

# --- REAL-TIME UPDATE LOOP ---
while True:
    # Generate new data
    new_sale = generate_sales_data()
    new_sale_df = pd.DataFrame([new_sale])

    # Append new data and keep only the last 500 records for performance
    st.session_state.sales_data = pd.concat([st.session_state.sales_data, new_sale_df], ignore_index=True)
    st.session_state.sales_data = st.session_state.sales_data.tail(500)

    # Use the placeholder to draw the dashboard
    with placeholder.container():
        # --- KEY METRICS ---
        df = st.session_state.sales_data
        total_revenue = df['revenue'].sum()
        total_sales_units = df['quantity'].sum()
        
        # Calculate top performing product by revenue
        if not df.empty:
            top_product = df.groupby('product')['revenue'].sum().idxmax()
        else:
            top_product = "N/A"

        # Display KPIs in a 3-column layout
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(
            label="Total Revenue 💵",
            value=f"${total_revenue:,.2f}",
        )
        kpi2.metric(
            label="Total Sales (Units) 📦",
            value=f"{total_sales_units}",
        )
        kpi3.metric(
            label="Top Performing Product 🔥",
            value=top_product,
        )

        st.markdown("---") # Visual separator

        # --- VISUALIZATIONS ---
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.subheader("Revenue Over Time")
            # Create a cumulative revenue column for the line chart
            df['cumulative_revenue'] = df['revenue'].cumsum()
            fig_revenue = px.line(
                df,
                x='timestamp',
                y='cumulative_revenue',
                labels={"cumulative_revenue": "Cumulative Revenue", "timestamp": "Time"},
                title="Real-time Cumulative Revenue Stream"
            )
            fig_revenue.update_layout(height=400)
            st.plotly_chart(fig_revenue, use_container_width=True)

        with fig_col2:
            st.subheader("Product Performance (Top 5 by Revenue)")
            # Group by product, sum revenue, and get the top 5
            product_performance = df.groupby('product')['revenue'].sum().nlargest(5).reset_index()
            fig_product = px.bar(
                product_performance,
                y='product',
                x='revenue',
                orientation='h',
                labels={"revenue": "Total Revenue", "product": "Product"},
                title="Top 5 Products by Revenue",
                text='revenue'
            )
            fig_product.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
            fig_product.update_layout(height=400)
            st.plotly_chart(fig_product, use_container_width=True)
            
        st.markdown("---")

        # --- RECENT SALES (CUSTOM LIST) ---
        st.subheader("Recent Sales")
        recent_sales = df.sort_values(by="timestamp", ascending=False).head(7)
        
        for index, sale in recent_sales.iterrows():
            col1, col2, col3 = st.columns([2,1,1])
            with col1:
                st.markdown(f"**{sale['product']}**")
                st.markdown(f"<span style='color:grey'>Qty: {sale['quantity']}</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**${sale['revenue']:,.2f}**")
            with col3:
                 st.markdown(f"<span style='color:grey'>{sale['timestamp'].strftime('%r')}</span>", unsafe_allow_html=True)
            st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)


    # Set the update frequency
    time.sleep(2)
