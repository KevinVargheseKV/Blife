import time
import joblib
import pandas as pd

from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# Load trained BLife model
model = joblib.load("blife_model.pkl")

# Label decoding
label_mapping = {
    0: "Stable",
    1: "Warning",
    2: "Critical"
}

print("BLife Real-Time Prediction Started...\n")

# Continuous prediction loop
while True:

    # Read latest patient data
    df = pd.read_csv("../simulator/patient_data.csv")

    latest_patient = df.iloc[-1]

    # Create dataframe for prediction
    patient_data = pd.DataFrame([{
        "SpO2": latest_patient["SpO2"],
        "HeartRate": latest_patient["HeartRate"],
        "RespiratoryRate": latest_patient["RespiratoryRate"],
        "AirwayPressure": latest_patient["AirwayPressure"],
        "TidalVolume": latest_patient["TidalVolume"],
        "FiO2": latest_patient["FiO2"]
    }])

    # Predict condition
    prediction = model.predict(patient_data)[0]

    # Convert numeric prediction to label
    risk_level = label_mapping[prediction]

    print("\n==============================")

    # Color-based alerts
    if risk_level == "Stable":

        print(Fore.GREEN + f"Latest Patient Condition: {risk_level}")

    elif risk_level == "Warning":

        print(Fore.YELLOW + f"Latest Patient Condition: {risk_level}")

    else:

        print(Fore.RED + f"Latest Patient Condition: {risk_level}")

    # Display patient vitals
    print(patient_data)

    # Wait before next prediction
    time.sleep(1)