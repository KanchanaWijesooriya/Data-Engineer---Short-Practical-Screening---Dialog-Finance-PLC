# Senior Data Engineer — Short Practical Screening

Thank you for applying for the **Senior Data Engineer** position supporting Dialog Finance PLC's telco‑credit analytics work.

This is a **short, practical screening task**. It should take about **2–4 hours of focused effort**. You have **24 hours** from receipt to submit. We would rather see a small amount of careful, correct, well‑explained work than a large amount of rushed work.

> **All data in this task is synthetic and invented for assessment purposes.** The scenario below uses fictional companies. No real customer, financial, or telco data is involved.

---

## The scenario (fictional)

**Meridian Telecom** is a mobile network operator. Its sister company, **Meridian Finance**, offers small digital loans and wants to use *approved, privacy‑safe* telco behaviour (like top‑up / recharge activity) to help assess credit.

You are a data engineer sitting **inside Meridian Telecom**. Your job is to turn raw telco records into clean, trustworthy, **point‑in‑time‑correct** inputs that Meridian Finance can rely on — without ever leaking information that wouldn't have been known at the moment a loan was requested.

This screening uses a tiny slice of that world: **loan applications** and **mobile recharge (top‑up) events**.

---

## The data (in `data/`)

### `loan_applications.csv` — 180 rows
One row per loan application.

| Column | Meaning |
|---|---|
| `application_id` | Unique application ID |
| `customer_token` | Synthetic, irreversible customer key (used to join to telco data) |
| `application_ts` | Timestamp the loan was applied for (Asia/Colombo, ISO‑8601) |
| `requested_amount_lkr` | Requested loan amount |
| `label_default_90d` | Whether this customer defaulted within 90 days (**outcome**, not an input) |

### `recharge_events.csv` — 1,464 rows
One row per mobile top‑up (recharge) event.

| Column | Meaning |
|---|---|
| `event_id` | Unique event ID |
| `customer_token` | Customer key (joins to applications) |
| `event_ts` | When the top‑up actually happened |
| `ingestion_ts` | When the record actually **landed in Meridian's data systems** |
| `amount_lkr` | Top‑up amount (negative values are used for reversals) |
| `is_reversal` | `1` if this row reverses a previous top‑up, else `0` |

---

## Your tasks

### Task 1 — Quick data‑quality check (~45 min)

Inspect `recharge_events.csv` and report the **exact count** of each of the following, plus **one sentence** on how you would handle it in a production pipeline:

1. **Duplicate top‑ups** — the *same real recharge* appearing more than once.
2. **Invalid amounts** — non‑reversal rows whose amount is zero or negative.
3. **Late‑arriving records** — rows that landed in the system **more than 24 hours** after the top‑up happened.

> Be explicit about the rule you used for "duplicate." There is a right answer, and how you define "same real recharge" matters.

### Task 2 — One point‑in‑time feature (~90 min) — *the main task*

For **each loan application**, compute a single feature:

> **`recharge_count_30d`** = the number of **valid top‑ups** in the **30 days before `application_ts`** that were **actually available in Meridian's systems at the moment the application was made**.

- "Valid top‑ups" means real top‑ups, not reversals or invalid rows.
- Read the emphasised phrase above carefully. It is the point of this task.
- Output exactly one row per application.

**Deliverable:** `features.csv` with two columns: `application_id`, `recharge_count_30d` — plus the script/code that produced it.

### Task 3 — Judgement & walkthrough (~45 min)

In your `SUBMISSION.md`, answer briefly (a few sentences each — not essays):

**(a)** `loan_applications.csv` includes `label_default_90d`. May it be used as an **input feature** for a credit model? Why or why not?

**(b)** Name **one specific `event_id`** from `recharge_events.csv` that a careless implementation of Task 2 **would count but should not**, and explain in one or two sentences why.

**(c)** Record a **3–5 minute screen walkthrough** (Loom, screen recording, or similar) of your Task 2 code, explaining the **single design decision you are most confident about**. Paste the link (or attach the file). Talking us through your own code in your own words is a required part of this screening.

---

## What to submit

A single ZIP or a link to a private repository containing:

```
features.csv          ← your Task 2 output
SUBMISSION.md         ← Task 1 counts, Task 3 answers, recording link
<your code>           ← the script(s) that produced features.csv
```

- Your code must **run** and reproduce `features.csv` from the two CSVs in `data/`.
- Use any mainstream language/library (Python + pandas or SQL/DuckDB are all fine).
- Do **not** include the raw data files in your submission; we already have them.
- Do **not** include credentials, secrets, or any real personal data.

A starter file is provided in `starter/` if you'd like a scaffold — using it is optional.

---

## How you'll be assessed (high level)

We are looking for **correctness, judgement, and clear communication** — not volume. A tidy, correct, well‑explained submission from someone who clearly understands *why* each choice was made will always beat a large, clever‑looking one that gets the fundamentals wrong.

Good luck — we're looking forward to seeing how you think.
