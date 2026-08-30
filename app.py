import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- Page setup ----
st.set_page_config(
    page_title="UC Admit Rates by Campus",
    page_icon="🎓",
    layout="centered",
)

# ---- Shared chart style ----
ACCENT = "#4F8BF9"
AVG_COLOR = "#F97066"

plt.rcParams.update({
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "axes.edgecolor": "#3A3F4B",
    "axes.labelcolor": "#FAFAFA",
    "xtick.color": "#C9CDD3",
    "ytick.color": "#C9CDD3",
    "text.color": "#FAFAFA",
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 11,
})

st.title("🎓 UC Admit Rate by Campus")
st.markdown(
    "##### How did UC admit rates differ across the nine campuses for Bay Area "
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
selected_year = st.selectbox("📅 Fall term", years, index=years.index(2025))

y = df[(df.fall_term == selected_year) & (df.campus != "Universitywide")]

campus_summary = (
    y.groupby("campus")
     .agg(total_applicants=("applicants", "sum"),
          total_admits=("admits", "sum"))
     .assign(admit_rate=lambda d: d.total_admits / d.total_applicants)
     .reset_index()
     .sort_values("admit_rate")
)

# ---- Headline metric cards ----
most_selective = campus_summary.iloc[0]
least_selective = campus_summary.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Most selective", most_selective.campus, f"{most_selective.admit_rate * 100:.1f}%")
col2.metric("Least selective", least_selective.campus, f"{least_selective.admit_rate * 100:.1f}%")
col3.metric("Total Bay Area applicants", f"{int(campus_summary.total_applicants.sum()):,}")

st.divider()
st.subheader(f"📊 Admit rate by campus, fall {selected_year}")
fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.barh(campus_summary.campus, campus_summary.admit_rate, color=ACCENT)
ax.set_xlabel("UC admit rate")
ax.bar_label(bars, labels=[f"{v*100:.1f}%" for v in campus_summary.admit_rate],
             padding=4, color="#FAFAFA", fontsize=9)
st.pyplot(fig)

st.subheader("🔢 Underlying numbers")
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
st.subheader("🏫 Drill into a specific high school")

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

fig2, ax2 = plt.subplots(figsize=(7, 4.5))
ax2.barh(school_summary.campus, school_summary.admit_rate, color=ACCENT, label=selected_school)

# Overlay the Bay Area-wide average per campus as reference marks
for _, row in campus_summary.iterrows():
    y_pos = school_summary.campus.tolist().index(row.campus) if row.campus in school_summary.campus.values else None
    if y_pos is not None:
        ax2.scatter(row.admit_rate, y_pos, color=AVG_COLOR, zorder=3, s=60,
                    label="Bay Area avg" if y_pos == 0 else None)

ax2.set_xlabel("Admit rate")
ax2.set_title(f"{selected_school} vs. Bay Area average, fall {selected_year}", fontsize=11)
ax2.legend(frameon=False)
st.pyplot(fig2)

st.dataframe(
    school_summary.set_index("campus").assign(
        admit_rate=lambda d: (d.admit_rate * 100)
    ),
    column_config={
        "admit_rate": st.column_config.NumberColumn("admit_rate", format="%.1f%%")
    },
)

st.divider()
st.subheader("📈 Admit rate trend over time")

all_campuses = sorted(df[df.campus != "Universitywide"].campus.unique())
selected_campuses = st.multiselect(
    "Campuses to show", all_campuses, default=all_campuses
)

trend_data = df[(df.campus != "Universitywide") & (df.campus.isin(selected_campuses))].copy()
trend_data["admits"] = trend_data["admits"].fillna(0)

trend_summary = (
    trend_data.groupby(["fall_term", "campus"])
    .agg(total_applicants=("applicants", "sum"),
         total_admits=("admits", "sum"))
    .assign(admit_rate=lambda d: d.total_admits / d.total_applicants)
    .reset_index()
)

palette = plt.cm.viridis
n = max(len(selected_campuses), 1)

fig3, ax3 = plt.subplots(figsize=(7, 4.5))
for i, campus in enumerate(selected_campuses):
    campus_trend = trend_summary[trend_summary.campus == campus].sort_values("fall_term")
    ax3.plot(campus_trend.fall_term, campus_trend.admit_rate,
              marker="o", markersize=4, linewidth=2,
              color=palette(i / max(n - 1, 1)), label=campus)

ax3.set_xlabel("Fall term")
ax3.set_ylabel("UC admit rate")
ax3.set_title("Admit rate by campus, 2010–2025", fontsize=11)
ax3.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize="small", frameon=False)
st.pyplot(fig3, use_container_width=True)

