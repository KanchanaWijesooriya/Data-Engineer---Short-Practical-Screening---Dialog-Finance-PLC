"""
Task 1 (Part 3) — Late-arriving records

Rule used to define "late-arriving":
    A row is late-arriving when the gap between ingestion_ts and
    event_ts is MORE THAN 24 hours -- i.e. the top-up happened, but
    it took Meridian's systems over a day to actually record it.

    late  <=>  (ingestion_ts - event_ts) > 24 hours
"""

import pandas as pd

INPUT_PATH = "data\\recharge_events.csv"
OUTPUT_PATH = "outputs\\late_arrivals.csv"

LATE_THRESHOLD = pd.Timedelta(hours=24)


def find_late_arrivals(recharge: pd.DataFrame) -> pd.DataFrame:
    """Return rows where ingestion_ts arrived more than 24 hours after event_ts."""
    delay = recharge["ingestion_ts"] - recharge["event_ts"]
    late_mask = delay > LATE_THRESHOLD
    return recharge[late_mask]


def main():
    recharge = pd.read_csv(INPUT_PATH, parse_dates=["event_ts", "ingestion_ts"])

    late_arrivals = find_late_arrivals(recharge)

    print(f"Total rows in recharge_events.csv: {len(recharge)}")
    print(f"Late-arriving rows (ingestion_ts - event_ts > 24h): {len(late_arrivals)}")

    late_arrivals.to_csv(OUTPUT_PATH, index=False)
    print(f"\nLate-arriving records written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
    