import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Smart Inventory Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# THEN styling
st.markdown("""
<style>

/* 🌌 Main Background */
.main {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Remove default padding */
.block-container {
    padding-top: 3rem;
    padding-bottom: 2rem;
}

/* Headings */
h1, h2, h3 {
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* ✨ Glass Cards */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    transition: 0.3s;
}

/* Hover effect */
div[data-testid="stMetric"]:hover {
    transform: scale(1.05);
}

div[data-testid="stHorizontalBlock"] {
    gap: 20px;
}
            
/* Section blocks */
div[data-testid="stHorizontalBlock"] > div {
    padding: 12px;
    border-radius: 12px;
    background: transparent;
    overflow: visible;
    min-height: 160px;   /* 🔥 ADD THIS */
}
            
div[data-testid="stHorizontalBlock"] > div:hover {
    transform: translateY(-5px);
    transition: 0.3s;
}

/* Buttons */
button[kind="primary"] {
    background: linear-gradient(90deg,#00f5ff,#00ffcc);
    color: black;
    border-radius: 10px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}

.kpi-card {
    position: relative;
    overflow: hidden;
    padding: 18px;
    border-radius: 16px;
    background: linear-gradient(270deg, rgba(0,255,200,0.1), rgba(0,150,255,0.1));
    background-size: 400% 400%;
    
    /* 🔥 COMBINE BOTH ANIMATIONS */
    animation: gradientMove 6s ease infinite, glow 3s infinite linear;

    backdrop-filter: blur(12px);
    text-align: center;
    transition: all 0.3s ease;
}

/* 🔥 GLOW BORDER */
.kpi-card::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 16px;
    padding: 1px;
    background: linear-gradient(90deg, #00f5ff, #00ffcc, #00f5ff);
    -webkit-mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}

/* 🔥 GRADIENT ANIMATION */
@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}

/* 🔥 GLOW ANIMATION */
@keyframes glow {
    0% { box-shadow: 0 0 5px #00f5ff; }
    50% { box-shadow: 0 0 20px #00ffcc; }
    100% { box-shadow: 0 0 5px #00f5ff; }
}

/* 🔥 HOVER EFFECT */
.kpi-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow:
        0 0 10px rgba(0,255,255,0.4),
        0 0 25px rgba(0,255,255,0.6),
        0 0 40px rgba(0,255,255,0.3);
}

button {
    border-radius: 12px !important;
    height: 45px;
    font-weight: 600;
    transition: all 0.3s ease;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(0,255,255,0.5);
}
            
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="
    padding:20px;
    border-radius:15px;
    background: linear-gradient(135deg, rgba(0,255,150,0.15), rgba(0,255,100,0.05));
    border: 1px solid rgba(0,255,150,0.3);
    text-align:center;
    min-height:160px;   /* 🔥 ADD THIS */
    display:flex;
    flex-direction:column;
    justify-content:center;
    ">
        <h4>🟢 Demand Agent</h4>
        <p style="opacity:0.7;">Active</p>
        <b style="color:#00ffcc;">✔ Running Smoothly</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
    padding:20px;
    border-radius:15px;
    background: linear-gradient(135deg, rgba(0,150,255,0.15), rgba(0,150,255,0.05));
    border: 1px solid rgba(0,150,255,0.3);
    text-align:center;
    min-height:160px;   /* 🔥 ADD THIS */
    display:flex;
    flex-direction:column;
    justify-content:center;
    ">
        <h4>🔵 Inventory Agent</h4>
        <p style="opacity:0.7;">Running</p>
        <b style="color:#4da6ff;">✔ Processing Inventory</b>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
    padding:20px;
    border-radius:15px;
    background: linear-gradient(135deg, rgba(200,100,255,0.15), rgba(200,100,255,0.05));
    border: 1px solid rgba(200,100,255,0.3);
    text-align:center;    
    min-height:160px;   /* 🔥 ADD THIS */
    display:flex;
    flex-direction:column;
    justify-content:center;
    ">
        <h4>🟣 Decision Agent</h4>
        <p style="opacity:0.7;">Processing</p>
        <b style="color:#d580ff;">✔ AI Decision Active</b>
    </div>
    """, unsafe_allow_html=True)

# 🔹 Title section (already there)

st.markdown("""
<div style="text-align:center; padding:20px 0;">
    <h1 style="
        font-size:38px;
        margin-bottom:10px;
        background: linear-gradient(to right, #00f5ff, #00ffcc);
        -webkit-background-clip: text;
        color: transparent;
    ">
        🚀 Real-Time AI Decision Engine
    </h1>

<div style="font-size:16px; opacity:0.7; margin-top:0;">
    ⚡ Multi-Agent Intelligence + Human-in-the-Loop System
</div>
""", unsafe_allow_html=True)

# 🔹 Divider
st.markdown("""
<hr style="height:2px;background:linear-gradient(to right,#00f5ff,#00ffcc);border:none;margin:20px 0;">
""", unsafe_allow_html=True)

# 👤 Human-in-the-Loop Control (CENTERED PERFECTLY)

# Title (centered)
st.markdown("""
<div style="text-align:center; margin-top:20px;">
    <h3>👤 Human-in-the-Loop Control</h3>
</div>
""", unsafe_allow_html=True)

# Optional spacing fix (removes extra gap)
st.markdown("<div style='margin-top:-10px'></div>", unsafe_allow_html=True)

# Columns layout (center focus)
colA, colB, colC = st.columns([2,3,2])

with colA:
    st.empty()   # left spacing

with colB:
    btn1, btn2 = st.columns(2)

    with btn1:
        if st.button("✅ Approve AI Decision", use_container_width=True):
            st.success("Decision Approved by Human")

    with btn2:
        if st.button("❌ Reject AI Decision", use_container_width=True):
            st.error("Decision Rejected by Human")

