"""
Exploratory analysis: What's associated with having a sleep disorder?

This script answers a few sub-questions and saves one chart per question
to outputs/. Each function is self-contained and commented so it's easy
to follow the reasoning in a code review or GitHub browse.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
DATA_PATH = "data/sleep_health_clean.csv"
OUTPUT_DIR = "outputs"

DISORDER_ORDER = ["No Disorder", "Insomnia", "Sleep Apnea"]
DISORDER_PALETTE = {"No Disorder": "#4C9F70", "Insomnia": "#E8A33D", "Sleep Apnea": "#C1443D"}


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def chart_stress_by_disorder(df: pd.DataFrame) -> None:
    """Q1: Is stress level associated with having a sleep disorder?"""
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(
        data=df, x="Sleep Disorder", y="Stress Level", hue="Sleep Disorder",
        order=DISORDER_ORDER, palette=DISORDER_PALETTE, legend=False, ax=ax,
    )
    ax.set_title("Stress Level by Sleep Disorder Status")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/01_stress_by_disorder.png", dpi=150)
    plt.close(fig)


def chart_activity_by_disorder(df: pd.DataFrame) -> None:
    """Q2: Does physical activity level differ by disorder status?"""
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.boxplot(
        data=df, x="Sleep Disorder", y="Physical Activity Level", hue="Sleep Disorder",
        order=DISORDER_ORDER, palette=DISORDER_PALETTE, legend=False, ax=ax,
    )
    ax.set_title("Physical Activity Level by Sleep Disorder Status")
    ax.set_xlabel("")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/02_activity_by_disorder.png", dpi=150)
    plt.close(fig)


def chart_bmi_vs_disorder(df: pd.DataFrame) -> None:
    """Q3: Is BMI category related to which disorder (if any) someone has?"""
    ct = pd.crosstab(df["BMI Category"], df["Sleep Disorder"], normalize="index") * 100
    ct = ct[DISORDER_ORDER]
    fig, ax = plt.subplots(figsize=(8, 5))
    ct.plot(kind="bar", stacked=True, color=[DISORDER_PALETTE[c] for c in DISORDER_ORDER], ax=ax)
    ax.set_title("Sleep Disorder Breakdown by BMI Category")
    ax.set_ylabel("% of group")
    ax.set_xlabel("")
    ax.legend(title="", loc="upper right")
    plt.xticks(rotation=0)
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/03_bmi_vs_disorder.png", dpi=150)
    plt.close(fig)


def chart_occupation_vs_disorder(df: pd.DataFrame) -> None:
    """Q4: Which occupations have the highest rate of sleep disorders?"""
    ct = pd.crosstab(df["Occupation"], df["Sleep Disorder"], normalize="index") * 100
    ct = ct[DISORDER_ORDER]
    # Sort by "healthiest first" so the chart tells a clear story left-to-right
    ct = ct.sort_values("No Disorder", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ct.plot(kind="bar", stacked=True, color=[DISORDER_PALETTE[c] for c in DISORDER_ORDER], ax=ax)
    ax.set_title("Sleep Disorder Rate by Occupation")
    ax.set_ylabel("% of occupation group")
    ax.set_xlabel("")
    ax.legend(title="", loc="lower left")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/04_occupation_vs_disorder.png", dpi=150)
    plt.close(fig)


def chart_sleep_duration_quality(df: pd.DataFrame) -> None:
    """Q5: How do duration and quality of sleep relate, and does disorder status separate the pattern?"""
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.scatterplot(
        data=df, x="Sleep Duration", y="Quality of Sleep",
        hue="Sleep Disorder", hue_order=DISORDER_ORDER, palette=DISORDER_PALETTE,
        s=60, alpha=0.7, ax=ax,
    )
    ax.set_title("Sleep Duration vs. Quality, by Disorder Status")
    fig.tight_layout()
    fig.savefig(f"{OUTPUT_DIR}/05_duration_vs_quality.png", dpi=150)
    plt.close(fig)


def print_summary_stats(df: pd.DataFrame) -> None:
    print("=== Sleep Disorder counts ===")
    print(df["Sleep Disorder"].value_counts())
    print()
    print("=== Mean stats by disorder ===")
    print(
        df.groupby("Sleep Disorder")[
            ["Stress Level", "Physical Activity Level", "Quality of Sleep", "Sleep Duration"]
        ].mean().round(2)
    )


if __name__ == "__main__":
    data = load_data()
    print_summary_stats(data)
    chart_stress_by_disorder(data)
    chart_activity_by_disorder(data)
    chart_bmi_vs_disorder(data)
    chart_occupation_vs_disorder(data)
    chart_sleep_duration_quality(data)
    print("\nAll charts saved to outputs/")
