# Submission — Chanuka Kanchana Wijesooriya

## Task 1 — Data quality check

This is the way i handle these requested operations in assessment, for more information go to the optional notes section.

All the steps are ccelarly in this qork drectory, so do not try to change file locations.

if any script want to run and seen the result execute => `python copy_relative_path of file.py`

Task 1 explicitly asking in question, So I assuming,
"Inspect `recharge_events.csv` and report the exact count of each of the following, plus one sentence on how you would handle it in a production pipeline" it asking to use only"`recharge_events.csv` and report the exact count of each" so i used the same raw data file to perform assessment task 1 parts considering as 03 separate tasks, and didn't use clean data set earlier part for next part in task 1.

So, in task 2 I ran these task 1 steps again as a continuously running pipeline to deduplicate, exclude invalid rows.

| Check | Count | How I'd handle it in a pipeline |
|---|---|---|
| Duplicate top-ups (same real recharge appearing more than once) | 40|Rule I used to handle duplicate, A duplicate = two or more rows that share the same, considered columns, for more about the way and rule i thought go to optianal notes section.|
| Invalid amounts (non-reversal rows with amount <= 0) | 25  (without deduplication, directly to the original raw data file)| Rule I used to decide a row is invalid amount when it is NOT a reversal (is_reversal == 0) and its amount_lkr is zero or negative. (`is_reversal` = 0 and `amount_lkr` <= 0) |
| Late-arriving records (landed > 24h after the event) |44  (without deduplication, directly to the original raw data file) |Rule I used to define "late-arriving", A row is late-arriving when the gap between ingestion_ts and event_ts is MORE THAN 24 hours. <br>  late  <=>  (`ingestion_ts`​ - `event_ts​`) > 24 hours |

## Task 2 — Point-in-time feature 

- To run the code execute `python exercise\build_features_starter.py`command in terminal.
- Output file: `outputs\features.csv`
- A top-up only counts toward `recharge_count_30d` if it fell within the 30 days before application_ts and was already ingested into Meridian's system by that same `application_ts` (`ingestion_ts` <= `application_ts`), because a loan officer at decision time could only ever see data the system had actually recorded so far.

- In other words, a top-up that genuinely happened within the 30-day window but was logged late, after the application was already submitted, is excluded, since including it would mean using information that wasn't actually available at the moment the decision was being made.
## Task 3 — Judgement & walkthrough

**(a) Can `label_default_90d` be used as an input feature? Why / why not?**
 
- No
- We can't use `label_default_90d` as an input feature. It's the actual outcome we're trying to predict, and we only find out its true value months after the loan is given out, once we see whether the person actually defaulted or not. But the model has to make its prediction the moment someone applies, before that outcome even exists yet, so using it as an input would mean giving the model the answer to the exact question it's supposed to figure out on its own (this is called data leakage).   
- It would look perfect during testing since it's just reading back the label, but it would completely fail on a real new applicant, since that column simply wouldn't exist yet for them at that point. This is really the same idea as the point-in-time rule from Task 2, just in its clearest and most obvious form: never let the model see information from the future relative to when the decision actually has to be made.

**(b) One `event_id` a careless Task 2 would count but should not, and why:**

- `event_id`: RCH_01373
- Reason:
  - `RCH_01373` (application `APP_0001`, customer `CUST_0001`)
    - `event_ts` = 2026-03-12 21:29:56 (the top-up happened here — within the 30 days before the application)
    - `application_ts` = 2026-03-17 01:17:33 (the loan application)
    - `ingestion_ts` = 2026-03-18 14:20:38 (Meridian didn't actually log this top-up until after the application)
- `RCH_01373` is a top-up that happened on 2026-03-12, which falls within the 30 days before application `APP_0001` was submitted on 2026-03-17. A careless implementation that only checks whether event_ts falls in the 30-day window would wrongly count it, but this record wasn't actually ingested into Meridian's system until 2026-03-18, a day after the application was already made, so it couldn't have been available to a loan officer at decision time and should be excluded.

**(c) Video Link:**  [Short Demo Video of explaining task 2 click here](https://drive.google.com/file/d/1ew-yve_wNn7abzYHYGUQKNIQx4vT6fGu/view?usp=sharing) or view directly https://drive.google.com/file/d/1ew-yve_wNn7abzYHYGUQKNIQx4vT6fGu/view?usp=sharing  
If you feels video quality is low try it 720P

## Notes / assumptions (optional)

### Task 1: part 1:
 - Original rows involved in a duplicate group: 80  
     Distinct duplicated real recharges: 40  
     Extra rows (duplicates to remove): 40  
 - `customer_token` + `event_ts` + `amount_lkr` + `is_reversal` together describe the
      real-world event (who, when it happened, how much, reversal or not) so, this is
      what a "recharge" actually is from the customer's perspective. I also included `is_reversal` because there can be same other column vaues with is_reversal = 1,1 or 0,0.
 - `event_id` is excluded: it is a synthetic and system auto generated ID
      that is unique per row by design, even when the same real
      recharge has been logged more than once due to some reason like delays, retries. Deduping on it would
      never find a duplicate. Also manually chcked the csv as well and all event_id's are unique.
 - `ingestion_ts` is excluded: it records when the row landed in
      Meridian's systems, not when the recharge happened. A true
      duplicate (e.g. a retried/re-ingested record) is expected to
      have a DIFFERENT ingestion_ts for the same real event, so
      including it in the key would hide exactly the duplicates
      we're trying to catch. 
 - You can view code on `exercise\clean_duplicates.py` and results `outputs\duplicate_rows.csv`.

### part 2,3:
 - This check is run against the raw, untouched `recharge_events.csv`, as independent tasks.
 - In this task when the code execution, you can see how many duplication removed and invalid rows excluded from data set as a sequential pipeline in termnal tab.

### part 3:
 - Reversal rows (`is_reversal` == 1) are included in this check.
      Lateness is about how long a record took to reach the system,
      which applies to any row regardless of whether it's a genuine
      top-up or a reversal. So, there's no reason to treat them
      differently for this particular check.


