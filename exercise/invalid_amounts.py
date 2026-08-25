"""
Task 1 (Part 2) — Invalid amount detection

Rule used to define "invalid amount":
    A row is invalid when it is NOT a reversal (is_reversal == 0)
    but its amount_lkr is zero or negative.

This check is run against the raw, untouched recharge_events.csv,
independent of the duplicate check in Part 1 -- each Task 1 check
reports on the raw data as-is, rather than being applied sequentially
on top of a cleaned file.
"""

import pandas as pd

INPUT_PATH = "data\\recharge_events.csv"
OUTPUT_PATH = "outputs\\invalid_records.csv"


def find_invalid_amounts(recharge: pd.DataFrame) -> pd.DataFrame:
    """Return non-reversal rows whose amount is zero or negative."""
    invalid_mask = (recharge["is_reversal"] == 0) & (recharge["amount_lkr"] <= 0)
    return recharge[invalid_mask]


def main():
    recharge = pd.read_csv(INPUT_PATH)

    invalid_records = find_invalid_amounts(recharge)

    print(f"Total rows in recharge_events.csv: {len(recharge)}")
    print(f"Invalid amount rows (non-reversal, amount <= 0): {len(invalid_records)}")

    invalid_records.to_csv(OUTPUT_PATH, index=False)
    print(f"\nInvalid records written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
    