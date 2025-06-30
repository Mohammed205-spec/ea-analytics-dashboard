# streamlit_app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="EA Analytics Dashboard", layout="wide")

# Title
st.title("Employee Attrition Analytics Dashboard")

# Load data
df = pd.read_csv("EA.csv")

# 1. Show dataset
st.header("Dataset Preview")
st.dataframe(df.head())

# 2. Attrition Rate
st.header("1️⃣ Attrition Rate")
attrition_rate = df['Attrition'].value_counts(normalize=True) * 100
st.write(attrition_rate)

# 3. Average Age & Income by Attrition
st.header("2️⃣ Average Age & Monthly Income by Attrition")
age_income = df.groupby('Attrition')[['Age', 'MonthlyIncome']].mean()
st.write(age_income)

# 4. Attrition by Department
st.header("3️⃣ Attrition by Department")
dept_counts = df.groupby(['Department', 'Attrition']).size().unstack()
st.bar_chart(dept_counts)

# 5. Attrition by Job Role
st.header("4️⃣ Attrition by Job Role")
role_counts = df.groupby(['JobRole', 'Attrition']).size().unstack()
st.bar_chart(role_counts)

# 6. Monthly Income Distribution
st.header("5️⃣ Monthly Income Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(df['MonthlyIncome'], bins=30, kde=True, ax=ax1)
ax1.set_title("Monthly Income Distribution")
st.pyplot(fig1)

# 7. Correlation Heatmap
st.header("6️⃣ Correlation Heatmap")
corr = df.corr(numeric_only=True)
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.heatmap(corr, cmap='coolwarm', annot=True, fmt=".2f", ax=ax2)
st.pyplot(fig2)

# 8. Monthly Income by Job Level
st.header("7️⃣ Monthly Income by Job Level")
fig3, ax3 = plt.subplots()
sns.boxplot(data=df, x='JobLevel', y='MonthlyIncome', ax=ax3)
ax3.set_title("Monthly Income by Job Level")
st.pyplot(fig3)

# 9. OverTime vs. Attrition
st.header("8️⃣ OverTime vs Attrition")
ot_attrition = df.groupby(['OverTime', 'Attrition']).size().unstack()
st.bar_chart(ot_attrition)

# 10. Work-Life Balance
st.header("9️⃣ Work-Life Balance Counts")
wlb_counts = df['WorkLifeBalance'].value_counts().sort_index()
st.bar_chart(wlb_counts)

# 11. Years at Company vs. Attrition
st.header("🔟 Years at Company vs Attrition")
years_attrition = df.groupby(['YearsAtCompany', 'Attrition']).size().unstack().fillna(0)
st.line_chart(years_attrition)

# Footer
st.write("---")
st.write("Dashboard by [Your Name]. Powered by Streamlit 🚀")
