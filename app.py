import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Diabetic Patient Healthcare Analysis",
    page_icon="🩺",
    layout="wide"
)

# 1. Simple Data Load
@st.cache_data
def load_data():
    # FIXED PATH: Looking directly for the file on your main GitHub page
    df = pd.read_csv("cleaned_diabetic_data.csv")
    return df

df = load_data()

# 2. Simple Sidebar Navigation
st.sidebar.title("🩺 Navigation")
page = st.sidebar.selectbox(
    "Choose a Section",
    ["Home", "Exploratory Data Analysis", "Clinical Insights", "Interactive Dashboard"]
)

# 3. HOME PAGE
if page == "Home":
    st.title("Diabetic Patient Healthcare Analysis")
    st.write("Welcome to the diabetic patient data analysis dashboard. This app helps visualize and understand clinical trends.")
    
    # Basic Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", f"{len(df):,}")
    col2.metric("Avg Hospital Stay", f"{df['Hospital_Stay'].mean():.1f} days")
    col3.metric("Avg Medications", f"{df['Medications'].mean():.1f}")
    
    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

# 4. EDA PAGE (Charts)
elif page == "Exploratory Data Analysis":
    st.title("🔍 Exploratory Data Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gender Distribution")
        fig, ax = plt.subplots()
        df['gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=['#0F9D8C', '#38BDF8'])
        ax.set_ylabel('')
        st.pyplot(fig)
        
    with col2:
        st.subheader("Top Races in Dataset")
        st.bar_chart(df['race'].value_counts())

    st.subheader("Age Group Counts")
    st.bar_chart(df['age'].value_counts())

# 5. CLINICAL INSIGHTS PAGE
elif page == "Clinical Insights":
    st.title("🏥 Clinical Insights")
    
    st.subheader("Hospital Stay Duration Distribution")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(df['Hospital_Stay'], bins=15, color="#0F9D8C", kde=True, ax=ax)
    st.pyplot(fig)
    
    st.subheader("Correlation Map")
    # Selecting simple numbers to correlate
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(numeric_df.corr(), annot=True, cmap="crest", fmt=".2f", ax=ax)
    st.pyplot(fig)

# 6. INTERACTIVE DASHBOARD PAGE
elif page == "Interactive Dashboard":
    st.title("📊 Interactive Filters")
    
    # Easy filters without categorical issues
    gender_list = df['gender'].unique().tolist()
    selected_gender = st.multiselect("Select Gender", gender_list, default=gender_list)
    
    # Filter the data
    filtered_df = df[df['gender'].isin(selected_gender)]
    
    st.subheader("Filtered Data Snapshot")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # Simple metric for filtered count
    st.info(f"Showing {len(filtered_df)} records based on your selection.")
