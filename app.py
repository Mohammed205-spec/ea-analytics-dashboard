# streamlit_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- Page config ---
st.set_page_config(page_title="EA Interactive Dashboard", layout="wide")

# --- Load data ---
df = pd.read_csv("EA.csv")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Data")

# Toggle to show raw data
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("📄 Raw Dataset")
    st.dataframe(df)

# Department filter
departments = df['Department'].unique()
selected_departments = st.sidebar.multiselect("Department:", departments, default=departments)

# Job Role filter
job_roles = df['JobRole'].unique()
selected_roles = st.sidebar.multiselect("Job Role:", job_roles, default=job_roles)

# OverTime filter
overtime_opts = df['OverTime'].unique()
selected_overtime = st.sidebar.multiselect("OverTime:", overtime_opts, default=overtime_opts)

# Age slider
age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Age Range:", age_min, age_max, (age_min, age_max))

# Monthly Income slider
income_min, income_max = int(df['MonthlyIncome'].min()), int(df['MonthlyIncome'].max())
income_range = st.sidebar.slider("Monthly Income Range:", income_min, income_max, (income_min, income_max))

# --- Filter data based on selections ---
df_filtered = df[
    (df['Department'].isin(selected_departments)) &
    (df['JobRole'].isin(selected_roles)) &
    (df['OverTime'].isin(selected_overtime)) &
    (df['Age'].between(*age_range)) &
    (df['MonthlyIncome'].between(*income_range))
]

st.sidebar.write(f"✅ Rows after filter: {df_filtered.shape[0]}")

# --- Tabs for better navigation ---
tab1, tab2, tab3 = st.tabs(["📊 KPIs", "📈 Charts", "🗃️ Details"])

# --- Tab 1: KPIs ---
with tab1:
    st.header("📊 Key Metrics")
    col1, col2, col3 = st.columns(3)

    attrition_rate = df_filtered['Attrition'].value_counts(normalize=True) * 100
    col1.metric("Attrition Rate (%)", f"{attrition_rate.get('Yes',0):.2f}%")
    col2.metric("Avg Age", f"{df_filtered['Age'].mean():.1f} yrs")
    col3.metric("Avg Monthly Income", f"${df_filtered['MonthlyIncome'].mean():,.2f}")

# --- Tab 2: Charts ---
with tab2:
    st.header("📈 Visual Analytics")

    st.subheader("Attrition by Department")
    dept_counts = df_filtered.groupby(['Department', 'Attrition']).size().unstack().fillna(0)
    st.bar_chart(dept_counts)

    st.subheader("Attrition by Job Role")
    role_counts = df_filtered.groupby(['JobRole', 'Attrition']).size().unstack().fillna(0)
    st.bar_chart(role_counts)

    st.subheader("Monthly Income Distribution")
    fig1, ax1 = plt.subplots()
    sns.histplot(df_filtered['MonthlyIncome'], bins=30, kde=True, ax=ax1)
    ax1.set_title("Monthly Income Distribution")
    st.pyplot(fig1)

    st.subheader("Correlation Heatmap")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.heatmap(df_filtered.corr(numeric_only=True), cmap='coolwarm', annot=True, fmt=".2f", ax=ax2)
    st.pyplot(fig2)

    st.subheader("Monthly Income by Job Level")
    fig3, ax3 = plt.subplots()
    sns.boxplot(data=df_filtered, x='JobLevel', y='MonthlyIncome', ax=ax3)
    ax3.set_title("Monthly Income by Job Level")
    st.pyplot(fig3)

    st.subheader("OverTime vs Attrition")
    ot_attrition = df_filtered.groupby(['OverTime', 'Attrition']).size().unstack().fillna(0)
    st.bar_chart(ot_attrition)

    st.subheader("Work-Life Balance Counts")
    wlb_counts = df_filtered['WorkLifeBalance'].value_counts().sort_index()
    st.bar_chart(wlb_counts)

    st.subheader("Years at Company vs Attrition")
    years_attrition = df_filtered.groupby(['YearsAtCompany', 'Attrition']).size().unstack().fillna(0)
    st.line_chart(years_attrition)

# --- Tab 3: Details ---
with tab3:
    st.header("🗃️ Filtered Data Details")
    st.dataframe(df_filtered)

# --- Footer ---
st.write("---")
st.write("🎉 Interactive Dashboard by [Your Name]. Powered by Streamlit 🚀")
