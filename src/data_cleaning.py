import os
import pandas as pd

print("Current working directory:", os.getcwd())


# ---------------------------
# LOAD DATA
# ---------------------------
def load_data(path):
    """Load dataset from CSV"""
    return pd.read_csv(path)


# ---------------------------
# HANDLE OUTLIERS (IQR METHOD)
# ---------------------------
def cap_outliers(df, col):
    """Cap outliers using IQR method"""
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df[col] = df[col].clip(lower, upper)
    return df


# ---------------------------
# CLEAN DATA
# ---------------------------
def clean_data(df):
    df = df.copy()

    print("\n🔹 Initial shape:", df.shape)

    # 1️⃣ Remove duplicates
    df = df.drop_duplicates()

    # 2️⃣ Handle missing values
    df["social_support"] = df["social_support"].fillna("Unknown")

    # 3️⃣ Outlier capping
    outlier_cols = [
        "smokes_per_day",
        "drinks_per_week",
        "sleep_hours",
        "bmi"
    ]

    for col in outlier_cols:
        df = cap_outliers(df, col)

    # 4️⃣ Logical checks
    df = df[df["age_started_smoking"] <= df["age"]]
    df = df[df["age_started_drinking"] <= df["age"]]

    print("✅ Final shape after cleaning:", df.shape)

    return df


# ---------------------------
# SAVE DATA
# ---------------------------
def save_data(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"\n💾 Cleaned data saved to: {path}")


# ---------------------------
# MAIN PIPELINE
# ---------------------------
if __name__ == "__main__":
    raw_path = "data/raw/addiction_population_data.csv"
    clean_path = "data/cleaned/addiction_population_clean.csv"

    df = load_data(raw_path)
    df_clean = clean_data(df)
    save_data(df_clean, clean_path)