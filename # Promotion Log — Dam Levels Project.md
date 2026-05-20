# Promotion Log — Dam Levels Project

## Promotion 1: Dev → Test
**Date:** 2026-05-20

**Changes Implemented:**
- Loaded raw dam levels data into staging layer
- Reshaped data from wide to long format (14 dams)
- Added derived date columns (year, month, quarter, season)
- Added critical level flags (is_critical, is_day_zero)
- Added 3 validation checks (RowCountCheck, NullCheck, CriticalLevelCheck)

**Evidence:**
- Screenshot of staging data source settings
- Screenshot of validation checks showing PASS
- Screenshot of Test model view

**Validation Results:**
- RowCountCheck: 124,262 rows — PASS
- NullCheck: No null values in current_pct — PASS
- CriticalLevelCheck: All values between 0-100 — PASS

**Promoted by:** Nobuhle Nkomo
**Status:** ✅ SUCCESS

---

## Promotion 2: Test → Production
**Date:** 2026-05-20

**Changes Implemented:**
- Switched data source from staging to mart layer
- Built star schema (fact_dam_levels, dim_date, dim_dam)
- Created polished Executive Summary page
- Added Drill-Down 1: By Dam
- Added Drill-Down 2: By Season
- Applied professional theme and titles

**Evidence:**
- Screenshot of Production data source settings
- Screenshot of Production model view
- Screenshot of Executive Summary page
- Screenshot of By Dam drill-down
- Screenshot of By Season drill-down

**Promoted by:** Nobuhle Nkomo
**Status:** ✅ SUCCESS

---

## Rollback Simulation
**Date:** 2026-05-20

**Problem Identified:**
Monitoring script detected data freshness alert — staging data is 111 days old
(latest date: 2026-01-29). Production report showing stale Big 6 percentages.

**Rollback Steps:**
1. Identified issue via monitoring_log.txt alert
2. Rolled back Production to previous stable version (02_Test.pbix)
3. Investigated root cause — source dataset not updated since January 2026
4. Fix implemented — added freshness threshold alert to monitoring.py
5. Re-promoted to Production after confirming alert system working

**Evidence:**
- Screenshot of monitoring alert (STALE warning)
- Screenshot of monitoring_log.txt

**Status:** ✅ RESOLVED

---

## Service Level Definitions

| Metric | Target | Current Status |
|--------|--------|----------------|
| Data freshness | Updated within 30 days | ⚠️ 111 days old |
| Row count | > 100,000 rows | ✅ 124,262 rows |
| Pipeline uptime | All 3 pbix files present | ✅ All present |
| Null values | 0 nulls in key columns | ✅ PASS |