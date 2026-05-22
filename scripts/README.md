# Cape Town Dam Levels Analytics
## E10 Assessment — Production-Style Analytics Product

**Student:** Nobuhle Nkomo
**Dataset:** City of Cape Town — Dam Levels from 2000
**Source:** https://odp-cctegis.opendata.arcgis.com
**Date:** May 2026

---

## Project Story
> *"How have Cape Town's dam levels changed over 25 years, and how close did the city come to Day Zero in 2018?"*

---

## Project Structure

dam_levels_project/
├── data/
│   ├── raw/          # Original source CSV
│   ├── staging/      # Cleaned and reshaped data
│   └── mart/         # Star schema tables
├── docs/
│   ├── data_quality_report.md
│   ├── accessibility_checklist.md
│   ├── postmortem.md
│   └── monitoring_log.txt
├── powerbi/
│   ├── 01_Development.pbix  # Dev environment
│   ├── 02_Test.pbix         # Test environment
│   └── 03_Production.pbix   # Production environment
├── screenshots/
│   ├── dev/
│   ├── test/
│   └── prod/
├── scripts/
│   ├── ingest_staging.py    # Incremental ingestion
│   ├── build_mart.py        # Star schema builder
│   └── monitoring.py        # Monitoring and alerts
├── promotion_log.md
└── README.md

## How to Run

### Prerequisites
-Python 3.13+
-pandas
-openpyxl

### Install dependencies
```bash
pip install pandas openpyxl

Step 1 — Run incremental ingestion
Bash: python scripts/ingest_staging.py

Step 2 — Build star schema mart
Bash: python scripts/build_mart.py

Step 3 — Run monitoring
Bash: python scripts/monitoring.py

### Data Pipeline
RAW CSV  → ingest_staging.py → staging_layer → build_mart.py → mart layer → Power BI

### Layers

| Layer   || Location  || Description    |
-------------------------------------------
|Raw      | data/raw/  || Original source data - never modified|
|Staging  | data/staging/|| Cleaned, reshaped, 124,262 rows    |
|Mart     | data/mart/ || Star schema - fact + 2 dimensions    | 


### Star Schema
Fact Table: fact_dam_levels
   - date_key (FK → dim_date)
   - dam_key (FK → dim_dam)
   - height_m, storage_ml, current_pct, last_year_pct
   - big6_storage_ml, big6_current_pct
   - is_critical, is_day_zero

### Dimensions:
   - dim_date — date, year, month, quarter, season
   - dim_dam — dam_name, catchment, capacity_ml, is_big6

### Deployment Pipeline
|Environment  || File               || Data Source  |
-----------------------------------------------------
|Development  ||01_Development.pbix ||data/mart/    |
|Test         ||02_Test.pbix        ||data/staging/ |
|Production   ||03_Production.pbix  ||data/mart/    |

### Validation Checks (Test Environment)

|Check                               || Result        |
----------------------------------------------------
|RowCountCheck — rows > 100,000      ||✅ PASS       |
|NullCheck — no nulls in current_pct ||✅ PASS       |
|CriticalLevelCheck — values 0-100   ||✅ PASS       |

### Service Level Definitions

|Metric         ||Target             ||Status      |
----------------------------------------------------
|Data freshness ||< 30 days          ||⚠️ 111 days |
|Row count      ||> 100,000          ||✅ 124,262  |
|Pipeline uptime||All 3 pbix present ||✅          |


## Key Insights

  - Big 6 dam levels dropped to critical levels during the 2017-2018 Day Zero crisis
  - Spring has the highest average dam levels due to Winter rainfall filling dams
  - Theewaterskloof is the largest dam accounting for the majority of Big 6 storage
  - Berg River and Land en Zeezicht were added to the system after 2000


## Accessibility

All Power BI visuals include alt text following Microsoft accessibility guidance.
See docs/accessibility_checklist.md for full compliance report.

## Git Commit History

[PROD] ROLLBACK - data freshness alert triggered
[PROD] Promoted from Test - production ready
[TEST] Promoted from Dev - validation checks added
[DEV] Initial build - raw data ingested
