
"""
summary.py

Generates summary CSVs for Dendrometer and TMS,
merges them into your JOINED.*.csv metadata files,
and also produces daily summaries per sensor.

These files will be used in ArcGIS Online to build our Story.
"""

import os
import re
import glob
import pandas as pd

# ─── CONFIG ────────────────────────────────────────────────────────────────────

DENDRO_DATA_DIR     = "Dendrometer_Data"
TMS_DATA_DIR        = "TMS_Data"

JOINED_DENDRO_CSV   = "JOINED.DENDROMETER.csv"
JOINED_TMS_CSV      = "JOINED.TMS.csv"

OUTPUT_DENDRO       = "Dendrometer_Average.csv"
OUTPUT_TMS          = "TMS_Average.csv"
OUTPUT_DENDRO_DAILY = "Dendrometer_Daily.csv"
OUTPUT_TMS_DAILY    = "TMS_Daily.csv"

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def summarize_folder(data_dir, metrics, sep=';', verbose=True):
    """
    Compute overall mean metrics per sensor.
    """
    records = []
    pattern = re.compile(r"data_(\d+)_\d{4}_\d{2}_\d{2}_\d+\.csv")
    paths = glob.glob(os.path.join(data_dir, "data_*.csv"))

    for path in paths:
        fname = os.path.basename(path)
        m = pattern.match(fname)
        if not m:
            if verbose: print(f"⚠️  skipping unexpected filename: {fname}")
            continue
        sensor_id = int(m.group(1))

        df = pd.read_csv(path, header=None, sep=sep, engine='python')
        if df.shape[1] <= max(metrics.values()):
            if verbose: print(f"⚠️  {fname} only has {df.shape[1]} cols—skipping")
            continue

        summary = {'sensor_id': sensor_id}
        for col_name, idx in metrics.items():
            summary[col_name] = df.iloc[:, idx].mean()
        records.append(summary)

    if verbose:
        print(f"  • scanned {len(paths)} files, produced {len(records)} summaries")
    return pd.DataFrame(records)


def daily_summary(data_dir, metrics, sep=';', verbose=True):
    """
    Compute daily mean metrics per sensor.
    Returns a DataFrame with columns: sensor_id, date, <metrics>
    """
    dfs = []
    pattern = re.compile(r"data_(\d+)_\d{4}_\d{2}_\d{2}_\d+\.csv")
    paths = glob.glob(os.path.join(data_dir, "data_*.csv"))

    for path in paths:
        fname = os.path.basename(path)
        m = pattern.match(fname)
        if not m:
            if verbose: print(f"⚠️  skipping unexpected filename: {fname}")
            continue
        sensor_id = int(m.group(1))

        df = pd.read_csv(path, header=None, sep=sep, engine='python')
        if df.shape[1] <= max(metrics.values()) or df.shape[1] <= 1:
            if verbose: print(f"⚠️  {fname} only has {df.shape[1]} cols—skipping")
            continue

        # Extract timestamp and metrics
        data = df.iloc[:, [1] + list(metrics.values())].copy()
        data.columns = ['timestamp'] + list(metrics.keys())
        data['sensor_id'] = sensor_id
        dfs.append(data)

    if not dfs:
        return pd.DataFrame()

    all_data = pd.concat(dfs, ignore_index=True)
    all_data['timestamp'] = pd.to_datetime(all_data['timestamp'], format="%Y.%m.%d %H:%M", errors='coerce')
    all_data['date'] = all_data['timestamp'].dt.date

    daily = (
        all_data
        .groupby(['sensor_id','date'])[list(metrics.keys())]
        .mean()
        .reset_index()
    )
    if verbose:
        print(f"  • aggregated to {len(daily)} daily rows")
    return daily

# ─── DENDROMETER OVERALL ───────────────────────────────────────────────────────

print("🔄 Summarizing dendrometer data…")
dendro_metrics = {'avg_air_temp': 3, 'avg_growth': 6}

df_dendro_sum = summarize_folder(DENDRO_DATA_DIR, dendro_metrics)

print(f"🔄 Reading metadata from {JOINED_DENDRO_CSV}")
df_meta_d = pd.read_csv(JOINED_DENDRO_CSV)

print("🔄 Merging summaries into metadata")
df_dendro_out = df_meta_d.merge(df_dendro_sum, on='sensor_id', how='left')

print(f"🔄 Writing output to {OUTPUT_DENDRO}")
df_dendro_out.to_csv(OUTPUT_DENDRO, index=False)

# ─── DENDROMETER DAILY ─────────────────────────────────────────────────────────

print("🔄 Building daily dendrometer summaries…")
dendro_daily = daily_summary(DENDRO_DATA_DIR, dendro_metrics)
# keep only sensor_id, date, metrics, then merge location/metadata
meta_sel = df_meta_d[['sensor_id','X','Y','Common_Name']]

df_dendro_daily = dendro_daily.merge(meta_sel, on='sensor_id', how='left')
print(f"🔄 Writing output to {OUTPUT_DENDRO_DAILY}")
df_dendro_daily.to_csv(OUTPUT_DENDRO_DAILY, index=False)

# ─── TMS OVERALL ───────────────────────────────────────────────────────────────

print("🔄 Summarizing TMS data…")
tms_metrics = {'avg_t1':3,'avg_t2':4,'avg_t3':5,'avg_moist':6}

df_tms_sum = summarize_folder(TMS_DATA_DIR, tms_metrics)

print(f"🔄 Reading metadata from {JOINED_TMS_CSV}")
df_meta_t = pd.read_csv(JOINED_TMS_CSV)

print("🔄 Merging TMS summaries into metadata")
df_tms_out = df_meta_t.merge(df_tms_sum, on='sensor_id', how='left')

print(f"🔄 Writing output to {OUTPUT_TMS}")
df_tms_out.to_csv(OUTPUT_TMS, index=False)

# ─── TMS DAILY ─────────────────────────────────────────────────────────────────

print("🔄 Building daily TMS summaries…")
tms_daily = daily_summary(TMS_DATA_DIR, tms_metrics)
meta_sel_t = df_meta_t[['sensor_id','X','Y','Common_Name']]

df_tms_daily = tms_daily.merge(meta_sel_t, on='sensor_id', how='left')
print(f"🔄 Writing output to {OUTPUT_TMS_DAILY}")
df_tms_daily.to_csv(OUTPUT_TMS_DAILY, index=False)

print("✅ Done.")
