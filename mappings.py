ADMISSION_TYPE = {
    1: "Emergency",
    2: "Urgent",
    3: "Elective",
    4: "Newborn",
    5: "Not Available",
    6: "Not Mapped/NULL",
    7: "Trauma Center",
    8: "Unknown",
}

DISCHARGE_DISPOSITION = {
    1: "Discharged to Home",
    2: "Transferred to Another Hospital",
    3: "Transferred to SNF",
    4: "Transferred to ICF",
    5: "Transferred to Other Inpatient Care",
    6: "Home Health Service",
    7: "Left Against Medical Advice",
    8: "Home Under Home IV Provider",
    9: "Admitted as Inpatient",
    10: "Neonate to Another Hospital",
    11: "Expired",
    12: "Still Patient/Outpatient Expected",
    13: "Hospice / Home",
    14: "Hospice / Medical Facility",
    15: "Medicare Swing Bed",
    16: "Transferred for Outpatient Services",
    17: "Referred for Outpatient Services",
    18: "Not Mapped/NULL",
    19: "Expired at Home (Hospice)",
    20: "Expired in Medical Facility (Hospice)",
    21: "Expired, Place Unknown (Hospice)",
    22: "Transferred to Rehab Facility",
    23: "Transferred to Long Term Care Hospital",
    24: "Transferred to Nursing Facility (Medicaid)",
    25: "Not Mapped",
    26: "Unknown/Invalid",
    27: "Transferred to Federal Health Facility",
    28: "Transferred to Psychiatric Hospital",
    29: "Transferred to Critical Access Hospital",
    30: "Transferred to Other Health Institution",
}

ADMISSION_SOURCE = {
    1: "Physician Referral",
    2: "Clinic Referral",
    3: "HMO Referral",
    4: "Transfer from Hospital",
    5: "Transfer from SNF",
    6: "Transfer from Health Facility",
    7: "Emergency Room",
    8: "Court/Law Enforcement",
    9: "Not Available",
    10: "Transfer from Critical Access Hospital",
    11: "Normal Delivery",
    12: "Premature Delivery",
    13: "Sick Baby",
    14: "Extramural Birth",
    15: "Not Available",
    17: "Unknown",
    18: "Transfer from Home Health Agency",
    19: "Readmission to Same Home Health Agency",
    20: "Unknown",
    21: "Unknown/Invalid",
    22: "Transfer from Hospital Inpatient",
    23: "Born Inside this Hospital",
    24: "Born Outside this Hospital",
    25: "Transfer from Ambulatory Surgery Center",
    26: "Transfer from Hospice",
}

AGE_ORDER = [
    "[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)",
    "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)",
]

MEDICATION_COLUMNS = [
    "metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride",
    "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone",
    "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide",
    "examide", "citoglipton", "insulin", "glyburide-metformin",
    "glipizide-metformin", "glimepiride-pioglitazone",
    "metformin-rosiglitazone", "metformin-pioglitazone",
]

READMIT_ORDER = ["NO", ">30", "<30"]

READMIT_LABELS = {
    "NO": "Not Readmitted",
    ">30": "Readmitted after 30 Days",
    "<30": "Readmitted within 30 Days",
}
