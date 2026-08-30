# UC Dashboard Construction — Hisha

## Question

How did UC admit rates differ across the nine campuses for Bay Area high
school applicants from years 2010 to 2025?

- **Time window:** Fall 2010–2025 (user-selectable via dropdown in the dashboard). Fall 2005–2009 only has systemwide ("Universitywide") totals in this dataset, not a per-campus breakdown, so those years are excluded from the dropdown.
- **Population:** Bay Area public high school applicants
- **Metric:** UC admit rate (admits ÷ applicants) by campus

## Dataset

`bay_area_modeling_table.csv` from the provided UC Admissions Data collection
(UC Information Center + California Department of Education, joined at the
school-year-campus level). Each row represents one high school, in one year,
at one UC campus. Applicant/admit/enrollee counts are available for every
year from 2005 to 2025.

## Method

1. Let the user pick a fall term via a dropdown (defaults to 2025).
2. Excluded rows where `campus == "Universitywide"`. That row counts distinct
   *students* admitted to at least one UC campus, not application counts per
   campus, so including it would double-count and distort the comparison.
3. Grouped the remaining rows by `campus`.
4. **Summed** `applicants` and `admits` within each campus group first, then
   divided total admits by total applicants to get one admit rate per campus.
   We did not average the per-school `admit_rate` column directly, since
   that would give small schools the same weight as large ones and skew
   the result.
5. Sorted campuses by admit rate and visualized the comparison as a bar
   chart, both in a Google Colab notebook (`.ipynb` file in this repo) and
   as an interactive Streamlit dashboard (`app.py`), where the year can be
   changed via a dropdown.

## Findings

Admit rates vary dramatically by campus, with the same overall pattern
holding across most years we checked: Merced and Riverside are consistently
the least selective (often 80–95%+ admit rate), while Los Angeles and
Berkeley are consistently the most selective (often under 15%). This
reflects well-known, persistent differences in campus selectivity across
the UC system rather than a subtle statistical pattern, making it a clear,
visually distinct result even after aggregating a large and noisy dataset
across two decades.

## Files

- `app.py` — Streamlit dashboard source code
- `requirements.txt` — Python dependencies for deployment
- `bay_area_modeling_table.csv` — dataset used
- `*.ipynb` — Colab notebook with the original analysis

## Live app

Deployed via Streamlit Community Cloud: *(https://uc-dashboard-construction---hisha-24qhqujecdftnodmwful9a.streamlit.app/)*
