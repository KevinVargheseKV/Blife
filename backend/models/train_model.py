import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier


# Load dataset
df = pd.read_csv("D:\\blife\\backend\\simulator\\patient_data.csv")


# Features (Input)
X = df[[
    "SpO2",
    "HeartRate",
    "RespiratoryRate",
    "AirwayPressure",
    "TidalVolume",
    "FiO2"
]]


# Target (Output)
y = df["RiskLevel"]


# Convert labels into numbers
label_mapping = {
    "Stable": 0,
    "Warning": 1,
    "Critical": 2
}

y = y.map(label_mapping)


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ---------------- RANDOM FOREST ---------------- #

rf_model = RandomForestClassifier()

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_predictions)

print("\nRandom Forest Accuracy:", rf_accuracy)


# ---------------- XGBOOST ---------------- #

xgb_model = XGBClassifier()

xgb_model.fit(X_train, y_train)

xgb_predictions = xgb_model.predict(X_test)

xgb_accuracy = accuracy_score(y_test, xgb_predictions)

print("XGBoost Accuracy:", xgb_accuracy)


# Best Model Selection
if xgb_accuracy > rf_accuracy:
    print("\nBest Model: XGBoost")

else:
    print("\nBest Model: Random Forest")
# Save best model

if xgb_accuracy > rf_accuracy:

    joblib.dump(xgb_model, "blife_model.pkl")

    print("XGBoost model saved successfully!")

else:

    joblib.dump(rf_model, "blife_model.pkl")

    print("Random Forest model saved successfully!")