"""
starter.py — optional scaffold for the Meridian screening task.

Using this is OPTIONAL. You may write your solution however you like
(pandas, plain Python, SQL/DuckDB, etc.). This just loads the two CSVs
and shows the shape of the expected output.

Run:  python starter.py
"""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    apps = pd.read_csv(DATA_DIR / "loan_applications.csv")
    recharges = pd.read_csv(DATA_DIR / "recharge_events.csv")
    # Parse timestamps as timezone-aware (they are in +05:30).
    apps["application_ts"] = pd.to_datetime(apps["application_ts"], utc=True)
    recharges["event_ts"] = pd.to_datetime(recharges["event_ts"], utc=True)
    recharges["ingestion_ts"] = pd.to_datetime(recharges["ingestion_ts"], utc=True)
    return apps, recharges


def main() -> None:
    apps, recharges = load_data()
    print(f"loan_applications: {len(apps)} rows")
    print(f"recharge_events:   {len(recharges)} rows")

    # TODO Task 2: build one row per application with recharge_count_30d.
    # Expected output columns: application_id, recharge_count_30d
    #
    # Remember: count only VALID top-ups in the 30 days before application_ts
    # that were ACTUALLY AVAILABLE in the system at the moment of application.

    # Example of the expected output shape (values are placeholders):
    example = apps[["application_id"]].copy()
    example["recharge_count_30d"] = 0
    print(example.head())


if __name__ == "__main__":
    main()
