import streamlit as st
import pandas as pd
import numpy as np
import io
import os
from datetime import datetime

st.set_page_config(page_title="FillMate", layout="wide")

# ========== Helper Functions ==========

def fill_null_values(df, method):
    """Fill null values based on selected method."""
    if method == "Forward Fill":
        return df.ffill()
    elif method == "Backward Fill":
        return df.bfill()
    elif method == "Closest Fill (Mean of Neighbors)":
        return df.interpolate(method='linear', limit_direction='both')
    else:
        return df

def save_analytics(num_nulls, num_filled, filename):
    """Save analytics locally to CSV file."""
    analytics_file = "analytics_log.csv"
    data = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "file_name": [filename],
        "total_nulls": [num_nulls],
        "total_filled": [num_filled]
    }
    df_log = pd.DataFrame(data)

    if os.path.exists(analytics_file):
        df_log.to_csv(analytics_file, mode='a', header=False, index=False)
    else:
        df_log.to_csv(analytics_file, index=False)

def load_analytics():
    """Load local analytics file."""
    analytics_file = "analytics_log.csv"
    if os.path.exists(analytics_file):
        return pd.read_csv(analytics_file)
    return pd.DataFrame(columns=["timestamp", "file_name", "total_nulls", "total_filled"])

def download_excel(df):
    """Convert dataframe to Excel for download."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='FilledData')
    return output.getvalue()

# ========== UI Layout ==========

st.title("🧠 FillMate — Smart Null Value Handler")
st.markdown("Effortlessly detect and fill missing data in Excel files with advanced options.")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📊 Uploaded Data Preview")
    st.dataframe(df.head())

    # Detect nulls
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()

    st.write(f"### ❌ Total Null Values: {total_nulls}")
    st.write("#### Columns with Nulls:")
    st.write(null_counts[null_counts > 0])

    # Fill method selection
    st.markdown("---")
    st.subheader("⚙️ Fill Missing Values")
    fill_method = st.selectbox("Select a filling method:", 
                               ["Forward Fill", "Backward Fill", "Closest Fill (Mean of Neighbors)"])

    if st.button("Apply Fill"):
        filled_df = fill_null_values(df, fill_method)
        num_filled = filled_df.isnull().sum().sum()
        save_analytics(total_nulls, num_filled, uploaded_file.name)

        st.success(f"✅ Null values filled using {fill_method}")
        st.dataframe(filled_df.head())

        # Export section
        st.markdown("### 💾 Download Processed File")
        csv_data = filled_df.to_csv(index=False).encode('utf-8')
        excel_data = download_excel(filled_df)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Download CSV", data=csv_data, file_name="filled_data.csv", mime="text/csv")
        with col2:
            st.download_button("⬇️ Download Excel", data=excel_data, file_name="filled_data.xlsx")

# ========== Analytics Dashboard ==========

st.markdown("---")
st.header("📈 FillMate Analytics Dashboard")

analytics_df = load_analytics()

if not analytics_df.empty:
    st.dataframe(analytics_df)

    st.metric("Total Files Processed", len(analytics_df))
    st.metric("Total Nulls Detected", int(analytics_df["total_nulls"].sum()))
    st.metric("Total Nulls Filled", int(analytics_df["total_filled"].sum()))

    # Allow download of analytics report
    csv_report = analytics_df.to_csv(index=False).encode('utf-8')
    st.download_button("📊 Download Analytics CSV", data=csv_report, file_name="fillmate_analytics.csv", mime="text/csv")
else:
    st.info("No analytics data available yet. Upload and process some files to see insights!")

# ========== Theme Toggle ==========

st.markdown("---")
st.markdown("🌙 **Theme Mode:** Use the Streamlit built-in theme switcher (top-right corner) to toggle Dark/Light Mode.")

