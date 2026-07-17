"""
Cleaning script for the Sleep Health and Lifestyle dataset.

Why this exists as a separate script rather than doing it inline in a notebook:
- It's reusable and reproducible (anyone can re-run it and get the same clean file)
- It documents *what* was wrong with the raw data and *why* we fixed it that way,
  which is exactly what a reviewer looking at your GitHub repo wants to see.
"""

import pandas as pd

RAW_PATH = "data/sleep_health.csv"
CLEAN_PATH = "data/sleep_health_clean.csv"


def load_raw(path: str = RAW_PATH) -> pd.DataFrame:
    # keep_default_na=False + na_values=[""] stops pandas from silently
    # converting the literal string "None" (a real category meaning
    # "no sleep disorder") into a missing value (NaN). Only truly empty
    # cells should count as missing.
    return pd.read_csv(path, keep_default_na=False, na_values=[""])


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- Issue 0: "None" as a category value is a landmine ---
    # Even though we fixed the *loading* step above, the literal text
    # "None" is still ambiguous to any future reader of this CSV (including
    # you, six months from now, opening it with a plain pd.read_csv()).
    # Renaming the category removes the trap entirely instead of relying
    # on everyone remembering the keep_default_na fix.
    df["Sleep Disorder"] = df["Sleep Disorder"].replace({"None": "No Disorder"})

    # --- Issue 1: BMI Category has inconsistent labels ---
    # "Normal" and "Normal Weight" both appear and mean the same thing.
    # If we don't fix this, any chart or groupby splits what should be
    # one group into two, silently distorting the analysis.
    df["BMI Category"] = df["BMI Category"].replace({"Normal Weight": "Normal"})

    # --- Issue 2: Blood Pressure is stored as a string like "126/83" ---
    # You can't do math or plot a range on a string. Split it into two
    # proper numeric columns: systolic and diastolic.
    bp_split = df["Blood Pressure"].str.split("/", expand=True)
    df["Systolic BP"] = bp_split[0].astype(int)
    df["Diastolic BP"] = bp_split[1].astype(int)
    df = df.drop(columns=["Blood Pressure"])

    # --- Issue 3: Column names have spaces, which is annoying in code ---
    # (kept the original display names in the CSV for readability, but
    # this is worth knowing: df.columns.str.replace(' ', '_') is the fix
    # if you want to type df.Sleep_Duration instead of df["Sleep Duration"])

    # --- Issue 4: Check for exact duplicate rows ---
    # Not necessarily an error (could be genuinely identical people), but
    # worth reporting so we know it's there and can decide consciously.
    n_dupes = df.duplicated().sum()
    print(f"Exact duplicate rows found: {n_dupes}")

    # --- Issue 5: Missing values ---
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if len(missing):
        print("Missing values by column:")
        print(missing)
    else:
        print("No missing values found.")

    return df


if __name__ == "__main__":
    raw = load_raw()
    print(f"Raw shape: {raw.shape}")

    cleaned = clean(raw)
    print(f"Clean shape: {cleaned.shape}")

    cleaned.to_csv(CLEAN_PATH, index=False)
    print(f"Saved cleaned data to {CLEAN_PATH}")
