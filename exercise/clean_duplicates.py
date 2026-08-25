"""
Task 1 : (Part 1) — Duplicate detection

Rule used to define "the same real recharges":
    A duplicate = two or more rows that share the same
    used columns: customer_token, event_ts, amount_lkr, is_reversal
    reason defined in the readme file as requested.
"""

import pandas as pd
 
INPUT_PATH = "data\\recharge_events.csv"
OUTPUT_PATH = "outputs\\duplicate_rows.csv"
 
DUP_KEY = ["customer_token", "event_ts", "amount_lkr", "is_reversal"]
 
 
def find_duplicates(recharge: pd.DataFrame) -> pd.DataFrame:
    """Return all rows that belong to a duplicate group, sorted for readability."""
    dup_mask = recharge.duplicated(subset=DUP_KEY, keep=False)
    return recharge[dup_mask].sort_values(DUP_KEY)
 
 
def main():
    recharge = pd.read_csv(INPUT_PATH)
 
    duplicate_rows = find_duplicates(recharge)
 
    num_duplicate_rows = len(duplicate_rows)
    num_duplicate_events = duplicate_rows.groupby(DUP_KEY).ngroups
    num_extra_rows = num_duplicate_rows - num_duplicate_events
 
    print(f"Total rows in recharge_events.csv:        {len(recharge)}")
    print(f"Rows involved in a duplicate group:        {num_duplicate_rows}")
    print(f"Distinct duplicated real recharges:        {num_duplicate_events}")
    print(f"Extra rows (duplicates to remove):         {num_extra_rows}")
 
    duplicate_rows.to_csv(OUTPUT_PATH, index=False)
    print(f"\nDuplicate rows written to {OUTPUT_PATH}")
 
 
if __name__ == "__main__":
    main()
    