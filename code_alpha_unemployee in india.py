import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

DATASET_PATH = Path(r"C:\Users\mithr\Downloads\Unemployment in India (4).csv")

try:
    df = pd.read_csv(DATASET_PATH)
    print("Dataset loaded successfully!\n")
except FileNotFoundError:
    print(f"Error: Dataset file not found at {DATASET_PATH}")
    exit()

print("First 5 Rows:")
print(df.head())
print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

df.columns = df.columns.str.strip()

df.dropna(inplace=True)

df.columns = [
    "Region",
    "Date",
    "Frequency",
    "Estimated_Unemployment_Rate",
    "Estimated_Employed",
    "Estimated_Labour_Participation_Rate",
    "Area"
]
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

if df["Date"].isna().any():
    df = df.dropna(subset=["Date"]).copy()

print("\nCleaned Dataset Shape:", df.shape)
print("\nStatistical Summary:")
print(df.describe())

region_unemployment = (
    df.groupby("Region")["Estimated_Unemployment_Rate"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Unemployment Rate by Region:")
print(region_unemployment)

plt.figure(figsize=(12,6))
region_unemployment.head(10).plot(kind="bar")
plt.title("Top 10 Regions by Average Unemployment Rate")
plt.xlabel("Region")
plt.ylabel("Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

monthly_trend = (
    df.groupby(df["Date"].dt.month)
    ["Estimated_Unemployment_Rate"]
    .mean()
)

plt.figure(figsize=(10,5))
plt.plot(monthly_trend.index, monthly_trend.values, marker='o')
plt.title("Monthly Average Unemployment Rate")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.grid(True)
plt.show()

print("\n========== PROJECT INSIGHTS ==========")
print(f"Highest Average Unemployment Region : {region_unemployment.idxmax()}")
print(f"Rate : {region_unemployment.max():.2f}%")

print(f"\nLowest Average Unemployment Region : {region_unemployment.idxmin()}")
print(f"Rate : {region_unemployment.min():.2f}%")

print("\nAnalysis Completed Successfully!")
