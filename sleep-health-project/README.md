# Sleep Health & Lifestyle: What's Associated with Sleep Disorders?

An exploratory data analysis of 374 individuals, looking at how stress, physical
activity, BMI, and occupation relate to sleep disorders (Insomnia, Sleep Apnea,
or none).

**Dataset:** [Sleep Health and Lifestyle Dataset](https://www.kaggle.com/datasets/uom190346a/sleep-health-and-lifestyle-dataset) (Kaggle)

## Key findings

- **BMI category and Sleep Apnea are clearly linked.** People in the
  Overweight/Obese categories show a much higher rate of Sleep Apnea than
  those with a Normal BMI (see `outputs/03_bmi_vs_disorder.png`).
- **Occupation shows a strong pattern, especially for Nurses.** Nurses have
  the highest rate of any disorder in the dataset — 83.6% have Sleep Apnea —
  while Engineers and Doctors are mostly disorder-free (90%+).
- **Stress level is higher, on average, for people with Insomnia** (5.87)
  than for people with No Disorder (5.11), though the gap is modest.
- **Sleep duration is shortest for people with Insomnia** (6.59 hrs avg) vs.
  7.36 hrs for people with no disorder — the most intuitive result in the
  data, and a useful sanity check that the dataset behaves as expected.

### A caveat worth stating out loud

A few occupations in this dataset have very small sample sizes — Manager
(n=1), Sales Representative (n=2), Scientist (n=4), Software Engineer (n=4).
Percentages for these groups (e.g. "100% Sleep Apnea") are **not reliable**
and are driven by one or two people, not a real trend. Nurse, Doctor,
Engineer, Lawyer, Teacher, Accountant, and Salesperson all have 30+ people
and are much more trustworthy comparisons.

## Charts

| Chart | Question it answers |
|---|---|
| `outputs/01_stress_by_disorder.png` | Is stress level associated with disorder status? |
| `outputs/02_activity_by_disorder.png` | Does physical activity differ by disorder status? |
| `outputs/03_bmi_vs_disorder.png` | Is BMI category related to disorder type? |
| `outputs/04_occupation_vs_disorder.png` | Which occupations have the highest disorder rates? |
| `outputs/05_duration_vs_quality.png` | How do sleep duration and quality relate, by disorder status? |

## Data cleaning notes

The raw CSV had a few issues that are documented and fixed in `src/clean_data.py`:

1. `BMI Category` used both `"Normal"` and `"Normal Weight"` for the same
   group — merged into one label.
2. `Blood Pressure` was stored as a string (`"126/83"`) — split into numeric
   `Systolic BP` and `Diastolic BP` columns.
3. Pandas' default CSV reader treats the literal text `"None"` as a missing
   value. Since `"None"` here is a real category ("no sleep disorder"), this
   silently turned 219 valid rows into NaN. Fixed by disabling that default
   behavior on load, and by renaming the category to `"No Disorder"` so the
   problem can't resurface on a future re-read.

## How to run this yourself

```bash
pip install -r requirements.txt
python src/clean_data.py   # raw CSV -> data/sleep_health_clean.csv
python src/analyze.py      # generates all charts in outputs/
```

## Project structure

```
.
├── data/
│   ├── sleep_health.csv          # raw data from Kaggle
│   └── sleep_health_clean.csv    # cleaned data (generated)
├── src/
│   ├── clean_data.py             # cleaning pipeline
│   └── analyze.py                # EDA + chart generation
├── outputs/                      # generated charts (PNG)
├── requirements.txt
└── README.md
```

## Possible next steps

- Statistical testing (chi-square for occupation vs. disorder) to confirm
  patterns aren't due to chance
- A predictive model (logistic regression) estimating disorder risk from
  the other features
- An interactive dashboard (Streamlit) instead of static charts
