import streamlit as st
import pandas as pd
import numpy as np
import time

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
        # Step 1: Group by product and sum their revenue.
        revenue_by_product = df.groupby('product')['revenue'].sum()
        # Step 2: Use idxmax() to get the NAME of the product with the highest revenue.
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

# This metric displays the correct product name calculated above.
kpi3.metric(label="Top Performing Product 🔥", value=top_product)

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

# === THIS IS THE FIX ===
# Replace the old, deprecated command with the current one.
st.rerun()
# ======================