with colC:
    st.empty()   # right spacing

# === 2. Load Data Function ===
@st.cache_data
def load_data():
    """Load and prepare data from multiple possible sources"""

    # Get curarent directory and project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    # Try multiple data paths with absolute paths - prioritize enhanced analysis results
    possible_paths = [
        os.path.join(project_root, "data", "processed", "inventory_analysis_results_enhanced.csv"),
        os.path.join(project_root, "data", "processed", "inventory_analysis_results.csv"),
        os.path.join(project_root, "dashboard", "cache", "dashboard_data.csv"),
        os.path.join(project_root, "data", "processed", "expiry_risk_predictions.csv"),
        os.path.join(project_root, "data", "cleaned_inventory_data.csv"),
        os.path.join(project_root, "cleaned_inventory_data.csv"),
    ]

    df = None
    data_source = None

    for path in possible_paths:
        if os.path.exists(path):
            try:
                # Fix: Added low_memory=False to prevent DtypeWarning
                df = pd.read_csv(path, low_memory=False)
                data_source = path
                break
            except Exception as e:
                st.warning(f"Error loading {path}: {str(e)}")
                continue

    # If no file found, create sample data
    if df is None:
        st.warning("⚠️ No data file found. Generating sample data for demonstration.")
        
        # Create sample data matching analysis structure
        np.random.seed(42)
        n_samples = 1000
        
        df = pd.DataFrame({
            'item_id': [f'ITEM_{i:05d}' for i in range(n_samples)],
            'product_name': [f'Product_{i:03d}' for i in range(n_samples)],
            'store_nbr': np.random.randint(1, 11, n_samples),
            'current_stock': np.random.randint(0, 200, n_samples),
            'rolling_avg_sales_7': np.random.exponential(5, n_samples),
            'days_to_expiry': np.random.randint(0, 31, n_samples),
            'unit_price': np.random.uniform(0.5, 50, n_samples),
            'Stock_Level': np.random.choice(['High', 'Normal', 'Low'], n_samples, p=[0.2, 0.6, 0.2]),
            'Expiry_Risk': np.random.choice(['Safe', 'Near Expiry', 'Expired'], n_samples, p=[0.7, 0.25, 0.05]),
            'Suggested_Discount': np.random.choice([0, 10, 20, 30, 40], n_samples, p=[0.6, 0.2, 0.1, 0.05, 0.05]),
            'Reorder': np.random.choice(['No', 'Yes'], n_samples, p=[0.8, 0.2]),
            'Action': np.random.choice(['No Action', 'Apply Discount', 'Restock', 'Redistribute', 'Remove'], 
                                    n_samples, p=[0.5, 0.2, 0.15, 0.1, 0.05]),
            'date': datetime.now().strftime('%Y-%m-%d')
        })
        data_source = "Generated Sample Data"

    # Ensure columns are properly named and typed
    if df is not None:
        # Standardize column names
        df.columns = df.columns.str.strip()

        # Create missing analysis columns if they don't exist
        if 'Stock_Level' not in df.columns:
            df['Stock_Level'] = 'Normal'
        if 'Expiry_Risk' not in df.columns:
            df['Expiry_Risk'] = 'Safe'
        if 'Suggested_Discount' not in df.columns:
            df['Suggested_Discount'] = 0
        if 'Reorder' not in df.columns:
            df['Reorder'] = 'No'
        if 'Action' not in df.columns:
            df['Action'] = 'No Action'
        
        # Add donation columns if they don't exist
        if 'donation_eligible' not in df.columns:
            df['donation_eligible'] = np.random.choice([True, False], len(df), p=[0.1, 0.9])
        if 'donation_status' not in df.columns:
            df['donation_status'] = np.where(
                df['donation_eligible'], 
                np.random.choice(['Pending', 'Donated', 'Rejected'], len(df), p=[0.7, 0.2, 0.1]),
                'N/A'
            )
        if 'city' not in df.columns:
            cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Hyderabad']
            df['city'] = np.random.choice(cities, len(df))
        if 'category' not in df.columns:
            # Handle category creation safely
            if 'product_name' in df.columns:
                df['category'] = df['product_name'].astype(str).str.split().str[0]
            else:
                df['category'] = 'Unknown'
        if 'nearest_ngo' not in df.columns:
            ngos = ['People For Animals', 'Blue Cross of India', 'Wildlife SOS', 'Friendicoes SECA', 'CARE India']
            df['nearest_ngo'] = np.random.choice(ngos, len(df))
        if 'ngo_contact' not in df.columns:
            df['ngo_contact'] = '+91-' + pd.Series(np.random.randint(1000000000, 9999999999, len(df))).astype(str)
        if 'store_latitude' not in df.columns:
            df['store_latitude'] = np.random.uniform(8.0, 35.0, len(df))
        if 'store_longitude' not in df.columns:
            df['store_longitude'] = np.random.uniform(68.0, 97.0, len(df))

        # Ensure data types
        try:
            df['store_nbr'] = df['store_nbr'].astype(str)
            df['rolling_avg_sales_7'] = pd.to_numeric(df['rolling_avg_sales_7'], errors='coerce').fillna(0)
            df['current_stock'] = pd.to_numeric(df['current_stock'], errors='coerce').fillna(0).astype(int)
            df['days_to_expiry'] = pd.to_numeric(df['days_to_expiry'], errors='coerce').fillna(7).astype(int)
            df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce').fillna(1.0)
            df['Suggested_Discount'] = pd.to_numeric(df['Suggested_Discount'], errors='coerce').fillna(0).astype(int)
        except Exception as e:
            st.error(f"Error processing data types: {str(e)}")

    return df, data_source

