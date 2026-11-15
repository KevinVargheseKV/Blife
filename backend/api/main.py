from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import pandas as pd
import joblib

# -----------------------------------
# FastAPI App
# -----------------------------------

app = FastAPI()

# -----------------------------------
# Enable CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Load ML Model
# -----------------------------------

model = joblib.load(
    "D:\\blife\\backend\\models\\blife_model.pkl"
)

# -----------------------------------
# Risk Labels
# -----------------------------------

label_mapping = {
    0: "Stable",
    1: "Warning",
    2: "Critical"
}

# -----------------------------------
# Dynamic Disease Storage
# -----------------------------------

patient_diseases = {

    "ICU Bed 1": "Post-Surgery Recovery",

    "ICU Bed 2": "Pneumonia",

    "ICU Bed 3": "ARDS",

    "ICU Bed 4": "Sepsis"
}

# -----------------------------------
# Disease Update Model
# -----------------------------------

class DiseaseUpdate(BaseModel):

    bed: str

    disease: str

# -----------------------------------
# Home Route
# -----------------------------------

@app.get("/")
def home():

    return {
        "message":
        "BLife ICU Monitoring API Running"
    }

# -----------------------------------
# Update Disease Route
# -----------------------------------

@app.post("/set-disease")
def set_disease(update: DiseaseUpdate):

    patient_diseases[update.bed] = update.disease

    return {
        "message":
        "Disease updated successfully"
    }

# -----------------------------------
# Prediction Route
# -----------------------------------

@app.get("/predict")
def predict():

    # Read simulator CSV
    df = pd.read_csv(
        "D:\\blife\\backend\\simulator\\patient_data.csv"
    )

    # Get latest patient row from each bed
    latest_patients = (
        df.groupby("Bed")
        .tail(1)
    )

    all_beds = {}

    # -----------------------------------
    # Process Each ICU Bed
    # -----------------------------------

    for _, patient in latest_patients.iterrows():

        patient_data = pd.DataFrame([{

            "SpO2":
            patient["SpO2"],

            "HeartRate":
            patient["HeartRate"],

            "RespiratoryRate":
            patient["RespiratoryRate"],

            "AirwayPressure":
            patient["AirwayPressure"],

            "TidalVolume":
            patient["TidalVolume"],

            "FiO2":
            patient["FiO2"]
        }])

        # ML Prediction
        prediction = model.predict(
            patient_data
        )[0]

        risk_level = label_mapping[prediction]

        # -----------------------------------
        # Dynamic Disease
        # -----------------------------------

        disease = patient_diseases[
            patient["Bed"]
        ]

        # -----------------------------------
        # Dynamic Medical Reasoning
        # -----------------------------------

        spo2 = int(patient["SpO2"])

        hr = int(patient["HeartRate"])

        rr = int(patient["RespiratoryRate"])

        medical_message = ""

        # ---------- ARDS ----------

        if disease == "ARDS":

            if spo2 < 88 and rr > 30:

                medical_message = (
                    "Severe oxygen desaturation "
                    "with escalating respiratory "
                    "distress detected. "
                    "High probability of acute "
                    "respiratory failure."
                )

            elif spo2 < 92:

                medical_message = (
                    "Progressive oxygen decline "
                    "suggests worsening lung "
                    "compliance and respiratory "
                    "instability."
                )

            else:

                medical_message = (
                    "Respiratory parameters "
                    "currently stable under "
                    "ARDS monitoring."
                )

        # ---------- SEPSIS ----------

        elif disease == "Sepsis":

            if hr > 125:

                medical_message = (
                    "Persistent tachycardia with "
                    "systemic instability detected. "
                    "Possible septic shock "
                    "progression."
                )

            else:

                medical_message = (
                    "Hemodynamic monitoring ongoing "
                    "for possible septic progression."
                )

        # ---------- COPD ----------

        elif disease == "COPD":

            if spo2 < 90:

                medical_message = (
                    "Chronic oxygen compromise with "
                    "worsening ventilation pattern "
                    "detected. Risk of respiratory "
                    "decompensation increasing."
                )

            else:

                medical_message = (
                    "COPD patient currently "
                    "maintaining acceptable "
                    "oxygenation."
                )

        # ---------- PNEUMONIA ----------

        elif disease == "Pneumonia":

            if spo2 < 91 and rr > 24:

                medical_message = (
                    "Respiratory infection pattern "
                    "worsening with oxygen "
                    "deterioration risk."
                )

            else:

                medical_message = (
                    "Pulmonary infection monitoring "
                    "active with moderate "
                    "respiratory stress."
                )

        # ---------- CARDIAC ----------

        elif disease == "Cardiac Instability":

            if hr > 130:

                medical_message = (
                    "Cardiovascular instability with "
                    "abnormal heart rate escalation "
                    "detected. Possible arrhythmia-"
                    "related emergency."
                )

            else:

                medical_message = (
                    "Cardiac rhythm monitoring "
                    "active with moderate "
                    "hemodynamic instability."
                )

        # ---------- ASTHMA ----------

        elif disease == "Asthma":

            if rr > 28:

                medical_message = (
                    "Elevated respiratory workload "
                    "suggests acute bronchospasm "
                    "risk and airway narrowing."
                )

            else:

                medical_message = (
                    "Airway monitoring active for "
                    "possible asthma exacerbation."
                )

        # ---------- STROKE ----------

        elif disease == "Stroke":

            medical_message = (
                "Neurological observation active "
                "with continuous vital stability "
                "monitoring."
            )

        # ---------- DEFAULT ----------

        else:

            medical_message = (
                "Continuous ICU monitoring "
                "in progress."
            )

        # -----------------------------------
        # Final API Response
        # -----------------------------------

        all_beds[patient["Bed"]] = {

            "SpO2":
            spo2,

            "HeartRate":
            hr,

            "RespiratoryRate":
            rr,

            "AirwayPressure":
            int(patient["AirwayPressure"]),

            "TidalVolume":
            int(patient["TidalVolume"]),

            "FiO2":
            int(patient["FiO2"]),

            "Disease":
            disease,

            "RiskLevel":
            risk_level,

            "EmergencyPrediction":
            medical_message
        }

    return all_beds