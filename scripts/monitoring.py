import os 
import datetime

#------Files to monitor-----------------------------------------------------------------------------
file_to_monitor = {
    "dev"  : "powerbi/01_Development.pbix",
    "test" : "powerbi/02_Test.pbix",
    "prod" : "powerbi/03_Production.pbix"
}

data_files = {
    "raw"     : "data/raw/dam_levels_from_2000.csv",
    "staging" : "data/staging/dam_levels_staging.csv",
    "mart"    : "data/mart/fact_dam_levels.xlsx"
}

LOG_PATH = "docs/monitoring_log.txt"
os.makedirs("docs", exist_ok=True)

print("=" * 55)
print("MONITORING SCRIPT - Dam Levels Project")
print(f"Run time: {datetime.datetime.now()}")
print("=" * 55)

alerts = []

#-----Check Power BI files--------------------------------------------------------------------------
print("\n--Power BI Environment Files--")
for env, path in file_to_monitor.items():
    if os.path.exists(path):
        size = os.path.getsize(path)
        modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        age_days = (datetime.datetime.now() - modified_time).days
        status = "✅ OK" if age_days <= 7 else "⚠️STALE"
        if age_days > 7:
            alerts.append(f"⚠️ALERT: {env} file not updated in{age_days} days")
        print(f"   [{env.upper()}] {path}")
        mod_str = modified_time.strftime("%Y-%m-%d %H:%M") if modified_time else "Unknown"
        print(f"      Size: {size:,} bytes | Last Modified: {mod_str} | Status: {status}")
    else:
        print(f"   [{env.upper()}] ❌ MISSING: {path}")
        alerts.append(f"❌ALERT: {env} Power BI file is MISSING")  

# ── Data freshness check ───────────────────────────────────────────────────
print("\n── Freshness Check ──")
import pandas as pd
try:
    df = pd.read_csv("data/staging/dam_levels_staging.csv")
    df['date'] = pd.to_datetime(df['date'])
    latest = df['date'].max()
    days_old = (datetime.datetime.now() - latest).days
    if days_old > 30:
        status = "⚠️ STALE"
        alerts.append(f"ALERT: Data is {days_old} days old — may need refresh")
    else:
        status = "✅ FRESH"
    print(f" Latest data date : {latest.date()}")
    print(f" Days since update: {days_old}")
    print(f" Freshness status : {status}")
except Exception as e:
    print(f" ❌ Could not check freshness: {e}")

# ── Row count check ────────────────────────────────────────────────────────
print("\n── Row Count Check ──")
try:
    row_count = len(df)
    status = "✅ PASS" if row_count > 100000 else "❌ FAIL"
    print(f" Staging rows: {row_count:,} — {status}")
    if row_count <= 100000:
        alerts.append(f"ALERT: Staging row count {row_count} below threshold")
except Exception as e:
    print(f" ❌ Could not check row count: {e}")

# ── Alerts summary ─────────────────────────────────────────────────────────
print("\n── Alerts Summary ──")
if alerts:
    for alert in alerts:
        print(f" ⚠️ {alert}")
else:
    print(" ✅ No alerts — all systems healthy")

# ── Save log ───────────────────────────────────────────────────────────────
with open(LOG_PATH, "a") as f:
    f.write(f"\n{'='*55}\n")
    f.write(f"Run: {datetime.datetime.now()}\n")
    if alerts:
        for alert in alerts:
            f.write(f" {alert}\n")
    else:
        f.write(" No alerts\n")

print(f"\n── Log saved to {LOG_PATH}")
print("\n✅ Monitoring complete.")  
        