import pandas as pd

# Load dataset
df = pd.read_csv("creditcard.csv")

# 1. Show first 5 rows
print("First 5 rows:")
print(df.head())

# 2. Dataset info
print("\nDataset Info:")
print(df.info())

# 3. Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# 4. Class distribution (IMPORTANT)
print("\nClass distribution:")
print(df['Class'].value_counts())

# -------------------------------
# Data Preprocessing
# -------------------------------

from sklearn.preprocessing import StandardScaler

# Normalize 'Amount'
scaler = StandardScaler()
df['Amount'] = scaler.fit_transform(df[['Amount']])

# Drop 'Time' column (not useful)
df = df.drop(['Time'], axis=1)

print("\nAfter preprocessing:")
print(df.head())

# -------------------------------
# Handle Imbalanced Data
# -------------------------------

fraud = df[df['Class'] == 1]
normal = df[df['Class'] == 0]

# Take equal number of normal transactions
normal_sample = normal.sample(n=len(fraud), random_state=42)

# Combine both
new_df = pd.concat([fraud, normal_sample])

print("\nNew class distribution:")
print(new_df['Class'].value_counts())

# -------------------------------
# Split data into X and y
# -------------------------------

X = new_df.drop('Class', axis=1)  # features
y = new_df['Class']               # target

# -------------------------------
# Train-Test Split
# -------------------------------

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Train Model
# -------------------------------

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)

print("\nModel training completed ✅")

# -------------------------------
# Model Evaluation
# -------------------------------

from sklearn.metrics import accuracy_score, classification_report

# Predict on test data
y_pred = model.predict(X_test)

# Accuracy
print("\nAccuracy:", accuracy_score(y_test, y_pred))

# Detailed report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

## -------------------------------
# Confusion Matrix 
# -------------------------------

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:\n", cm)

# Clear any previous plots
plt.figure(figsize=(5,4))

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.show()

# -------------------------------
# Random Forest Model (FINAL)
# -------------------------------

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Train model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predict using Random Forest 
y_pred = rf_model.predict(X_test)

print("\nRandom Forest Results:")

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

import pickle

# Save model
with open("fraud_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)

# Save scaler
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("✅ Model & Scaler saved")