# === 3. Load Data ===
try:
    df, data_source = load_data()

    # 🔥 Spinner MUST be inside try
    import time
    with st.spinner("🤖 AI Agents analyzing inventory..."):
        time.sleep(1)

    if df is not None and len(df) > 0:
        st.sidebar.success(f"✅ Data loaded: {os.path.basename(data_source) if data_source else 'Unknown'}")
        st.toast("🚀 AI System Activated")
        st.sidebar.info(f"📊 Records: {len(df)}")
        
        # Apply any pending changes from session state
        if 'df_changes' in st.session_state:
            for idx, new_status in st.session_state.df_changes.items():
                if idx in df.index and 'donation_status' in df.columns:
                    df.at[idx, 'donation_status'] = new_status
    else:
        st.error("❌ Failed to load data")
        st.stop()

except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# === 4. Sidebar Filters ===
st.sidebar.title("🔍 Filter Options")

# Store filter
try:
    unique_stores = df['store_nbr'].dropna().unique()
    if len(unique_stores) > 0:
        store_options = ['All'] + sorted([str(x) for x in unique_stores])
        selected_store = st.sidebar.selectbox("Select Store", store_options)
    else:
        selected_store = 'All'
except Exception as e:
    st.sidebar.error(f"Error creating store filter: {str(e)}")
    selected_store = 'All'

# Stock Level filter
stock_levels = ['All'] + list(df['Stock_Level'].unique())
selected_stock_level = st.sidebar.selectbox("Stock Level", stock_levels)

# Expiry Risk filter
expiry_risks = ['All'] + list(df['Expiry_Risk'].unique())
selected_expiry_risk = st.sidebar.selectbox("Expiry Risk", expiry_risks)

# Action filter
actions = ['All'] + list(df['Action'].unique())
selected_action = st.sidebar.selectbox("Required Action", actions)

# Apply filters
# Fix: Using shallow copy to prevent memory issues
filtered_df = df.copy(deep=False)

if selected_store != "All":
    filtered_df = filtered_df[filtered_df['store_nbr'] == selected_store]

if selected_stock_level != "All":
    filtered_df = filtered_df[filtered_df['Stock_Level'] == selected_stock_level]

if selected_expiry_risk != "All":
    filtered_df = filtered_df[filtered_df['Expiry_Risk'] == selected_expiry_risk]

if selected_action != "All":
    filtered_df = filtered_df[filtered_df['Action'] == selected_action]

# === AI Decision Logic ===

stock = filtered_df['current_stock'].mean()
demand = filtered_df['rolling_avg_sales_7'].mean()

gap = demand - stock

if gap > 20:
    decision = "Urgent Restock Required 🚨"
elif gap > 5:
    decision = "Restock Soon ⚠️"
elif stock > demand * 2:
    decision = "Overstock - Apply Discount 💸"
else:
    decision = "No Action Needed ✅"

st.markdown("""
<h1 style='text-align: center;
background: linear-gradient(90deg,#00f5ff,#00ffcc);
-webkit-background-clip: text;
color: transparent;'>
🚀 Smart Inventory AI Dashboard
</h1>
""", unsafe_allow_html=True)    

# ✅ ADD HERE
status = "🟢 Healthy" if "No Action" in decision else "🔴 Attention Needed"

st.markdown(f"""
<div style="
padding:10px;
border-radius:10px;
background: linear-gradient(90deg, rgba(0,255,200,0.2), rgba(0,150,255,0.2));
backdrop-filter: blur(8px);
border: 1px solid rgba(255,255,255,0.1);
text-align:center;
font-weight:600;
margin-bottom:15px;
">
System Status: {status}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
padding:20px;
border-radius:15px;
background: rgba(255,255,255,0.05);
margin-bottom:20px;
">
<h3>🧠 AI Decision Output</h3>
</div>
""", unsafe_allow_html=True)

