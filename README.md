# 🩺 Diabetic Patient Healthcare Analysis

A Streamlit-based data analysis and dashboard project exploring 100,000+ diabetic patient
hospital encounters across 130 US hospitals. Pure EDA + visualization + dashboard.
## Project Structure

```
diabetic_project/
├── app.py                  # Main Streamlit app (page logic only, no raw HTML)
├── mappings.py              # ID-to-label mappings and constants
├── style.py                  # All CSS/HTML lives here as helper functions
├── requirements.txt
├── .streamlit/config.toml   # Theme configuration
└── data/cleaned_diabetic_data.csv
```

`app.py` never contains raw HTML — it only calls functions like `hero()`, `kpi_card()`,
`section_title()`, and `insight()` which are defined in `style.py`.

## Setup

```
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501

## Pages

- Home — overview,  dataset 
- Exploratory Data Analysis — age, gender, race
- Hospital & Clinical Insights — admissions, hospital stay, diagnoses, correlations
- Medication Analysis — drug prescriptions and dosage changes
- Readmission Analysis — readmission patterns
- Interactive Dashboard — live filters,  

## Libraries

streamlit, pandas, numpy, matplotlib, seaborn
