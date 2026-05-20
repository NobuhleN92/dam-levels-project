# Data Quality Report — Dam Levels Project

**Dataset:** City of Cape Town — Dam Levels from 2000
**Source:** https://odp-cctegis.opendata.arcgis.com
**Prepared by:** Nobuhle Nkomo
**Date:** 2026-05-20

---

## 1. Dataset Overview

| Attribute | Value |
|-----------|-------|
| Raw rows | 9,526 |
| Raw columns | 64 |
| Date range | 2000-01-01 to 2026-01-29 |
| Dams covered | 14 |
| Staging rows (after reshape) | 124,262 |
| Mart fact rows | 124,262 |

---

## 2. Data Quality Checks

### 2.1 Completeness
| Column | Null Count | Action Taken |
|--------|-----------|--------------|
| current_pct | 0 | No action needed |
| storage_ml | 0 | No action needed |
| height_m | 0 | No action needed |
| big6_current_pct | 37,526 | Filled with 0 (dams not yet built) |
| dam_name | 0 | No action needed |
| date | 0 | No action needed |

### 2.2 Validity
| Check | Result |
|-------|--------|
| Date range valid (2000-2026) | ✅ PASS |
| current_pct between 0-100 | ✅ PASS |
| Row count > 100,000 | ✅ PASS |
| No nulls in key columns | ✅ PASS |

### 2.3 Consistency
| Check | Result |
|-------|--------|
| Date format consistent | ✅ Fixed (Sept → Sep) |
| Numeric columns stored as float64 | ✅ PASS |
| Boolean columns converted to int | ✅ PASS |
| All 14 dams present | ✅ PASS |

---

## 3. Transformations Applied

1. **Date parsing** — Fixed inconsistent month abbreviation (Sept → Sep)
2. **Wide to long reshape** — 64 columns reshaped into 14 dam records per date
3. **Null handling** — Rows where all measures null dropped (dams not yet built)
4. **Derived columns** — Added year, month, quarter, season
5. **Critical flags** — Added is_critical (< 20%) and is_day_zero (< 13.5%)
6. **Numeric conversion** — All measure columns forced to float64

---

## 4. Risks and Assumptions

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Data not updated since Jan 2026 | High | Medium | Monitoring alert configured |
| Some dams added after 2000 | Confirmed | Low | Null rows dropped cleanly |
| Big 6 nulls filled with 0 | Medium | Medium | Documented and flagged |

### Assumptions
- Day Zero threshold set at 13.5% (based on City of Cape Town official threshold)
- Critical level set at 20% (based on water restriction trigger levels)
- Southern Hemisphere seasons applied (Summer = Dec/Jan/Feb)
- Berg River and Land en Zeezicht dams only available from later years

---

## 5. Freshness & Completeness SLAs

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Data freshness | < 30 days old | 111 days | ⚠️ STALE |
| Row completeness | > 100,000 rows | 124,262 | ✅ PASS |
| Dam coverage | 14 dams | 14 dams | ✅ PASS |
| Date coverage | 2000-2026 | 2000-2026 | ✅ PASS |