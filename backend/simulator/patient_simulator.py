import random
import time
import os
import pandas as pd
from datetime import datetime

FILE_NAME = "patient_data.csv"

print("BLife Realistic ICU Simulator Started...\n")

# -----------------------------------
# ICU Patient Profiles
# -----------------------------------

patients = {

    "ICU Bed 1": {

        "profile":
        "Post-Surgery Stable",

        "disease":
        "Post-Surgery Recovery",

        "state":
        "Stable",

        "spo2": 98,
        "hr": 76,
        "rr": 15,

        "deterioration_chance": 0.01,
        "recovery_chance": 0.05,

        "fluctuation": 1
    },

    "ICU Bed 2": {

        "profile":
        "Pneumonia Monitoring",

        "disease":
        "Pneumonia",

        "state":
        "Warning",

        "spo2": 92,
        "hr": 112,
        "rr": 25,

        "deterioration_chance": 0.04,
        "recovery_chance": 0.03,

        "fluctuation": 2
    },

    "ICU Bed 3": {

        "profile":
        "Critical ARDS",

        "disease":
        "ARDS",

        "state":
        "Critical",

        "spo2": 84,
        "hr": 138,
        "rr": 36,

        "deterioration_chance": 0.08,
        "recovery_chance": 0.01,

        "fluctuation": 3
    },

    "ICU Bed 4": {

        "profile":
        "Sepsis Recovery",

        "disease":
        "Sepsis",

        "state":
        "Warning",

        "spo2": 94,
        "hr": 102,
        "rr": 22,

        "deterioration_chance": 0.02,
        "recovery_chance": 0.06,

        "fluctuation": 1
    }
}

# -----------------------------------
# Patient Evolution
# -----------------------------------

def evolve_patient(patient):

    state = patient["state"]

    f = patient["fluctuation"]

    # Normal fluctuation
    patient["spo2"] += random.randint(-f, f)

    patient["hr"] += random.randint(
        -(f * 2),
        (f * 2)
    )

    patient["rr"] += random.randint(-f, f)

    # -----------------------------------
    # Disease-specific behavior
    # -----------------------------------

    if patient["disease"] == "ARDS":

        patient["spo2"] -= random.randint(0, 2)

        patient["rr"] += random.randint(0, 2)

    elif patient["disease"] == "Sepsis":

        patient["hr"] += random.randint(0, 4)

    elif patient["disease"] == "Pneumonia":

        patient["spo2"] -= random.randint(0, 1)

        patient["rr"] += random.randint(0, 1)

    # -----------------------------------
    # Stable state
    # -----------------------------------

    if state == "Stable":

        patient["spo2"] = max(
            95,
            min(100, patient["spo2"])
        )

        patient["hr"] = max(
            60,
            min(100, patient["hr"])
        )

        patient["rr"] = max(
            12,
            min(20, patient["rr"])
        )

        if random.random() < (
            patient["deterioration_chance"]
        ):

            patient["state"] = "Warning"

    # -----------------------------------
    # Warning state
    # -----------------------------------

    elif state == "Warning":

        patient["spo2"] = max(
            90,
            min(94, patient["spo2"])
        )

        patient["hr"] = max(
            101,
            min(120, patient["hr"])
        )

        patient["rr"] = max(
            21,
            min(28, patient["rr"])
        )

        if random.random() < (
            patient["recovery_chance"]
        ):

            patient["state"] = "Stable"

        elif random.random() < (
            patient["deterioration_chance"]
        ):

            patient["state"] = "Critical"

    # -----------------------------------
    # Critical state
    # -----------------------------------

    else:

        patient["spo2"] = max(
            80,
            min(89, patient["spo2"])
        )

        patient["hr"] = max(
            121,
            min(150, patient["hr"])
        )

        patient["rr"] = max(
            29,
            min(40, patient["rr"])
        )

        if random.random() < (
            patient["recovery_chance"]
        ):

            patient["state"] = "Warning"

    return patient

# -----------------------------------
# Continuous ICU Simulation
# -----------------------------------

while True:

    all_patients = []

    for bed, patient in patients.items():

        updated = evolve_patient(patient)

        pressure = random.randint(10, 30)

        tidal = random.randint(400, 650)

        fio2 = random.randint(21, 100)

        patient_record = {

            "Timestamp":
            datetime.now(),

            "Bed":
            bed,

            "Profile":
            updated["profile"],

            "Disease":
            updated["disease"],

            "SpO2":
            updated["spo2"],

            "HeartRate":
            updated["hr"],

            "RespiratoryRate":
            updated["rr"],

            "AirwayPressure":
            pressure,

            "TidalVolume":
            tidal,

            "FiO2":
            fio2,

            "RiskLevel":
            updated["state"]
        }

        all_patients.append(
            patient_record
        )

    df = pd.DataFrame(all_patients)

    file_exists = os.path.isfile(
        FILE_NAME
    )

    df.to_csv(
        FILE_NAME,
        mode='a',
        header=not file_exists,
        index=False
    )

    print(df)

    time.sleep(1)
    
    