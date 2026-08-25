"""
Task 2 — recharge_count_30d feature

"""
import pandas as pd

RECHARGE_PATH = "data\\recharge_events.csv"
LOANS_PATH = "data\\loan_applications.csv"
OUTPUT_PATH = "outputs\\features.csv"

DUP_KEY = ["customer_token", "event_ts", "amount_lkr", "is_reversal"]
WINDOW_DAYS = 30


def main():
    recharge = pd.read_csv(RECHARGE_PATH, parse_dates=["event_ts", "ingestion_ts"])
    loans = pd.read_csv(LOANS_PATH, parse_dates=["application_ts"])
    print(f"Loaded recharge_events.csv: {len(recharge)} rows")
    print(f"Loaded loan_applications.csv: {len(loans)} rows")

    # Step 1: remove duplicates, keep only valid top-ups (not reversals, amount > 0)
    before_dedup = len(recharge)
    recharge = recharge.drop_duplicates(subset=DUP_KEY)
    after_dedup = len(recharge)
    print(f"Step 1: removed duplicates -> {before_dedup - after_dedup} dropped, {after_dedup} remaining")

    valid = recharge[(recharge["is_reversal"] == 0) & (recharge["amount_lkr"] > 0)]
    print(f"Step 1: kept valid top-ups only -> {after_dedup - len(valid)} dropped (reversals/invalid), {len(valid)} remaining")

    # Step 2: join valid top-ups to applications on customer_token
    merged = loans.merge(valid, on="customer_token", how="left", suffixes=("", "_rch"))
    print(f"Step 2: joined to applications -> {len(merged)} rows after join")

    # Step 3: apply the 30-day window + point-in-time rule together
    #
    # Point-in-time rule: a top-up only counts if Meridian had already
    # ingested it by the moment the application was made (ingestion_ts
    # <= application_ts). A top-up that happened inside the 30-day
    # window but was logged into the system after the application was
    # submitted couldn't have been seen by a loan officer at decision
    # time, so it must be excluded even though it occurred in time.
    window_start = merged["application_ts"] - pd.Timedelta(days=WINDOW_DAYS)
    in_window = (merged["event_ts"] >= window_start) & (merged["event_ts"] < merged["application_ts"])
    available_in_time = merged["ingestion_ts"] <= merged["application_ts"]

    merged["counts"] = in_window & available_in_time
    print(f"Step 3: rows in 30-day window: {in_window.sum()}, of which available in time: {(in_window & available_in_time).sum()}")

    # Step 4: aggregate per application (0 for applications with no qualifying top-ups)
    features = (
        merged.groupby("application_id")["counts"]
        .sum()
        .reset_index()
        .rename(columns={"counts": "recharge_count_30d"})
    )
    features["recharge_count_30d"] = features["recharge_count_30d"].astype(int)
    print(f"Step 4: aggregated recharge_count_30d for {len(features)} applications")

    # Step 5: ensure exactly one row per application, in original order
    features = loans[["application_id"]].merge(features, on="application_id", how="left")
    features["recharge_count_30d"] = features["recharge_count_30d"].fillna(0).astype(int)
    print(f"Step 5: final row count matches applications -> {len(features)} rows")

    features.to_csv(OUTPUT_PATH, index=False)
    print(f"\nApplications: {len(loans)}")
    print(f"Rows written to {OUTPUT_PATH}: {len(features)}")


if __name__ == "__main__":
    main()
    