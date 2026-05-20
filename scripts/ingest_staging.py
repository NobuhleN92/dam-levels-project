import pandas as pd
import os

# ── Paths ──────────────────────────────────────────────────────────────────
RAW_PATH     = 'data/raw/Dam_Levels_from_2000.csv'
STAGING_PATH = 'data/staging/dam_levels_staging.csv'

os.makedirs('data/staging', exist_ok=True)

print("=" * 55)
print("STEP 2 — STAGING LAYER: Dam Levels")
print("=" * 55)

# 1. Load raw data
df = pd.read_csv(RAW_PATH, low_memory=False)
print(f"\n[1] Raw rows loaded      : {len(df):,}")

# 2. Fix date column
df['DATE'] = df['DATE'].str.replace('Sept', 'Sep', regex=False)
df['DATE'] = pd.to_datetime(df['DATE'], format='mixed', dayfirst=True)
print(f"\n[2] Date range           : {df['DATE'].min().date()} → {df['DATE'].max().date()}")

# 3. Drop ObjectId
df.drop(columns=['ObjectId'], inplace=True)

# 4. Force numeric on all non-date columns
for col in df.columns:
    if col != 'DATE':
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 5. Define dams and their exact column names
dams = {
    'Wemmershoek'      : ('WEMMERSHOEK_HEIGHT_m_',       'WEMMERSHOEK_STORAGE_Ml_',      'WEMMERSHOEK_Current_',        'WEMMERSHOEK_Last_Year_'),
    'Steenbras Lower'  : ('STEENBRAS_LOWER_HEIGHT_m_',    'STEENBRAS_STORAGE__Ml_',        'STEENBRAS_LOWER_Current__',   'STEENBRAS_LOWER_Last_Year__'),
    'Steenbras Upper'  : ('STEENBRAS_UPPER_HEIGHT_m_',    'STEENBRAS_UPPER_STORAGE_Ml_',   'STEENBRAS_UPPER_Current__',   'STEENBRAS_UPPERLast_Year__'),
    'Voelvlei'         : ('VOËLVLEI_HEIGHT__m_',          'VOËLVLEI_STORAGE__Ml_',         'VOËLVLEI__Current__',         'VOËLVLEI_Last_Year_'),
    'Hely-Hutchinson'  : ('HELY_HUTCHINSON_HEIGHT_m_',    'HELY_HUTCHINSON_STORAGE__Ml_',  'HELY_HUTCHINSON_Current__',   'HELY_HUTCHINSON_Last_Year_'),
    'Woodhead'         : ('WOODHEAD_HEIGHT',              'WOODHEAD_STORAGE_Ml_',          'WOODHEAD_Current_',           'WOODHEAD_Last_Year_'),
    'Victoria'         : ('VICTORIA_HEIGHT',              'VICTORIA_STORAGE_Ml_',          'VICTORIA_Current_',           'VICTORIALast_Year_'),
    'Alexandra'        : ('ALEXANDRA_HEIGHT_m_',          'ALEXANDRA_STORAGE_Ml_',         'ALEXANDRA_Current_',          'ALEXANDRA_Last_Year_'),
    'De Villiers'      : ('DE_VILLIERS_HEIGHT_m_',        'DE_VILLIERS_STORAGE_Ml_',       'DE_VILLIERS_Current_',        'DE_VILLIERS_Last_Year_'),
    'Kleinplaats'      : ('KLEINPLAATS_HEIGHT__m_',       'KLEINPLAATS_STORAGE_Ml_',       'KLEINPLAATS_Current__',       'KLEINPLAATS_Last_Year__'),
    'Lewis Gay'        : ('LEWIS_GAY_HEIGHT__m_',         'LEWIS_GAY_STORAGE__Ml_',        'LEWIS_GAY_Current__',         'LEWIS_GAY_Last_Year__'),
    'Theewaterskloof'  : ('THEEWATERSKLOOF_HEIGHT__m_',   'THEEWATERSKLOOF_STORAGE__Ml_',  'THEEWATERSKLOOF_Current',     'THEEWATERSKLOOF_Last_Year__'),
    'Berg River'       : ('BERG_RIVER_HEIGHT__m_',        'BERG_RIVER_STORAGE__Ml_',       'BERG_RIVER_Current__',        'BERG_RIVER_Last_Year__'),
    'Land en Zeezicht' : ('LAND_en_ZEEZICHT_HEIGHT__m_',  'LAND_en_ZEEZICHT_STORAGE__Ml_', 'LAND_en_ZEEZICHT_Current__',  'LAND_en_ZEEZICHT_Last_Year__'),
}

# 6. Reshape wide → long
records = []
for dam_name, (h_col, s_col, c_col, ly_col) in dams.items():
    temp = df[['DATE', h_col, s_col, c_col, ly_col]].copy()
    temp.columns = ['date', 'height_m', 'storage_ml', 'current_pct', 'last_year_pct']
    temp['dam_name'] = dam_name
    records.append(temp)

long_df = pd.concat(records, ignore_index=True)

# 7. Keep Big 6 totals
totals = df[['DATE', 'TOTAL_STORED___BIG_6_STORAGE', 'TOTAL_STORED___BIG_6_Current', 'TOTAL_STORED___BIG_6_Last_Year']].copy()
totals.columns = ['date', 'big6_storage_ml', 'big6_current_pct', 'big6_last_year_pct']
long_df = long_df.merge(totals, on='date', how='left')

# 8. Drop rows where all measures are null
before = len(long_df)
long_df.dropna(subset=['height_m', 'storage_ml', 'current_pct'], how='all', inplace=True)
print(f"\n[3] Rows in staging      : {len(long_df):,}")
print(f"    Rows dropped (null)  : {before - len(long_df):,}")

# 9. Add derived date columns
long_df['year']       = long_df['date'].dt.year
long_df['month']      = long_df['date'].dt.month
long_df['month_name'] = long_df['date'].dt.strftime('%B')
long_df['quarter']    = long_df['date'].dt.quarter
long_df['season']     = long_df['month'].map({
    12:'Summer', 1:'Summer', 2:'Summer',
    3:'Autumn',  4:'Autumn', 5:'Autumn',
    6:'Winter',  7:'Winter', 8:'Winter',
    9:'Spring', 10:'Spring', 11:'Spring'
})

# 10. Flag critical levels
long_df['is_critical'] = long_df['current_pct'] < 20
long_df['is_day_zero'] = long_df['big6_current_pct'] < 13.5

# 11. Save
long_df.to_csv(STAGING_PATH, index=False)
long_df.to_excel('data/staging/dam_levels_staging.xlsx', index=False)
print(f"\n[4] Staging file saved   : {STAGING_PATH}")
print("\n✅ Staging layer complete.")


   