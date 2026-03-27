import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load model and scaler
model = pickle.load(open("fraud_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.set_page_config(page_title="Bank Fraud Detection", layout="wide")

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
    <h1 style='text-align: center; color: #1f4e79;'>🏦 SecureBank Fraud Detection System</h1>
    <hr>
""", unsafe_allow_html=True)

st.markdown("### 📂 Upload Transaction Data")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### 📊 Dataset Preview")
    st.dataframe(df.head())

    # Select a row
    st.write("### 🔍 Select Transaction Row")
    row_index = st.number_input(
        "Enter row index",
        min_value=0,
        max_value=len(df)-1,
        step=1
    )

    if st.button("🚀 Predict Selected Transaction"):

        try:
            # Select row
            selected_row = df.iloc[row_index]

            # Convert to DataFrame
            selected_row = pd.DataFrame([selected_row])

            # -------------------------------
            # Preprocessing (IMPORTANT)
            # -------------------------------

            # Drop unnecessary columns
            if 'Class' in selected_row.columns:
                selected_row = selected_row.drop('Class', axis=1)

            if 'Time' in selected_row.columns:
                selected_row = selected_row.drop('Time', axis=1)

            # Scale Amount (VERY IMPORTANT)
            if 'Amount' in selected_row.columns:
                selected_row['Amount'] = scaler.transform(selected_row[['Amount']])

            # Convert to numpy
            data = selected_row.values

            # -------------------------------
            # Prediction
            # -------------------------------
            prediction = model.predict(data)

            st.markdown("---")

            if prediction[0] == 1:
                st.error("⚠️ FRAUD DETECTED!")
            else:
                st.success("✅ Legitimate Transaction")

        except Exception as e:
            st.warning(f"Error: {e}")