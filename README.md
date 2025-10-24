# 🧩 FillMate  
**Smart Excel Missing-Value Detector & Filler**

FillMate is a minimalistic Python-powered web app that detects and fills missing values (nulls) in Excel files. It uses intelligent forward, backward, and nearest-neighbor algorithms to impute missing data and helps analysts quickly clean datasets.

---

## 🚀 Features
- 📊 Upload any `.xlsx` or `.csv` file  
- 🔍 View total null values and their locations  
- 🧠 Choose how to fill missing values:
  - **Forward Fill (ffill)** – uses previous values  
  - **Backward Fill (bfill)** – uses next values  
  - **Closest Value Algorithm** – fills using nearest non-null data points  
- 💾 Download the cleaned Excel file  
- 🌐 Simple, minimal UI built with **Streamlit**

---

## 🛠️ Technologies Used
- **Python 3.x**
- **Streamlit** — for the web interface  
- **Pandas** — for data handling and filling logic  
- **OpenPyXL** — for Excel file support  
- **GitHub Pages + Streamlit Cloud** — for free hosting  

---

## 📦 Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fillmate.git
cd fillmate
