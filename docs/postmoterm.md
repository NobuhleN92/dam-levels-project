# Blameless Postmortem Report
**Incident:** Data Freshness Alert — Production Report Showing Stale Data
**Date:** 2026-05-20
**Severity:** Medium
**Status:** Resolved
---
## Summary
The production monitoring script detected that dam levels data was 111 days old (latest date: 2026-01-29), exceeding the 30-day freshness SLA. This caused the Production report to display outdated Big 6 percentages.
---
## Timeline
| Time | Event |
|------|-------|
|03:22 | Monitoring script run — STALE alert triggered |
|03:25 | Alert logged to `docs/monitoring_log.txt` |
|03:30 | Investigation started — root cause identified |
|03:40 | Rollback to `02_Test.pbix` initiated |
|03:50 | Fix implemented in `monitoring.py` |
|04:00 | Re-promoted to Production — incident resolved |
---
## Root Cause
The source dataset (`Dam_Levels_from_2000.csv`) from the City of Cape Town Open Data Portal had not been updated since January 2026. The monitoring script did not have a freshness threshold alert configured at the time of initial deployment.
---
## Impact
-Production report showing Big 6 level data that was 111 days old
-No incorrect data was displayed — data was valid but stale
-No users were misled as the issue was caught by monitoring before any presentation
---
## Resolution1. 
1.Identified issue via `monitoring_log.txt`
2.Rolled back Production to `02_Test.pbix` as stable fallback
3.Investigated root cause — upstream data source not refreshed
4.Added freshness threshold alert to `monitoring.py` (threshold: 30 days)
5.Re-promoted fixed version to `03_Production.pbix`
6.Confirmed monitoring alert working correctly
---
## What Went Well
-Monitoring script detected the issue automatically
-Alert was logged clearly in `monitoring_log.txt`
-Rollback process was straightforward and documented- No data corruption occurred
---
## What Could Be Improved- 
-Set up automated data refresh from source portal
-Add email notification when freshness alert triggers
-Define escalation path for data quality incidents
---
## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| Schedule monthly data refresh reminder | Nobuhle Nkomo | 2026-06-01 |
| Add email alert to monitoring script | Nobuhle Nkomo | 2026-06-01 |
| Document data refresh procedure | Nobuhle Nkomo | 2026-06-01 |
---
## Blameless Statement
This incident was caused by an upstream data source limitation, not by any individual error. The monitoring system worked as intended by detecting and alerting on the issue. All team members responded promptly and professionally.