import streamlit as st
import pandas as pd
import io

# -------------------------------
# 🧠 App Configuration
# -------------------------------
st.set_page_config(
    page_title="FillMate - Smart Excel Null Filler",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# 🎨 Custom CSS Styling
# -------------------------------
st.markdown("""
    <style>
        /* General page background and font */
        body, .main {
            background-color: #ffffff;
            font-family: 'Inter', sans-serif;
            color: #333333;
        }

        /* Center main container */
        .block-container {
            max-width: 1000px;
            margin: auto;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Headings */
        h1, h2, h3 {
            text-align: center;
            color: #2b2b2b;
        }

        /* Upload section styling */
        .stFileUploader {
            border: 2px dashed #B0BEC5;
            background: #FAFAFA;
            border-radius: 10px;
            padding: 1rem;
        }

        /* Buttons */
        div.stButton > button {
            background-color: #1976D2;
            color: white;
            border-radius: 8px;
            border: none;
            font-size: 16px;
            padding: 0.5rem 1rem;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #0D47A1;
        }

        /* Footer */
        footer {
            text-align: center;
            color: #888888;
            font-size: 13px;
            margin-top: 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 🧩 App Header
# -------------------------------
st.title("🧩 FillMate")
st.subheader("Smart Excel Missing-Value Detector & Filler")

st.markdown("""
Welcome to **FillMate** — your intelligent assistant for detecting and filling missing values in Excel or CSV datasets.  
Upload your file, choose a filling strategy, and download your clean dataset within seconds.
""")

st.divider()

# -------------------------------
# 📂 File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "csv"])

if uploaded_file:
    # Detect file type and load
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.success("✅ File uploaded successfully!")
    st.write("### Preview of your data:")
    st.dataframe(df.head())

    # -------------------------------
    # 🧮 Null Value Analysis
    # -------------------------------
    st.subheader("Null Value Analysis")
    total_nulls = df.isnull().sum().sum()
    st.write(f"🔍 **Total Missing Values:** {total_nulls}")

    st.write("#### Missing values per column:")
    st.dataframe(df.isnull().sum())

    # -------------------------------
    # ⚙️ Filling Options
    # -------------------------------
    st.subheader("Choose Filling Method")
    method = st.selectbox(
        "Select how you want to handle missing values:",
        ["Forward Fill", "Backward Fill", "Nearest Value (Linear Interpolation)"]
    )

    if st.button("🧠 Process & Fill Nulls"):
        if method == "Forward Fill":
            df_filled = df.fillna(method="ffill")
        elif method == "Backward Fill":
            df_filled = df.fillna(method="bfill")
        else:
            df_filled = df.interpolate(method="linear")

        # Show updated preview
        st.success("✅ Missing values have been filled successfully!")
        st.write("### Preview after filling:")
        st.dataframe(df_filled.head())

        # -------------------------------
        # 💾 Download Cleaned Data
        # -------------------------------
        buffer = io.BytesIO()
        df_filled.to_excel(buffer, index=False, engine="openpyxl")
        buffer.seek(0)

        st.download_button(
            label="📥 Download Cleaned Excel File",
            data=buffer,
            file_name="filled_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# -------------------------------
# 🦶 Footer
# -------------------------------
st.markdown("""
<footer>
    Made with ❤️ by <b>Muhammad Haseeb</b> | FillMate © 2025  
</footer>
""", unsafe_allow_html=True)
