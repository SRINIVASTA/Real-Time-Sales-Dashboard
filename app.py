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
st.title("📈 Real-Time Sales Dashboard")

# Create a placeholder for the entire dashboard
placeholder = st.empty()

# --- REAL-TIME UPDATE LOOP ---
while True:
    new_sale_df = pd.DataFrame([generate_sales_data()])
    st.session_state.sales_data = pd.concat([st.session_state.sales_data, new_sale_df], ignore_index=True)
    st.session_state.sales_data = st.session_state.sales_data.tail(500)

    with placeholder.container():
        # --- KEY METRICS & DEBUGGING ---
        df = st.session_state.sales_data
        top_product = "N/A" # Default value

        # --- START OF DEBUGGING SECTION ---
        st.markdown("---")
        st.subheader("🕵️‍♂️ Debugging Information")
        try:
            # This block will try to calculate the top product
            if not df.empty:
                top_product_calculation = df.groupby('product')['revenue'].sum()
                st.write("Product Revenue Calculation (first 5):")
                st.write(top_product_calculation.head())
                top_product = top_product_calculation.idxmax()
                st.success(f"✅ Successfully calculated Top Product: **{top_product}**")
            else:
                st.warning("DataFrame is empty. 'Top Product' is 'N/A'.")

        except Exception as e:
            # If any error occurs during calculation, it will be displayed here
            st.error(f"An error occurred while calculating Top Product: {e}")
            top_product = "Error"
        st.markdown("---")
        # --- END OF DEBUGGING SECTION ---


        # Create 3 columns for the KPIs
        kpi1, kpi2, kpi3 = st.columns(3)

        # Display the KPIs
        kpi1.metric(
            label="Total Sales (Units) 📦",
            value=f"{df['quantity'].sum()}",
        )
        kpi2.metric(
            label="Total Revenue 💵",
            value=f"${df['revenue'].sum():,.2f}",
        )
        # This now uses the 'top_product' variable that we debugged above
        kpi3.metric(
            label="Top Performing Product 🔥",
            value=top_product,
        )
        
        st.markdown("---")

        # --- VISUALIZATIONS ---
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.subheader("Revenue Over Time")
            # Visualization code...
        with fig_col2:
            st.subheader("Product Performance")
            # Visualization code...

    # Update frequency
    time.sleep(5) # Increased sleep time to make reading debug info easier
