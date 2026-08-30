# UC Dashboard Construction — Hisha

## Question

How did UC admit rates differ across the nine campuses for Bay Area high
school applicants in fall 2025?

- **Time window:** Fall 2025
- **Population:** Bay Area public high school applicants
- **Metric:** UC admit rate (admits ÷ applicants) by campus

## Dataset

`bay_area_modeling_table.csv` from the provided UC Admissions Data collection
(UC Information Center + California Department of Education, joined at the
school-year-campus level). Each row represents one high school, in one year,
at one UC campus.

## Method

1. Filtered the data to `fall_term == 2025`.
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

Admit rates varied dramatically by campus for fall 2025 Bay Area applicants,
ranging from under 12% at the most selective campuses (Los Angeles,
Berkeley) to over 89% at the least selective (Riverside, Merced). This
reflects well-known and consistent differences in campus selectivity across
the UC system, rather than a subtle statistical pattern — making it a clear,
visually distinct result even after aggregating a large and noisy dataset.

## Files

- `app.py` — Streamlit dashboard source code
- `requirements.txt` — Python dependencies for deployment
- `bay_area_modeling_table.csv` — dataset used
- `*.ipynb` — Colab notebook with the original analysis

## Live app

Deployed via Streamlit Community Cloud: *(paste your share.streamlit.io link here)*
