"""
add_image_urls.py

Reads JOINED.DENDROMETER.csv, adds an 'image_url' column pointing to
each sensor's first image on GitHub Pages, and writes out a new CSV.
"""

import pandas as pd

INPUT_CSV  = "JOINED.DENDROMETER.csv"
OUTPUT_CSV = "JOINED.DENDROMETER_with_images.csv"

# If you enabled GitHub Pages on this repo:
URL_TEMPLATE = (
    "https://danielaggwm.github.io/arboretum/"
    "Images/{sensor_id}/1.jpeg"
)

print(f"🔄 Reading metadata from {INPUT_CSV}")
df = pd.read_csv(INPUT_CSV)

df['sensor_id'] = df['sensor_id'].astype(str)
print("🔄 Adding image_url column")
df['image_url'] = df['sensor_id'].apply(lambda sid: URL_TEMPLATE.format(sensor_id=sid))

print(f"🔄 Writing output to {OUTPUT_CSV}")
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ Done — {len(df)} rows written with image_url.")
