🏦 SecureBank – Credit Card Fraud Detection System

SecureBank is a machine learning–powered web application that detects fraudulent credit card transactions in real time and enhances security using OTP verification.

This project simulates a real-world banking system where transactions are analyzed instantly, classified as legitimate or fraudulent, and appropriate actions are taken automatically.

Features:
Machine Learning-based Fraud Detection (Random Forest)
Real-Time Transaction Processing
OTP Verification for Suspicious Transactions
Automatic Fraud Blocking
Realistic Banking Interface
Dynamic Balance Updates
Transaction History Tracking
Email Alerts for Security

How It Works?
User enters transaction details:
Amount
Location
Merchant Type
Device
The model calculates a fraud risk score (0–1)
Based on the score:
✅ Low Risk (< 0.2) → Transaction Approved
⚠️ Medium Risk (0.2–0.5) → OTP Verification
🚨 High Risk (> 0.5) → Transaction Blocked
Transaction is recorded and balance is updated

Tech Stack:
Python 
Machine Learning (Scikit-learn)
Streamlit
Pandas & NumPy
SMTP (Email OTP System)

Machine Learning Model
Dataset: Credit Card Fraud Detection Dataset
Algorithms Used:
Logistic Regression
Random Forest (Final Model)

Techniques:
Data preprocessing
Feature scaling
Handling imbalanced data

🔐 Security Features
OTP-based transaction verification
Email alerts for suspicious activity
Masked card details for privacy
