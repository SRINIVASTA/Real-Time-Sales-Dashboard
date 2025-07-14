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
def generate_sales_data():
    products = {
        "Quantum Laptop": 1499.99, "Nebula Smartphone": 799.99, "Galaxy Tablet": 675.75,
        "Fusion Smartwatch": 299.00, "Vortex VR Headset": 399.99, "Sonic Earbuds": 149.99,
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
# Custom CSS for the blinking "Live" indicator
st.markdown("""
<style>
.blinking-dot {
    height: 10px; width: 10px; background-color: #00ff00; border-radius: 50%;
    display: inline-block; animation: blinking 1s infinite; margin-right: 5px;
}
@keyframes blinking { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

st.title("📈 Real-Time Sales Dashboard")
st.markdown('<h3><span class="blinking-dot"></span>Live</h3>', unsafe_allow_html=True)

# Create a placeholder for the entire dashboard
placeholder = st.empty()

# --- REAL-TIME UPDATE LOOP ---
while True:
    new_sale_df = pd.DataFrame([generate_sales_data()])
    st.session_state.sales_data = pd.concat([st.session_state.sales_data, new_sale_df], ignore_index=True)
    st.session_state.sales_data = st.session_state.sales_data.tail(500)

    with placeholder.container():
        # --- KEY METRICS ---
        df = st.session_state.sales_data

        # 1. CALCULATE TOP PERFORMING PRODUCT
        if not df.empty:
            # Group by product and sum the revenue to find the product with the highest total revenue
            top_product = df.groupby('product')['revenue'].sum().idxmax()
        else:
            top_product = "N/A"

        # 2. CREATE 3 COLUMNS FOR THE KPIs
        kpi1, kpi2, kpi3 = st.columns(3)

        # 3. DISPLAY THE KPIs IN THE CORRECT ORDER
        kpi1.metric(
            label="Total Sales (Units) 📦",
            value=f"{df['quantity'].sum()}",
        )
        kpi2.metric(
            label="Total Revenue 💵",
            value=f"${df['revenue'].sum():,.2f}",
        )
        # The Top Performing Product metric is now correctly placed and calculated
        kpi3.metric(
            label="Top Performing Product 🔥",
            value=top_product, # This value is calculated above
        )
        
        st.markdown("---")

        # --- VISUALIZATIONS ---
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.subheader("Revenue Over Time")
            df_viz = df.copy() # Use a copy for visualization-specific columns
            df_viz['cumulative_revenue'] = df_viz['revenue'].cumsum()
            fig_revenue = px.line(
                df_viz, x='timestamp', y='cumulative_revenue',
                labels={"cumulative_revenue": "Cumulative Revenue", "timestamp": "Time"},
                title="Real-time Cumulative Revenue Stream"
            )
            st.plotly_chart(fig_revenue, use_container_width=True)

        with fig_col2:
            st.subheader("Product Performance (Top 5 by Revenue)")
            product_performance = df.groupby('product')['revenue'].sum().nlargest(5).reset_index()
            fig_product = px.bar(
                product_performance, y='product', x='revenue', orientation='h',
                labels={"revenue": "Total Revenue", "product": "Product"},
                title="Top 5 Products by Revenue", text='revenue'
            )
            fig_product.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
            fig_product.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_product, use_container_width=True)
            
        st.markdown("---")

        # --- RECENT SALES LIST ---
        st.subheader("Recent Sales")
        for index, sale in df.sort_values(by="timestamp", ascending=False).head(7).iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])
            col1.markdown(f"**{sale['product']}**<br><span style='color:grey'>Qty: {sale['quantity']}</span>", unsafe_allow_html=True)
            col2.markdown(f"**${sale['revenue']:,.2f}**")
            col3.markdown(f"<span style='color:grey'>{sale['timestamp'].strftime('%r')}</span>", unsafe_allow_html=True)
            st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

    # Update frequency
    time.sleep(2)
