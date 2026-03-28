import pandas as pd
import time
import pickle
import smtplib
import random
from email.mime.text import MIMEText

# -------------------------------
# EMAIL ALERT FUNCTION (FRAUD)
# -------------------------------
def send_email_alert(prob):
    sender_email = "tanvijoshi2903@gmail.com"
    receiver_emails = [
        "tanvijoshi2903@gmail.com",
        "tansings29@gmail.com"
    ]
    password = "cswc dhvi gilw quhf"

    subject = "🚨 Fraud Alert - Immediate Action Required"
    body = f"""
ALERT: Suspicious transaction detected!

Risk Score: {prob:.2f}

Please verify immediately.

- SecureBank
"""

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        for receiver in receiver_emails:
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver

            server.sendmail(sender_email, receiver, msg.as_string())

        server.quit()
        print("📧 Fraud alert sent!\n")

    except Exception as e:
        print("❌ Email error:", e)


# -------------------------------
# OTP EMAIL FUNCTION
# -------------------------------
def send_otp_email():
    sender_email = "tanvijoshi2903@gmail.com"
    receiver_email = "tanvijoshi2903@gmail.com"   # user email
    password = "cswc dhvi gilw quhf"

    otp = str(random.randint(100000, 999999))

    subject = "🔐 OTP Verification - SecureBank"
    body = f"""
Dear Customer,

A transaction has been flagged as suspicious.

🔐 Your OTP for verification is: {otp}

If this transaction was initiated by you:
Please open your SecureBank app/website and enter this OTP to approve.

If this was NOT you:
Do NOT share this OTP. Your transaction will be blocked automatically.

- SecureBank Fraud Detection System
"""

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email

        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("📧 OTP sent to your email!")

    except Exception as e:
        print("❌ OTP email error:", e)

    return otp


# -------------------------------
# LOAD MODEL & DATA
# -------------------------------
model = pickle.load(open("fraud_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

df = pd.read_csv("creditcard.csv")

print("🚀 Real-Time Fraud Detection Started...\n")

# -------------------------------
# REAL-TIME LOOP
# -------------------------------
while True:

    # 30% fraud simulation
    if random.random() < 0.3:
        row = df[df['Class'] == 1].sample(n=1)
    else:
        row = df[df['Class'] == 0].sample(n=1)

    # Preprocess
    row = row.drop(['Class', 'Time'], axis=1)
    row['Amount'] = scaler.transform(row[['Amount']])

    # Predict probability
    prob = model.predict_proba(row)[0][1]

    print(f"Transaction Risk Score: {prob:.2f}")

    # -------------------------------
    # DECISION ENGINE
    # -------------------------------
    if prob > 0.7:
        print("🚨 HIGH RISK FRAUD DETECTED!")
        send_email_alert(prob)

    elif prob > 0.3:
        print("⚠️ Suspicious Transaction - OTP Required")

        otp = send_otp_email()

        user_input = input("Enter OTP received in email: ")

        if user_input == otp:
            print("✅ OTP Verified - Transaction Approved\n")
        else:
            print("❌ Wrong OTP - Transaction Blocked\n")

    else:
        print("✅ Safe Transaction\n")

    time.sleep(1)