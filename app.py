import streamlit as st
import pickle
import numpy as np
import random
import smtplib
import pandas as pd
from email.mime.text import MIMEText

# -------------------------------
# LOAD MODEL
# -------------------------------
model = pickle.load(open("fraud_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.set_page_config(page_title="SecureBank", layout="wide")

# -------------------------------
# SESSION INIT
# -------------------------------
if "balance" not in st.session_state:
    st.session_state.balance = 125000

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
.card {
    background: linear-gradient(135deg, #1f4e79, #16324f);
    padding: 20px;
    border-radius: 15px;
    color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
}
.balance {
    font-size: 28px;
    font-weight: bold;
}
.title {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1 style='text-align:center;'>🏦 SecureBank</h1>", unsafe_allow_html=True)

# -------------------------------
# ACCOUNT CARD
# -------------------------------
st.markdown(f"""
<div class="card">
    <div class="title">💳 Account Holder</div>
    <div class="balance">Tanvi Joshi</div>
    <br>
    <div class="title">💰 Available Balance</div>
    <div class="balance">₹ {st.session_state.balance}</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# MASKED CARD
# -------------------------------
def generate_masked_card():
    return f"**** **** **** {random.randint(1000,9999)}"

st.markdown(f"""
<div class="card">
    <div class="title">💳 Debit Card</div>
    <div class="balance">{generate_masked_card()}</div>
    <br>
    <div class="title">Expiry</div>
    <div>08/28</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# CARD INPUT
# -------------------------------
st.markdown("### 💳 Enter Card Details")

col1, col2 = st.columns(2)

with col1:
    card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
    card_name = st.text_input("Card Holder Name")

with col2:
    expiry = st.text_input("Expiry (MM/YY)", placeholder="08/28")
    cvv = st.text_input("CVV", type="password", max_chars=3)

if card_number:
    masked = "**** **** **** " + card_number[-4:]
    st.info(f"Using Card: {masked}")

# -------------------------------
# TRANSACTION INPUT
# -------------------------------
st.markdown("### 💸 Make a Payment")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("💳 Amount (₹)", min_value=1.0)
    location = st.selectbox("🌍 Location", ["India", "International"])

with col2:
    merchant = st.selectbox("🏪 Merchant", ["Trusted", "New Merchant", "High Risk"])
    device = st.selectbox("📱 Device", ["Registered Device", "New Device"])

# -------------------------------
# CONVERT TO NUMERIC
# -------------------------------
location_risk = 0.1 if location == "India" else 0.9
merchant_risk = {"Trusted":0.1, "New Merchant":0.5, "High Risk":0.9}[merchant]
device_risk = 0.1 if device == "Registered Device" else 0.8

# -------------------------------
# FEATURE GENERATION
# -------------------------------
def generate_remaining_features():
    return np.random.normal(0, 1, 25)

# -------------------------------
# EMAIL OTP
# -------------------------------
def send_otp_email():
    sender_email = "tanvijoshi2903@gmail.com"
    receiver_email = "tanvijoshi2903@gmail.com"
    password = "cswc dhvi gilw quhf"

    otp = str(random.randint(100000, 999999))

    msg = MIMEText(f"Your SecureBank OTP is: {otp}")
    msg["Subject"] = "🔐 SecureBank OTP"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

    return otp

# -------------------------------
# PROCESS PAYMENT
# -------------------------------
if st.button("🚀 Pay Now"):

    extra = generate_remaining_features()

    data = np.concatenate([
        [amount],
        [location_risk, merchant_risk, device_risk],
        extra
    ]).reshape(1, -1)

    data[0][0] = scaler.transform([[amount]])[0][0]

    prob = model.predict_proba(data)[0][1]

    # 🔥 DEMO BOOST
    if merchant == "High Risk":
        prob += 0.25
    if device == "New Device":
        prob += 0.2
    if location == "International":
        prob += 0.2

    prob = min(prob, 1.0)

    st.session_state.prob = prob
    st.session_state.current_amount = amount

# -------------------------------
# RESULT LOGIC
# -------------------------------
if "prob" in st.session_state:

    prob = st.session_state.prob
    amt = st.session_state.current_amount

    st.metric("Fraud Risk Score", f"{prob:.2f}")

    status = ""

    if prob > 0.5:
        st.error("🚨 Fraud Detected - Transaction Blocked")
        status = "Blocked"

    elif prob > 0.2:
        st.warning("⚠️ OTP Required")

        if "otp" not in st.session_state:
            st.session_state.otp = send_otp_email()

        user_otp = st.text_input("Enter OTP")

        if st.button("Verify OTP"):
            if user_otp == st.session_state.otp:
                st.success("✅ Payment Successful")
                st.session_state.balance -= amt
                status = "Approved"
                st.session_state.pop("otp")
            else:
                st.error("❌ Wrong OTP")
                status = "Failed"

    else:
        st.success("✅ Payment Successful")
        st.session_state.balance -= amt
        status = "Approved"

    # SAVE HISTORY
    if status != "":
        st.session_state.history.append({
            "Amount": amt,
            "Risk": round(prob, 2),
            "Status": status
        })

# -------------------------------
# TRANSACTION HISTORY
# -------------------------------
st.markdown("### 📊 Transaction History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)
else:
    st.write("No transactions yet")