# utils/analytics.py
import pandas as pd

def add_resolution_hours(df: pd.DataFrame) -> pd.DataFrame:
    closed_df = df[df["status"] == "Closed"].copy()
    if closed_df.empty:
        return closed_df

    closed_df["date_raised"] = pd.to_datetime(closed_df["date_raised"], errors="coerce")
    closed_df["date_closed"] = pd.to_datetime(closed_df["date_closed"], errors="coerce")
    closed_df = closed_df.dropna(subset=["date_raised", "date_closed"])

    if closed_df.empty:
        return closed_df

    closed_df["resolution_hours"] = (
        closed_df["date_closed"] - closed_df["date_raised"]
    ).dt.total_seconds() / 3600.0

    return closed_df

def get_trend_df(df: pd.DataFrame) -> pd.DataFrame:
    trend_df = df.copy()
    trend_df["date"] = pd.to_datetime(trend_df["date_raised"], errors="coerce").dt.date
    trend_df = trend_df.dropna(subset=["date"])
    return trend_df.groupby("date").size().reset_index(name="total_queries")

def get_support_load(df: pd.DataFrame):
    total = len(df)
    open_count = (df["status"] == "Open").sum()
    closed_count = (df["status"] == "Closed").sum()
    return total, open_count, closed_count
