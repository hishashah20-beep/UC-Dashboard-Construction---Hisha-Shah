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
     .agg(total_applicants=("applicants", "sum"),
          total_admits=("admits", "sum"))
     .assign(admit_rate=lambda d: d.total_admits / d.total_applicants)
     .reset_index()
     .sort_values("admit_rate")
)

st.subheader(f"Admit rate by campus, fall {selected_year}")
fig, ax = plt.subplots()
ax.barh(campus_summary.campus, campus_summary.admit_rate)
ax.set_xlabel("UC admit rate")
st.pyplot(fig)

st.subheader("Underlying numbers")
display_summary = campus_summary.set_index("campus").copy()
display_summary["admit_rate"] = display_summary["admit_rate"] * 100

st.dataframe(
    display_summary,
    column_config={
        "admit_rate": st.column_config.NumberColumn(
            "admit_rate",
            format="%.1f%%",
        )
    },
)

st.divider()
st.subheader("Drill into a specific high school")

# Get schools available in the selected year (same filter as campus_summary)
schools = sorted(y.high_school.dropna().unique())
selected_school = st.selectbox("High school", schools)

school_data = y[y.high_school == selected_school].copy()
school_data["admits"] = school_data["admits"].fillna(0)

school_summary = (
    school_data.groupby("campus")
    .agg(total_applicants=("applicants", "sum"),
         total_admits=("admits", "sum"))
    .assign(admit_rate=lambda d: d.total_admits / d.total_applicants)
    .reset_index()
    .sort_values("admit_rate")
)

fig2, ax2 = plt.subplots()
ax2.barh(school_summary.campus, school_summary.admit_rate, label=selected_school)

# Overlay the Bay Area-wide average per campus as reference marks
for _, row in campus_summary.iterrows():
    y_pos = school_summary.campus.tolist().index(row.campus) if row.campus in school_summary.campus.values else None
    if y_pos is not None:
        ax2.scatter(row.admit_rate, y_pos, color="red", zorder=3,
                    label="Bay Area avg" if y_pos == 0 else None)

ax2.set_xlabel("Admit rate")
ax2.set_title(f"{selected_school} — admit rate by campus, fall {selected_year}")
ax2.legend()
st.pyplot(fig2)

st.dataframe(
    school_summary.set_index("campus").assign(
        admit_rate=lambda d: (d.admit_rate * 100)
    ),
    column_config={
        "admit_rate": st.column_config.NumberColumn("admit_rate", format="%.1f%%")
    },
)
