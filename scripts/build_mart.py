import pandas as pd
import os

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_PATH = 'data/staging/dam_levels_staging.csv'
MART_PATH = 'data/mart/'

os.makedirs(MART_PATH, exist_ok=True)

print("=" * 55)
print("STEP 3 — MART LAYER: Star Schema")
print("=" * 55)

# 1. Load staging data
df = pd.read_csv(STAGING_PATH)
df['date'] = pd.to_datetime(df['date'])
print(f"\n[1] Staging rows loaded : {len(df):,}")

# ── dim_date ───────────────────────────────────────────────────────────────
print("\n[2] Building dim_date...")
dim_date = df[['date', 'year', 'month', 'month_name', 'quarter', 'season']].drop_duplicates()
dim_date = dim_date.sort_values('date').reset_index(drop=True)
dim_date['date_key'] = dim_date.index + 1
dim_date.to_excel(MART_PATH + 'dim_date.xlsx', index=False)
print(f" Rows: {len(dim_date):,}")

# ── dim_dam ────────────────────────────────────────────────────────────────
print("\n[3] Building dim_dam...")
dim_dam = pd.DataFrame({
    'dam_name' : ['Wemmershoek', 'Steenbras Lower', 'Steenbras Upper',
                     'Voelvlei', 'Hely-Hutchinson', 'Woodhead',
                     'Victoria', 'Alexandra', 'De Villiers',
                     'Kleinplaats', 'Lewis Gay', 'Theewaterskloof',
                     'Berg River', 'Land en Zeezicht'],
    'catchment' : ['Wemmershoek', 'Steenbras', 'Steenbras',
                     'Voelvlei', 'Table Mountain', 'Table Mountain',
                     'Table Mountain', 'Table Mountain', 'Table Mountain',
                     'Kleinplaats', 'Lewis Gay', 'Theewaterskloof',
                     'Berg River', 'Land en Zeezicht'],
    'is_big6' : [True, True, False, True, False, False,
                     False, False, False, False, False, True,
                     True, False],
    'capacity_ml' : [58644, 33517, 31767, 164095, 925, 955,
                     531, 184, 242, 1301, 171, 480188,
                     130010, 450]
})
dim_dam['dam_key'] = dim_dam.index + 1
dim_dam.to_excel(MART_PATH + 'dim_dam.xlsx', index=False)
print(f" Rows: {len(dim_dam):,}")

# ── fact_dam_levels ────────────────────────────────────────────────────────
print("\n[4] Building fact_dam_levels...")
fact = df.merge(dim_date[['date', 'date_key']], on='date', how='left')
fact = fact.merge(dim_dam[['dam_name', 'dam_key']], on='dam_name', how='left')

fact = fact[[
    'date_key', 'dam_key',
    'height_m', 'storage_ml', 'current_pct', 'last_year_pct',
    'big6_storage_ml', 'big6_current_pct', 'big6_last_year_pct',
    'is_critical', 'is_day_zero'
]]
# Fill null in numeric columns with 0
numeric_cols = ['height_m', 'storage_ml', 'current_pct', 'last_year_pct',
                'big6_storage_ml', 'big6_current_pct', 'big6_last_year_pct']
fact[numeric_cols] = fact[numeric_cols].fillna(0)

fact.to_excel(MART_PATH + 'fact_dam_levels.xlsx', index=False)
print(f" Rows: {len(fact):,}")

print("\n── Files saved to data/mart/ ──")
print(" dim_date.xlsx")
print(" dim_dam.xlsx")
print(" fact_dam_levels.xlsx")
print("\n✅ Mart layer complete.")