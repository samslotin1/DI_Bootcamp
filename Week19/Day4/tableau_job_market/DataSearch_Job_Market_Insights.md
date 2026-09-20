# DataSearch job market insights

## Scope and preparation

The analysis uses **25,114** original job postings dated 2017–2021. Tableau calculations classify titles into **Data Science**, **Data Engineering**, **Analytics**, and **Other**; the focused scope contains **12,060** postings in the first three groups. Dates and numeric fields are typed in the Tableau data source, and blank pay values are deliberately retained as missing.

Skills are normalized into a separate one-row-per-skill summary. This prevents multiple skills embedded in a source cell from being treated as one category.

## Key findings

- **Analytics** is the largest data-role group, with **5,966 postings**.
- The leading named city market is **New York, NY** with **366 data-role postings**. National U.S. listings are excluded from this city ranking.
- **Internet** leads hiring demand with **2,612 data-role postings**.
- **SQL** is the most frequently requested skill, appearing in **5,481 postings**.
- Posting volume peaks in **2021** at **3,938 data-role postings**.

## Recommendations for DataSearch

1. Focus recruiter sourcing on the largest role group and reusable searches around SQL, Python, cloud/data platforms, and analytical tooling.
2. Prioritize the leading city and technology-heavy industries for employer outreach; keep national listings separate from local-market signals.
3. Use the trend view for recruiter-capacity planning and reassess skill demand quarterly.

## Tableau workbook

Open `DataSearch_Job_Market_Analysis.twbx` in Tableau Public. It contains an original dashboard with posting-trend, locations, industries, and in-demand-skills views, plus a Role mix worksheet. The workbook includes calculated fields for **Role Group**, **Data Role Scope**, and **Average Pay**.
