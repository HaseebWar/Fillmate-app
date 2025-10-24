import streamlit as st
import pandas as pd

# ---------------------------
# App Configuration
# ---------------------------
st.set_page_config(page_title="FillMate | Excel Null Cleaner", layout="wide")

# ---------------------------
# Header Section
# ---------------------------
st.title("🧹 FillMate")
st.markdown("""
### Smart Excel Null Value Cleaner
Upload your Excel or CSV file to detect and handle missing values with intelligent filling algorithms.
""")

# Optional style for minimal look
st.markdown("""
<style>
    body {
        background-color: #f7f9fb;
    }
    .stApp {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# File Upload
# ---------------------------
uploaded_file = st.file_uploader("📁 Upload your Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file is not None:
    # Load data
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

    st.subheader("📊 Null Value Summary")

    # Calculate nulls
    null_summary = df.isnull().sum().to_frame("Null Count")
    null_summary["Null Percentage (%)"] = (df.isnull().sum() / len(df) * 100).round(2)
    st.dataframe(null_summary, use_container_width=True)

    # Columns with missing values
    cols_with_nulls = [col for col in df.columns if df[col].isnull().any()]
    if cols_with_nulls:
        st.info(f"Columns containing nulls: {', '.join(cols_with_nulls)}")
    else:
        st.success("✅ No missing values found!")
    
    st.divider()

    # ---------------------------
    # Fill Options
    # ---------------------------
    st.subheader("⚙️ Fill Missing Values")

    fill_method = st.selectbox(
        "Select a method to fill missing values:",
        ["None", "Forward Fill", "Backward Fill", "Mean", "Median", "Mode", "Interpolation"]
    )

    if fill_method != "None":
        df_filled = df.copy()

        # Apply chosen fill method
        if fill_method == "Forward Fill":
            df_filled = df.fillna(method="ffill")
        elif fill_method == "Backward Fill":
            df_filled = df.fillna(method="bfill")
        elif fill_method == "Mean":
            df_filled = df.fillna(df.mean(numeric_only=True))
        elif fill_method == "Median":
            df_filled = df.fillna(df.median(numeric_only=True))
        elif fill_method == "Mode":
            for col in df.columns:
                try:
                    mode_val = df[col].mode()[0]
                    df_filled[col].fillna(mode_val, inplace=True)
                except:
                    pass
        elif fill_method == "Interpolation":
            df_filled = df.interpolate()

        st.success(f"✅ Missing values filled using **{fill_method}** method!")

        st.subheader("📋 Cleaned Data Preview")
        st.dataframe(df_filled.head(20), use_container_width=True)

        # ---------------------------
        # Download Cleaned Data
        # ---------------------------
        st.divider()
        csv_data = df_filled.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Cleaned CSV File",
            data=csv_data,
            file_name="fillmate_cleaned_data.csv",
            mime="text/csv"
        )

        st.caption("Tip: If Excel download is needed, save CSV as .xlsx in Excel later.")

    st.divider()

    # ---------------------------
    # Extra Info
    # ---------------------------
    with st.expander("ℹ️ About FillMate"):
        st.markdown("""
        **FillMate** helps analysts and data engineers clean Excel datasets quickly.
        - Detects and summarizes null values
        - Offers statistical and algorithmic filling methods
        - Simple, clean, and browser-based
        """)
else:
    st.info("👆 Please upload an Excel or CSV file to begin.")
