import streamlit as st
import pandas as pd
import numpy as np
import io
import os
from datetime import datetime
import plotly.express as px

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="FillMate", layout="wide")

# --- DARK MODE TOGGLE STATE ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# --- DARK MODE STYLING FUNCTION ---
def apply_theme():
    """Apply dark or light theme using custom CSS."""
    if st.session_state.dark_mode:
        css = """
        <style>
        body, .stApp {
            background-color: #000000 !important;
            color: #ffffff !important;
        }
        .stButton>button {
            background-color: #333333 !important;
            color: #ffffff !important;
            border: 1px solid #555555 !important;
        }
        .stSelectbox, .stFileUploader, .stDownloadButton, .stMetric {
            color: #ffffff !important;
        }
        div[data-testid="stMarkdownContainer"], div[data-testid="stDataFrame"] {
            color: #ffffff !important;
        }
        </style>
        """
    else:
        css = """
        <style>
        body, .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

apply_theme()

# --- HEADER ---
col1, col2 = st.columns([9, 1])
with col1:
    text_color = "#ffffff" if st.session_state.dark_mode else "#000000"
    st.markdown(
        f"<h3 style='text-align:center; color:{text_color};'>🧠 FillMate — Smart Null Value Handler</h3>",
        unsafe_allow_html=True,
    )
with col2:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="mode_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown(
    f"<p style='text-align:center; color:{text_color}; font-size:15px;'>Detect, visualize, and fill missing values in Excel or CSV files — effortlessly.</p>",
    unsafe_allow_html=True,
)

# ----------------- FUNCTIONS -----------------
def fill_null_values(df, method):
    if method == "Forward Fill":
        return df.ffill()
    elif method == "Backward Fill":
        return df.bfill()
    elif method == "Closest Fill (Mean of Neighbors)":
        return df.interpolate(method='linear', limit_direction='both')
    return df

def save_analytics(num_nulls, num_filled, filename):
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
    analytics_file = "analytics_log.csv"
    if os.path.exists(analytics_file):
        return pd.read_csv(analytics_file)
    return pd.DataFrame(columns=["timestamp", "file_name", "total_nulls", "total_filled"])

def download_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='FilledData')
    return output.getvalue()

# ----------------- FILE UPLOAD SECTION -----------------
uploaded_file = st.file_uploader("📂 Upload your Excel or CSV file", type=["xlsx", "xls", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📊 Uploaded Data Preview")
    st.dataframe(df.head())

    null_counts = df.isnull().sum()
    total_nulls = int(null_counts.sum())

    st.write(f"### ❌ Total Null Values: {total_nulls}")
    st.write("#### Columns with Nulls:")
    st.write(null_counts[null_counts > 0])

    st.markdown("---")
    st.subheader("⚙️ Fill Missing Values")
    fill_method = st.selectbox("Select a filling method:",
                               ["Forward Fill", "Backward Fill", "Closest Fill (Mean of Neighbors)"])

    if st.button("Apply Fill"):
        filled_df = fill_null_values(df, fill_method)
        num_filled = int(filled_df.isnull().sum().sum())
        save_analytics(total_nulls, num_filled, uploaded_file.name)

        st.success(f"✅ Null values filled using {fill_method}")
        st.dataframe(filled_df.head())

        st.markdown("### 💾 Download Processed File")
        csv_data = filled_df.to_csv(index=False).encode('utf-8')
        excel_data = download_excel(filled_df)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Download CSV", data=csv_data, file_name="filled_data.csv", mime="text/csv")
        with col2:
            st.download_button("⬇️ Download Excel", data=excel_data, file_name="filled_data.xlsx")

        # --- LIVE ANALYTICS ---
        st.markdown("---")
        st.header("📈 FillMate Analytics Dashboard")

        analytics_df = load_analytics()
        if not analytics_df.empty:
            total_files = len(analytics_df)
            total_nulls_detected = int(analytics_df["total_nulls"].sum())
            total_filled = int(analytics_df["total_filled"].sum())

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Files Processed", total_files)
            col2.metric("Total Nulls Detected", total_nulls_detected)
            col3.metric("Total Nulls Filled", total_filled)

            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                fig_bar = px.bar(
                    analytics_df,
                    x="file_name",
                    y="total_nulls",
                    color="total_nulls",
                    title="Null Values per File"
                )
                fig_bar.update_layout(
                    plot_bgcolor="#000000" if st.session_state.dark_mode else "#ffffff",
                    paper_bgcolor="#000000" if st.session_state.dark_mode else "#ffffff",
                    font=dict(color="#ffffff" if st.session_state.dark_mode else "#000000")
                )
                st.plotly_chart(fig_bar, use_container_width=True)

            with chart_col2:
                fig_line = px.line(
                    analytics_df,
                    x="timestamp",
                    y="total_filled",
                    markers=True,
                    title="Filled Values Over Time"
                )
                fig_line.update_layout(
                    plot_bgcolor="#000000" if st.session_state.dark_mode else "#ffffff",
                    paper_bgcolor="#000000" if st.session_state.dark_mode else "#ffffff",
                    font=dict(color="#ffffff" if st.session_state.dark_mode else "#000000")
                )
                st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No analytics data available yet. Upload and process some files to see insights!")

# ----------------- FOOTER -----------------
st.markdown("---")
st.caption("Developed with ❤️ by Haseeb — Simplifying Data Cleaning")