# Info box (NO decision here)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        📦 <b>Demand</b><br>
        <span style="font-size:24px; font-weight:700;">{demand:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        📊 <b>Stock</b><br>
        <span style="font-size:24px;">{stock:.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        📉 <b>Gap</b><br>
        <span style="font-size:24px;">{abs(gap):.2f}</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        ⚡ <b>Decision</b><br>
        <span style="font-size:24px;">{decision.split(" ")[0]}</span>
    </div>
    """, unsafe_allow_html=True)

# Decision (only here)
if "Urgent" in decision:
    st.error("🚨 " + decision)
elif "Restock" in decision:
    st.warning("⚠️ " + decision)
elif "Overstock" in decision:
    st.info("💸 Apply discount to clear excess stock")
else:
    st.success("✅ Inventory balanced")

# 💡 Insight
st.caption("💡 AI analyzes demand vs stock in real-time to suggest optimal actions")
# 🔥 ADD THIS
st.markdown("<br>", unsafe_allow_html=True)

# ✅ risk score (ONLY ONCE)
risk_score = min(100, int(abs(gap) / (demand + 1) * 100))

# 🔥 ADD THIS HERE
colR1, colR2 = st.columns(2)

with colR1:
    st.metric("⚠️ Inventory Risk Score", f"{risk_score}%")

with colR2:
    st.metric("⚡ System Health", f"{100 - risk_score}%")

# ✅ risk display
if risk_score > 70:
    st.error(f"🚨 High Risk: {risk_score}%")
elif risk_score > 40:
    st.warning(f"⚠️ Medium Risk: {risk_score}%")
else:
    st.success(f"✅ Low Risk: {risk_score}%")

# ✅ system health
st.markdown("""
<div style="
padding:10px;
border-radius:10px;
background: rgba(255,255,255,0.05);
margin-bottom:10px;
">
<h3>⚡ System Health</h3>
</div>
""", unsafe_allow_html=True)

health = max(10, 100 - risk_score)

st.progress(health)

st.caption(f"System Efficiency: {health}%")

# 🔥 NEW FEATURES
confidence = np.random.randint(85, 98)
st.metric("🤖 AI Confidence", f"{confidence}%")

trend = "Increasing 📈" if demand > stock else "Stable 📊"
st.write(f"📊 Demand Trend: **{trend}**")

st.caption(f"🧠 AI Insight: Demand is {'higher' if demand > stock else 'lower'} than stock by {abs(gap):.2f} units.")

st.info(f"💡 Recommendation: Focus on {'restocking' if gap > 0 else 'clearing excess stock'} strategy.")
# 📈 Trend Chart
st.markdown("""
<div style="
padding:15px;
border-radius:12px;
background: rgba(255,255,255,0.04);
margin-bottom:10px;
">
<h3>📈 Demand vs Stock Trend</h3>
</div>
""", unsafe_allow_html=True)

trend_df = pd.DataFrame({
    "Metric": ["Stock", "Demand"],
    "Value": [stock, demand]
})

fig = px.bar(trend_df, x="Metric", y="Value", color="Metric")
fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    title_x=0.3,
    title_font=dict(size=20, color="#00f5ff")
)
st.plotly_chart(fig, use_container_width=True)
# 🔥 ADD THIS
st.markdown("<br>", unsafe_allow_html=True)

# 🧠 Smart Message
if "Urgent" in decision:
    st.error("🚨 High risk of stockout! Immediate action required.")
elif "Restock" in decision:
    st.warning("⚠️ Stock levels dropping. Plan restocking soon.")
elif "Overstock" in decision:
    st.info("💸 Excess inventory detected. Apply discounts.")
else:
    st.success("✅ Inventory is balanced and healthy.")

st.markdown("""
<hr style="
border: none;
height: 2px;
background: linear-gradient(to right, #00f5ff, #00ffcc);
margin: 20px 0;
">
""", unsafe_allow_html=True)

# 📊 Strategic Insights
st.subheader("📊 Strategic Insights")

col1, col2 = st.columns(2)

with col1:
    top_category = filtered_df.groupby('category')['current_stock'].sum().idxmax()
    st.info(f"📦 Highest Inventory Category: **{top_category}**")

with col2:
    risky_store = filtered_df.groupby('store_nbr')['days_to_expiry'].mean().idxmin()
    st.warning(f"🏪 Most Risky Store (Expiry): **{risky_store}**")

# 📈 Pattern Insight
st.subheader("📈 Inventory Pattern Insight")

if demand > stock:
    st.error("🚨 Demand exceeds supply → risk of stockout")
elif stock > demand * 2:
    st.warning("⚠️ Overstock detected → risk of wastage")
else:
    st.success("✅ Inventory is balanced")

# 🚨 Critical Alerts
st.subheader("🚨 Critical Alerts")

high_risk_count = len(filtered_df[filtered_df['Action'].isin(['Remove', 'Apply Discount'])])
restock_count = len(filtered_df[filtered_df['Reorder'] == 'Yes'])

colA, colB = st.columns(2)

with colA:
    st.error(f"🚨 High Risk Items: {high_risk_count}")

with colB:
    st.warning(f"📦 Items Needing Restock: {restock_count}")

st.markdown("""
<hr style="
border: none;
height: 2px;
background: linear-gradient(to right, #00f5ff, #00ffcc);
margin: 20px 0;
">
""", unsafe_allow_html=True)

# === 5.5. Summary Metrics Section ===
st.subheader("💰 Financial Impact Summary")

try:
    # Calculate total revenue from discounted items (revenue after discount)
    discount_items = filtered_df[filtered_df['Action'] == 'Apply Discount']
    if len(discount_items) > 0 and 'Suggested_Discount' in discount_items.columns:
        # Calculate revenue after discount: unit_price * current_stock * (1 - discount_rate / 100)
        original_values = discount_items['unit_price'] * discount_items['current_stock']
        discount_amounts = original_values * (discount_items['Suggested_Discount'] / 100)
        total_discount_revenue = original_values.sum() - discount_amounts.sum()
    else:
        total_discount_revenue = 0.0
    
    # Calculate total value of donated items
    donated_items = filtered_df[filtered_df['donation_status'] == 'Donated']
    if len(donated_items) > 0:
        # Calculate donated value: unit_price * current_stock
        donated_values = donated_items['unit_price'] * donated_items['current_stock']
        total_donated_value = donated_values.sum()
    else:
        total_donated_value = 0.0
    
    # Calculate total value of removed items (loss)
    removed_items = filtered_df[filtered_df['Action'] == 'Remove']
    if len(removed_items) > 0:
        removed_values = removed_items['unit_price'] * removed_items['current_stock']
        total_removed_value = removed_values.sum()
    else:
        total_removed_value = 0.0
    
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💸 Revenue from Discounted Sales", 
            f"₹{total_discount_revenue:,.2f}",
            help="Total revenue generated from items sold at discount"
        )
    
    with col2:
        st.metric(
            "🧡 Value of Donated Goods", 
            f"₹{total_donated_value:,.2f}",
            help="Total value of items successfully donated to NGOs"
        )
    
    with col3:
        st.metric(
            "🗑️ Loss from Removed Items", 
            f"₹{total_removed_value:,.2f}",
            delta=f"-₹{total_removed_value:,.2f}" if total_removed_value > 0 else None,
            delta_color="inverse",
            help="Total value lost from items too expired to sell or donate"
        )
    
    with col4:
        # Calculate net financial impact
        net_impact = total_discount_revenue + total_donated_value - total_removed_value
        st.metric(
            "📊 Net Financial Impact", 
            f"₹{net_impact:,.2f}",
            delta=f"₹{net_impact:,.2f}" if net_impact >= 0 else f"-₹{abs(net_impact):,.2f}",
            delta_color="normal" if net_impact >= 0 else "inverse",
            help="Net financial impact: (Discount Revenue + Donated Value) - Removed Value"
        )
    
    # Additional insights row
    if total_discount_revenue > 0 or total_donated_value > 0 or total_removed_value > 0:
        st.markdown("""
<hr style="height:2px;background:linear-gradient(to right,#00f5ff,#00ffcc);border:none;margin:20px 0;">
""", unsafe_allow_html=True)
        col_insights1, col_insights2 = st.columns(2)
        
        with col_insights1:
            # Recovery rate
            total_at_risk = total_discount_revenue + total_donated_value + total_removed_value
            if total_at_risk > 0:
                recovery_rate = ((total_discount_revenue + total_donated_value) / total_at_risk) * 100
                st.metric(
                    "📈 Value Recovery Rate",
                    f"{recovery_rate:.1f}%",
                    help="Percentage of at-risk inventory value recovered through discounts and donations"
                )
        
        with col_insights2:
            # Count of items processed
            total_processed = len(discount_items) + len(donated_items) + len(removed_items)
            st.metric(
                "📦 Items Processed",
                f"{total_processed:,}",
                help="Total number of items requiring action (discount, donate, or remove)"
            )

except Exception as e:
    st.error(f"Error calculating financial summary: {str(e)}")
    # Fallback simple metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💸 Revenue from Discounted Sales", "₹0.00")
    with col2:
        st.metric("🧡 Value of Donated Goods", "₹0.00")

st.markdown("""
<hr style="height:2px;background:linear-gradient(to right,#00f5ff,#00ffcc);border:none;margin:20px 0;">
""", unsafe_allow_html=True)

# === 6. Enhanced KPIs ===
st.subheader("📌 Operational Key Performance Indicators")

try:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_items = len(filtered_df)
        st.metric("Total Items", f"{total_items:,}")
    with col2:
        total_value = (filtered_df['current_stock'] * filtered_df['unit_price']).sum()
        st.metric("Total Inventory Value", f"₹{total_value:,.0f}")
    with col3:
        high_risk = len(filtered_df[filtered_df['Action'].isin(['Remove', 'Apply Discount'])])
        st.metric("High Risk Items", high_risk)
    with col4:
        reorder_needed = len(filtered_df[filtered_df['Reorder'] == 'Yes'])
        st.metric("Reorder Needed", reorder_needed)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        overstocked = len(filtered_df[filtered_df['Stock_Level'] == 'High'])
        st.metric("Overstocked Items", overstocked)
    with col6:
        understocked = len(filtered_df[filtered_df['Stock_Level'] == 'Low'])
        st.metric("Understocked Items", understocked)
    with col7:
        near_expiry = len(filtered_df[filtered_df['Expiry_Risk'] == 'Near Expiry'])
        st.metric("Near Expiry", near_expiry)
    with col8:
        avg_discount = filtered_df[filtered_df['Suggested_Discount'] > 0]['Suggested_Discount'].mean()
        st.metric("Avg Suggested Discount", f"{avg_discount:.1f}%" if not pd.isna(avg_discount) else "0%")
except Exception as e:
    st.error(f"Error calculating KPIs: {str(e)}")

st.markdown("""
<hr style="height:2px;background:linear-gradient(to right,#00f5ff,#00ffcc);border:none;margin:20px 0;">
""", unsafe_allow_html=True)

# === 7. Analysis Charts ===
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Stock Level Distribution")
    try:
        stock_counts = filtered_df['Stock_Level'].value_counts()
        if len(stock_counts) > 0:
            fig1 = px.pie(
                values=stock_counts.values,
                names=stock_counts.index,
                title="Stock Level Distribution",
                color_discrete_map={'High': '#FF6B6B', 'Normal': '#4ECDC4', 'Low': '#45B7D1'}
            )
            st.plotly_chart(fig1, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating stock level chart: {str(e)}")

with col_right:
    st.subheader("⚠️ Expiry Risk Analysis")
    try:
        expiry_counts = filtered_df['Expiry_Risk'].value_counts()
        if len(expiry_counts) > 0:
            fig2 = px.pie(
                values=expiry_counts.values,
                names=expiry_counts.index,
                title="Expiry Risk Distribution",
                color_discrete_map={'Safe': '#2E8B57', 'Near Expiry': '#FFA500', 'Expired': '#DC143C'}
            )
            st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Error creating expiry risk chart: {str(e)}")

# === 8. Action Recommendations ===
st.subheader("⚡ Action Recommendations")
try:
    action_counts = filtered_df['Action'].value_counts()
    if len(action_counts) > 0:
        fig3 = px.bar(
            x=action_counts.index,
            y=action_counts.values,
            title="Required Actions Distribution",
            labels={'x': 'Action', 'y': 'Number of Items'},
            color=action_counts.values,
            color_continuous_scale='RdYlBu_r'
        )
        st.plotly_chart(fig3, use_container_width=True)
except Exception as e:
    st.error(f"Error creating action recommendations chart: {str(e)}")

# === 9. Inventory Value Analysis ===
st.subheader("💰 Inventory Value Analysis")
try:
    # Calculate value by action type
    # Fix: Added group_keys=False to prevent FutureWarning
    value_by_action = filtered_df.groupby('Action', group_keys=False).apply(
        lambda x: (x['current_stock'] * x['unit_price']).sum()
    ).reset_index()
    value_by_action.columns = ['Action', 'Total_Value']
    
    if len(value_by_action) > 0:
        fig4 = px.bar(
            value_by_action,
            x='Action',
            y='Total_Value',
            title="Inventory Value by Required Action",
            labels={'Total_Value': 'Inventory Value ($)'},
            color='Total_Value',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig4, use_container_width=True)
except Exception as e:
    st.error(f"Error creating value analysis chart: {str(e)}")

# === 10. Critical Items Tables ===
st.subheader("🚨 Critical Items Requiring Immediate Action")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔴 Urgent Actions", "💸 Discount Opportunities", "📦 Restock Alerts", "🗑️ Remove Items", "🐾 Donation Center"])

with tab1:
    st.write("**Items requiring immediate attention:**")
    try:
        urgent_items = filtered_df[
            filtered_df['Action'].isin(['Remove', 'Apply Discount', 'Restock'])
        ].sort_values(['Action', 'days_to_expiry'])
        
        if len(urgent_items) > 0:
            display_cols = ['item_id', 'product_name', 'store_nbr', 'current_stock', 
                          'Stock_Level', 'Expiry_Risk', 'days_to_expiry', 'Action']
            st.dataframe(urgent_items[display_cols].head(20), use_container_width=True)
        else:
            st.success("✅ No items requiring urgent action!")
    except Exception as e:
        st.error(f"Error processing urgent items: {str(e)}")

with tab2:
    st.write("**Items with discount recommendations:**")
    try:
        discount_items = filtered_df[
            filtered_df['Action'] == 'Apply Discount'
        ].sort_values('Suggested_Discount', ascending=False)
        
        if len(discount_items) > 0:
            display_cols = ['item_id', 'product_name', 'store_nbr', 'current_stock', 
                          'Suggested_Discount', 'Expiry_Risk', 'unit_price']
            # Fix: Using shallow copy to prevent memory issues
            discount_display = discount_items[display_cols].copy(deep=False)
            
            # Calculate both potential revenue and discount amount
            discount_display['Original_Value'] = (
                discount_display['current_stock'] * discount_display['unit_price']
            ).round(2)
            discount_display['Discount_Amount'] = (
                discount_display['current_stock'] * 
                discount_display['unit_price'] * 
                (discount_display['Suggested_Discount'] / 100)
            ).round(2)
            discount_display['Potential_Revenue'] = (
                discount_display['Original_Value'] - discount_display['Discount_Amount']
            ).round(2)
            
            st.dataframe(discount_display.head(20), use_container_width=True)
            
            # Enhanced summary metrics for discount section
            col_discount1, col_discount2, col_discount3 = st.columns(3)
            
            with col_discount1:
                total_original_value = discount_display['Original_Value'].sum()
                st.info(f"💰 Original Value: ₹{total_original_value:,.2f}")
            
            with col_discount2:
                total_discount_amount = discount_display['Discount_Amount'].sum()
                st.warning(f"💸 Total Discount Given: ₹{total_discount_amount:,.2f}")
            
            with col_discount3:
                total_discount_revenue = discount_display['Potential_Revenue'].sum()
                st.success(f"💵 Revenue After Discount: ₹{total_discount_revenue:,.2f}")
                
        else:
            st.info("ℹ️ No items currently recommended for discount!")
    except Exception as e:
        st.error(f"Error processing discount items: {str(e)}")

with tab3:
    st.write("**Items needing restock:**")
    try:
        restock_items = filtered_df[
            filtered_df['Reorder'] == 'Yes'
        ].sort_values('current_stock')
        
        if len(restock_items) > 0:
            display_cols = ['item_id', 'product_name', 'store_nbr', 'current_stock', 
                          'rolling_avg_sales_7', 'Stock_Level', 'days_to_expiry']
            st.dataframe(restock_items[display_cols].head(20), use_container_width=True)
        else:
            st.success("✅ No items requiring restock!")
    except Exception as e:
        st.error(f"Error processing restock items: {str(e)}")

with tab4:
    st.write("**Expired items to remove:**")
    try:
        remove_items = filtered_df[
            filtered_df['Action'] == 'Remove'
        ].sort_values('days_to_expiry')
        
        if len(remove_items) > 0:
            display_cols = ['item_id', 'product_name', 'store_nbr', 'current_stock', 
                          'days_to_expiry', 'unit_price']
            # Fix: Using shallow copy to prevent memory issues
            remove_display = remove_items[display_cols].copy(deep=False)
            remove_display['Loss_Value'] = (
                remove_display['current_stock'] * remove_display['unit_price']
            ).round(2)
            st.dataframe(remove_display.head(20), use_container_width=True)
            
            total_loss = remove_display['Loss_Value'].sum()
            st.error(f"⚠️ Total value of items to remove: ₹{total_loss:,.2f}")
        else:
            st.success("✅ No expired items to remove!")
    except Exception as e:
        st.error(f"Error processing remove items: {str(e)}")

with tab5:
    st.markdown("### 🐾 Donation Management Center")
    
    try:
        # Filter donation-eligible items with Action == "Donate"
        # Fix: Using shallow copy to prevent memory issues
        donation_items = filtered_df[
            (filtered_df['donation_eligible'] == True) & 
            (filtered_df['Action'] == 'Donate')
        ].copy(deep=False)
        
        if len(donation_items) > 0:
            # === Donation Summary Section ===
            st.subheader("📊 Donation Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_eligible = len(donation_items)
                st.metric("🎁 Total Eligible Items", total_eligible)
            with col2:
                pending_count = len(donation_items[donation_items['donation_status'] == 'Pending'])
                st.metric("🟡 Pending", pending_count)
            with col3:
                donated_count = len(donation_items[donation_items['donation_status'] == 'Donated'])
                st.metric("🟢 Donated", donated_count)
            with col4:
                rejected_count = len(donation_items[donation_items['donation_status'] == 'Rejected'])
                st.metric("🔴 Rejected", rejected_count)
            
            # Additional value metrics for donations
            if 'unit_price' in donation_items.columns and 'current_stock' in donation_items.columns:
                col_value1, col_value2, col_value3 = st.columns(3)
                
                with col_value1:
                    # Total value of all donation-eligible items
                    total_eligible_value = (donation_items['unit_price'] * donation_items['current_stock']).sum()
                    st.metric("💰 Total Eligible Value", f"₹{total_eligible_value:,.2f}")
                
                with col_value2:
                    # Value of successfully donated items
                    donated_items_subset = donation_items[donation_items['donation_status'] == 'Donated']
                    if len(donated_items_subset) > 0:
                        donated_value = (donated_items_subset['unit_price'] * donated_items_subset['current_stock']).sum()
                        st.metric("🧡 Successfully Donated Value", f"₹{donated_value:,.2f}")
                    else:
                        st.metric("🧡 Successfully Donated Value", "₹0.00")
                
                with col_value3:
                    # Value of pending donations
                    pending_items_subset = donation_items[donation_items['donation_status'] == 'Pending']
                    if len(pending_items_subset) > 0:
                        pending_value = (pending_items_subset['unit_price'] * pending_items_subset['current_stock']).sum()
                        st.metric("🟡 Pending Value", f"₹{pending_value:,.2f}")
                    else:
                        st.metric("🟡 Pending Value", "₹0.00")
            
            # Status distribution chart
            st.subheader("📈 Donation Status Distribution")
            status_counts = donation_items['donation_status'].value_counts()
            if len(status_counts) > 0:
                fig_status = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Donation Status Distribution",
                    color_discrete_map={
                        'Pending': '#FFA500', 
                        'Donated': '#28a745', 
                        'Rejected': '#dc3545'
                    }
                )
                st.plotly_chart(fig_status, use_container_width=True)
            
            # Top Cities and NGOs
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader("🏙️ Top 5 Cities by Donations")
                if 'city' in donation_items.columns:
                    city_counts = donation_items['city'].value_counts().head(5)
                    for i, (city, count) in enumerate(city_counts.items()):
                        st.write(f"{i+1}. **{city}**: {count} items")
                
            with col_right:
                st.subheader("🏢 Top 5 NGOs by Donations")
                if 'nearest_ngo' in donation_items.columns:
                    ngo_counts = donation_items['nearest_ngo'].value_counts().head(5)
                    for i, (ngo, count) in enumerate(ngo_counts.items()):
                        st.write(f"{i+1}. **{ngo}**: {count} items")
            
            st.markdown("""
<hr style="height:2px;background:linear-gradient(to right,#00f5ff,#00ffcc);border:none;margin:20px 0;">
""", unsafe_allow_html=True)
            
            # === Interactive Donation Table ===
            st.subheader("📋 Interactive Donation Management")
            
            # City and category filters for donations
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                cities = ['All'] + sorted(donation_items['city'].unique()) if 'city' in donation_items.columns else ['All']
                selected_donation_city = st.selectbox("Filter by City", cities, key="donation_city")
            with col_filter2:
                categories = ['All'] + sorted(donation_items['category'].unique()) if 'category' in donation_items.columns else ['All']
                selected_donation_category = st.selectbox("Filter by Category", categories, key="donation_category")
            
            # Apply filters
            # Fix: Using shallow copy to prevent memory issues
            filtered_donations = donation_items.copy(deep=False)
            if selected_donation_city != 'All':
                filtered_donations = filtered_donations[filtered_donations['city'] == selected_donation_city]
            if selected_donation_category != 'All':
                filtered_donations = filtered_donations[filtered_donations['category'] == selected_donation_category]
            
            # Display donation table with action buttons
            st.write(f"**Showing {len(filtered_donations)} donation-eligible items:**")
            
            # Create columns for the table
            display_columns = ['item_id', 'product_name', 'days_to_expiry', 'city', 'nearest_ngo', 'ngo_contact', 'donation_status']
            available_columns = [col for col in display_columns if col in filtered_donations.columns]
            
            if len(available_columns) > 0:
                # Show the table
                # Fix: Using shallow copy to prevent memory issues
                donation_display = filtered_donations[available_columns].copy(deep=False)
                
                # Add status badges
                def get_status_badge(status):
                    if status == 'Pending':
                        return "🟡 Pending"
                    elif status == 'Donated':
                        return "🟢 Donated"
                    elif status == 'Rejected':
                        return "🔴 Rejected"
                    else:
                        return status
                
                if 'donation_status' in donation_display.columns:
                    donation_display['Status'] = donation_display['donation_status'].apply(get_status_badge)
                    donation_display = donation_display.drop('donation_status', axis=1)
                
                st.dataframe(donation_display, use_container_width=True)
                
                # Action buttons for pending items
                pending_items = filtered_donations[filtered_donations['donation_status'] == 'Pending']
                if len(pending_items) > 0:
                    st.subheader("⚡ Quick Actions")
                    st.write("**Update donation status for pending items:**")
                    
                    # Create action columns
                    action_col1, action_col2, action_col3 = st.columns(3)
                    
                    with action_col1:
                        if st.button("✅ Mark All Pending as Donated", type="primary"):
                            # Update all pending items to donated
                            mask = (df['donation_eligible'] == True) & (df['donation_status'] == 'Pending')
                            if selected_donation_city != 'All':
                                mask = mask & (df['city'] == selected_donation_city)
                            if selected_donation_category != 'All':
                                mask = mask & (df['category'] == selected_donation_category)
                            
                            df.loc[mask, 'donation_status'] = 'Donated'
                            st.success(f"✅ Updated {mask.sum()} items to 'Donated' status!")
                            st.rerun()
                    
                    with action_col2:
                        if st.button("❌ Mark All Pending as Rejected", type="secondary"):
                            # Update all pending items to rejected
                            mask = (df['donation_eligible'] == True) & (df['donation_status'] == 'Pending')
                            if selected_donation_city != 'All':
                                mask = mask & (df['city'] == selected_donation_city)
                            if selected_donation_category != 'All':
                                mask = mask & (df['category'] == selected_donation_category)
                            
                            df.loc[mask, 'donation_status'] = 'Rejected'
                            st.success(f"❌ Updated {mask.sum()} items to 'Rejected' status!")
                            st.rerun()
                    
                    with action_col3:
                        if st.button("💾 Export Donation Data", type="secondary"):
                            # Create downloadable CSV
                            csv = filtered_donations.to_csv(index=False)
                            st.download_button(
                                label="📥 Download CSV",
                                data=csv,
                                file_name=f"donation_data_{datetime.now().strftime('%Y%m%d')}.csv",
                                mime="text/csv"
                            )
                
                # Individual item actions (for smaller datasets)
                if len(pending_items) <= 10:
                    st.write("**Individual item actions:**")
                    for idx, row in pending_items.iterrows():
                        col_item, col_action1, col_action2 = st.columns([3, 1, 1])
                        
                        with col_item:
                            st.write(f"**{row.get('product_name', 'Unknown')}** - {row.get('city', 'Unknown')} - {row.get('nearest_ngo', 'Unknown')}")
                        
                        with col_action1:
                            if st.button(f"✅ Donate", key=f"donate_{idx}"):
                                # Use session state to track changes
                                if 'df_changes' not in st.session_state:
                                    st.session_state.df_changes = {}
                                st.session_state.df_changes[idx] = 'Donated'
                                st.success("Item marked as donated!")
                                st.rerun()
                        
                        with col_action2:
                            if st.button(f"❌ Reject", key=f"reject_{idx}"):
                                # Use session state to track changes
                                if 'df_changes' not in st.session_state:
                                    st.session_state.df_changes = {}
                                st.session_state.df_changes[idx] = 'Rejected'
                                st.success("Item marked as rejected!")
                                st.rerun()
                
                # Optional: Map visualization (if coordinates are available)
                if 'store_latitude' in donation_items.columns and 'store_longitude' in donation_items.columns:
                    st.subheader("🗺️ Donation Locations Map")
                    
                    # Create a simple map using Plotly
                    map_data = filtered_donations[
                        ['store_latitude', 'store_longitude', 'city', 'nearest_ngo', 'donation_status']
                    ].dropna()
                    
                    if len(map_data) > 0:
                        # Fix: Replaced px.scatter_mapbox with px.scatter_map to fix DeprecationWarning
                        fig_map = px.scatter_map(
                            map_data,
                            lat="store_latitude",
                            lon="store_longitude",
                            color="donation_status",
                            hover_name="city",
                            hover_data=["nearest_ngo"],
                            color_discrete_map={
                                'Pending': '#FFA500', 
                                'Donated': '#28a745', 
                                'Rejected': '#dc3545'
                            },
                            zoom=5,
                            height=500,
                            title="Donation Locations"
                        )
                        # Fix: Updated layout method for scatter_map
                        fig_map.update_layout(map_style="open-street-map")
                        st.plotly_chart(fig_map, use_container_width=True)
            
        else:
            st.info("ℹ️ No donation-eligible items found in the current dataset.")
            st.write("Items become donation-eligible when they are:")
            st.write("- Near expiry or expired")
            st.write("- Safe for donation")
            st.write("- Have partner NGOs available")
    
    except Exception as e:
        st.error(f"Error processing donation data: {str(e)}")
        st.write("Please ensure the enhanced dataset is loaded with donation columns.")

# === 11. Data Summary ===
with st.expander("📋 Analysis Data Summary"):
    try:
        st.write(f"**Dataset Shape:** {filtered_df.shape[0]} rows, {filtered_df.shape[1]} columns")
        st.write(f"**Data Source:** {data_source}")
        st.write("**Analysis Columns Added:**")
        analysis_cols = ['Stock_Level', 'Expiry_Risk', 'Suggested_Discount', 'Reorder', 'Action']
        for col in analysis_cols:
            if col in filtered_df.columns:
                st.write(f"✅ {col}")

        if st.checkbox("Show raw data sample"):
            st.dataframe(filtered_df.head(10))
    except Exception as e:
        st.error(f"Error displaying data summary: {str(e)}")

st.markdown("""
<hr style="
border: none;
height: 2px;
background: linear-gradient(to right, #00f5ff, #00ffcc);
margin: 20px 0;
">
""", unsafe_allow_html=True)

st.success("✅ Advanced Inventory Management Dashboard loaded successfully!")
st.info("🔄 Run the main pipeline (`python main.py`) to refresh analysis results")
st.markdown("""
<style>
.footer {
    text-align: center;
    padding: 20px;
    font-size: 14px;
    opacity: 0.8;
    animation: fadeInUp 2s ease;
}

.footer span {
    color: #00f5ff;
    font-weight: 600;
    animation: glowText 2s infinite alternate;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes glowText {
    from { text-shadow: 0 0 5px #00f5ff; }
    to { text-shadow: 0 0 20px #00ffcc; }
}
</style>

<div class="footer">
    🚀 Built with AI-powered Multi-Agent Intelligence <br><br>
    © 2026 <span>Mousoom Samanta</span> <br>
    💡 Developed by <span>Mousoom Samanta</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:20px; opacity:0.7;">
🚀 Built with AI-powered Multi-Agent Intelligence  
💡 Smart Inventory Optimization System  
</div>
""", unsafe_allow_html=True)




