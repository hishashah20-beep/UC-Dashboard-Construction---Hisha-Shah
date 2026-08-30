import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="UC Admit Rates by Campus", layout="centered")

st.title("UC Admit Rate by Campus")
st.write(
    "How did UC admit rates differ across the nine campuses for Bay Area "
    "high school applicants from years 2010 to 2025?"
)

@st.cache_data
def load_data():
    df = pd.read_csv("bay_area_modeling_table.csv", low_memory=False)
    return df

df = load_data()

# Only offer years that actually have per-campus data.
# Fall 2005-2009 only has "Universitywide" totals, no campus breakdown.
years = sorted(df[df.campus != "Universitywide"].fall_term.unique())
selected_year = st.selectbox("Fall term", years, index=years.index(2025))

y = df[(df.fall_term == selected_year) & (df.campus != "Universitywide")]

campus_summary = (
    y.groupby("campus")
     .apply(lambda g: pd.Series({
         "total_applicants": g.applicants.sum(),
         "total_admits": g.admits.sum(),
         "admit_rate": g.admits.sum() / g.applicants.sum()
     }))
     .reset_index()
     .sort_values("admit_rate")
)

st.subheader(f"Admit rate by campus, fall {selected_year}")
fig, ax = plt.subplots()
ax.barh(campus_summary.campus, campus_summary.admit_rate)
ax.set_xlabel("UC admit rate")
st.pyplot(fig)

st.subheader("Underlying numbers")
st.dataframe(campus_summary.set_index("campus"))
