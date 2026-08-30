# UC Dashboard Construction — Hisha

## Question

How did UC admit rates differ across the nine campuses for Bay Area high
school applicants from years 2010 to 2025?

- **Time window:** Fall 2010–2025 (user-selectable via dropdown in the dashboard, defaults to 2025). The underlying dataset has per-campus data back to 2005, but Fall 2005–2009 only has systemwide ("Universitywide") totals, not a per-campus breakdown, so those years are excluded from the dropdown and from this analysis.
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
6. Extended the dashboard beyond the single-year campus comparison with
   three additional views:
   - **School drill-in:** pick any individual Bay Area high school (from
     the selected year) and see its admit rate at each campus, plotted
     against the Bay Area-wide average per campus for reference.
   - **Trend over time:** a multi-select of campuses plotted as admit
     rate over every available fall term (2010–2025), so campus
     selectivity can be compared as a trend rather than a single
     snapshot.
   - **Demographic breakdown:** pick a campus and see admit rate by
     demographic group (African American, American Indian, Asian,
     Hispanic/Latinx, International, Pacific Islander, White, and
     domestic/unknown), summed the same way as the campus-level
     numbers (sum admits and applicants per group, then divide).
   - **Academic outcomes vs. admit rate:** pick a campus and see a
     scatter plot of each Bay Area high school's CAASPP mathematics
     mean score against that school's admit rate at the selected
     campus, with a trendline and a correlation coefficient (r).

## Findings

Admit rates vary dramatically by campus, with the same overall pattern
holding across most years we checked: Merced and Riverside are consistently
the least selective (often 80–95%+ admit rate), while Los Angeles and
Berkeley are consistently the most selective (often under 15%). This
reflects well-known, persistent differences in campus selectivity across
the UC system rather than a subtle statistical pattern, making it a clear,
visually distinct result even after aggregating a large and noisy dataset
across two decades.

The trend view shows this ranking has stayed fairly stable across 2010–2025
rather than campuses swapping places — selectivity differences between UC
campuses are persistent, not a one-year anomaly. The school drill-in shows
that any individual high school's admit rate at a given campus can deviate
noticeably from the Bay Area-wide average, especially for schools with a
small number of applicants to that campus in a given year.

The academic outcomes view shows only a weak relationship between a
school's CAASPP math scores and its admit rate at a given campus (for
example, r ≈ 0.2 at Berkeley) — meaning UC admit rate is driven by much
more than a school's aggregate test performance.

## Limitations

- Admit rate is a function of both selectivity *and* who chooses to apply;
  it doesn't capture yield, financial aid effects, or major-specific
  admission differences.
- Fall 2005–2009 is excluded entirely due to lack of per-campus granularity
  (see Time window above).
- Demographic subgroup counts (in the demographic breakdown view) do not
  always sum to the overall campus total. The source data suppresses small
  group counts for privacy, so some students aren't captured in any
  demographic category shown.

## Files

- `app.py` — Streamlit dashboard source code
- `requirements.txt` — Python dependencies for deployment
- `bay_area_modeling_table.csv` — dataset used
- `*.ipynb` — Colab notebook with the original analysis

## Run locally

```bash
git clone https://github.com/hishashah20-beep/UC-Dashboard-Construction---Hisha-Shah.git
cd UC-Dashboard-Construction---Hisha-Shah
pip install -r requirements.txt
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

## Live app

Deployed via Streamlit Community Cloud: https://uc-dashboard-construction---hisha-24qhqujecdftnodmwful9a.streamlit.app/
