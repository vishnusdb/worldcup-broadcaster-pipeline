# Live Broadcaster Engagement & Monetization Strategy Pipeline
### 2026 FIFA World Cup — End-to-End Data Analytics Project

This project builds a live data pipeline that tracks the 2026 FIFA World Cup and identifies which matches represent the highest-value advertising inventory for broadcasters — using Python, SQL, and Power BI.

Broadcasters sell advertising slots around live match coverage, and the price of those slots scales with expected viewership. Viewership, in turn, is driven by match stakes — elimination drama and especially **upsets**, where a lower-ranked team beats a strong favourite. This pipeline quantifies that signal in real time: it ingests live tournament data, calculates group standings, identifies upset matches using pre-tournament team strength ratings, and classifies every match into an advertising-value tier — turning raw football data into a broadcaster monetisation recommendation.

---

## What This Project Demonstrates

- **REST/public API data extraction** with Python (`requests`, `csv`, secure credential handling via `.env`)
- **SQL data engineering**: dimensional modelling, `UNION ALL` aggregations, multi-table `JOIN`s across three data sources, and `RANK() OVER` window functions
- **Business intelligence**: translating raw match data into a quantified ad-revenue recommendation framework
- **Data quality handling**: name standardisation across data sources, NULL handling, and type enforcement — all encountered and resolved as real engineering problems (see `queries.sql` for the full log)

---

## Tech Stack

| Layer | Tool |
|---|---|
| Extraction | Python (`requests`, `python-dotenv`) |
| Data Source | [openfootball/worldcup.json](https://github.com/openfootball/worldcup.json) (live match data) |
| Transformation | MySQL 8.0 / MySQL Workbench |
| Visualisation | Power BI |

---

## Pipeline Architecture

```
openfootball public JSON (live World Cup 2026 data)
     ↓  [Python: extract_matches.py]
matches.csv (raw, 104 fixtures)
     ↓  [MySQL: queries.sql — 8 SQL transformation stages]
team_groups · elo_ratings · matches_clean · team_match_stats
     ↓
group_standings · final_standings · high_engagement_matches
     ↓  [CSV export]
final_standings.csv + high_engagement_matches.csv
     ↓  [Power BI]
Broadcaster Optimization Dashboard
```

---

## Repository Structure

```
worldcup_pipeline/
├── extract_matches.py          # Python extraction script
├── queries.sql                 # All SQL: schema, transformations, and a
│                                #   documented log of every error encountered
│                                #   and how it was resolved
├── data/
│   ├── raw/
│   │   └── matches.csv         # Raw extracted fixtures
│   ├── processed/
│   │   ├── final_standings.csv         # Ranked group standings
│   │   └── high_engagement_matches.csv # Upset analysis + ad-slot tiers
│   └── reference/
│       └── elo_ratings_wc2026.csv      # Reference Elo data
└── README.md
```

---

## How to Run This Project

1. Clone the repository:
   ```bash
   git clone https://github.com/vishnusdb/worldcup-broadcaster-pipeline.git
   cd worldcup-broadcaster-pipeline
   ```

2. Install Python dependencies:
   ```bash
   pip3 install requests python-dotenv
   ```

3. Run the extraction script to pull the latest match data:
   ```bash
   python3 extract_matches.py
   ```

4. Open `queries.sql` in MySQL Workbench (or any MySQL 8.0+ client) and run it top to bottom against a fresh database to rebuild all transformation tables.

5. Export `final_standings` and `high_engagement_matches` as CSVs and load them into Power BI to rebuild the dashboard.

---

## Key Insight (as of June 2026)

Four confirmed upsets have been identified in the group stage so far, ranked by Elo gap (the larger the gap, the bigger the surprise):

| Match | Result | Elo Gap | Ad Slot Tier |
|---|---|---|---|
| South Korea vs Czech Republic | 2–1 | 247 | TIER 2 — High |
| Scotland vs Morocco | 0–1 | 180 | TIER 2 — High |
| Czech Republic vs Mexico | 0–3 | 177 | TIER 2 — High |
| Ecuador vs Germany | 2–1 | 120 | TIER 2 — High |

Ecuador's win over Germany stands out as the highest-profile shock relative to pre-tournament expectations, and under this model would justify a premium CPM recommendation on replay and highlight inventory for that match.

---

## Author

Vishnu Gautam — Mechanical Engineering student, building data analytics portfolio projects for Business/Product Analyst roles.