st.divider()
st.subheader("🧑‍🤝‍🧑 Admit rate by demographic group")

DEMO_GROUPS = {
    "African American": ("adm_african_american", "app_african_american"),
    "American Indian": ("adm_american_indian", "app_american_indian"),
    "Asian": ("adm_asian", "app_asian"),
    "Hispanic/Latinx": ("adm_hispanic_latinx", "app_hispanic_latinx"),
    "International": ("adm_int_l", "app_int_l"),
    "Pacific Islander": ("adm_pacific_islander", "app_pacific_islander"),
    "White": ("adm_white", "app_white"),
    "Domestic, unknown": ("adm_domestic_unknown", "app_domestic_unknown"),
}

demo_campus = st.selectbox("Campus", sorted(y.campus.unique()), key="demo_campus")
demo_data = y[y.campus == demo_campus]

demo_rows = []
for group, (adm_col, app_col) in DEMO_GROUPS.items():
    total_adm = demo_data[adm_col].sum()
    total_app = demo_data[app_col].sum()
    if total_app > 0:
        demo_rows.append({
            "group": group,
            "total_applicants": total_app,
            "total_admits": total_adm,
            "admit_rate": total_adm / total_app,
        })

demo_summary = pd.DataFrame(demo_rows).sort_values("admit_rate")

fig4, ax4 = plt.subplots(figsize=(7, 4.5))
bars4 = ax4.barh(demo_summary.group, demo_summary.admit_rate, color=ACCENT)
ax4.set_xlabel("Admit rate")
ax4.set_title(f"{demo_campus} — admit rate by demographic group, fall {selected_year}", fontsize=11)
ax4.bar_label(bars4, labels=[f"{v*100:.1f}%" for v in demo_summary.admit_rate],
              padding=4, color="#FAFAFA", fontsize=9)
st.pyplot(fig4)

st.dataframe(
    demo_summary.set_index("group").assign(
        admit_rate=lambda d: (d.admit_rate * 100)
    ),
    column_config={
        "admit_rate": st.column_config.NumberColumn("admit_rate", format="%.1f%%")
    },
)

st.caption(
    "Demographic subgroup counts may not sum to the overall campus total — "
    "the source data suppresses small group counts for privacy, so some "
    "students aren't captured in any demographic category above."
)

st.divider()
st.subheader("📐 Academic outcomes vs. admit rate")

outcome_campus = st.selectbox("Campus", sorted(y.campus.unique()), key="outcome_campus")
outcome_data = y[y.campus == outcome_campus].copy()
outcome_data["admits"] = outcome_data["admits"].fillna(0)

outcome_summary = (
    outcome_data.groupby("high_school")
    .agg(
        total_applicants=("applicants", "sum"),
        total_admits=("admits", "sum"),
        math_score=("caaspp_mathematics_mean_score", "mean"),
    )
    .assign(admit_rate=lambda d: d.total_admits / d.total_applicants)
    .dropna(subset=["math_score"])
    .reset_index()
)

if len(outcome_summary) >= 2:
    corr = np.corrcoef(outcome_summary.math_score, outcome_summary.admit_rate)[0, 1]
    slope, intercept = np.polyfit(outcome_summary.math_score, outcome_summary.admit_rate, 1)

    fig5, ax5 = plt.subplots(figsize=(7, 4.5))
    ax5.scatter(outcome_summary.math_score, outcome_summary.admit_rate,
                color=ACCENT, alpha=0.7, s=40)

    x_line = np.linspace(outcome_summary.math_score.min(), outcome_summary.math_score.max(), 50)
    ax5.plot(x_line, slope * x_line + intercept, color=AVG_COLOR, linewidth=2,
              label=f"Trend (r = {corr:.2f})")

    ax5.set_xlabel("School's CAASPP math mean score")
    ax5.set_ylabel("Admit rate at this campus")
    ax5.set_title(f"{outcome_campus} — school math scores vs. admit rate, fall {selected_year}", fontsize=11)
    ax5.legend(frameon=False)
    st.pyplot(fig5)

    st.caption(
        f"Correlation coefficient r = {corr:.2f} across {len(outcome_summary)} schools "
        f"with available CAASPP math data. r close to 0 means little relationship; "
        f"closer to 1 or -1 means a stronger positive or negative relationship."
    )
else:
    st.info("Not enough schools with CAASPP math data for this campus/year to plot a trend.")

st.caption("Built for the UC Dashboard Construction hackathon project · Data: UC Information Center + California Department of Education")
