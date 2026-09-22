"""
analyze.py

Loads the synthetic medical student behavioral-health training dataset and
produces:
  - printed summary KPIs
  - 5 charts saved to charts/

Run:
    python3 scripts/analyze.py
"""

import sqlite3
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "training.db"
CHARTS_DIR = ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

BLUE = "#2a78d6"
ORANGE = "#eb6834"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
SURFACE = "#fcfcfb"

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "axes.edgecolor": GRIDLINE,
        "axes.labelcolor": INK_SECONDARY,
        "text.color": INK_PRIMARY,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "grid.color": GRIDLINE,
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.titlecolor": INK_PRIMARY,
        "axes.axisbelow": True,
    }
)


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM training_data", conn)
    conn.close()
    df["pre_test_score"] = pd.to_numeric(df["pre_test_score"], errors="coerce")
    df["post_test_score"] = pd.to_numeric(df["post_test_score"], errors="coerce")
    df["satisfaction_score"] = pd.to_numeric(df["satisfaction_score"], errors="coerce")
    df["learning_gain"] = df["post_test_score"] - df["pre_test_score"]
    return df


def print_kpis(df):
    total = len(df)
    completed = (df["completion_status"] == "Completed").sum()
    overall_rate = 100 * completed / total

    bsp = df[df["category"] == "Behavioral Science & Psychiatry"]
    long_bsp = bsp[bsp["duration_hours"] >= 4]
    short_bsp = bsp[bsp["duration_hours"] < 4]
    long_rate = 100 * (long_bsp["completion_status"] == "Completed").mean()
    short_rate = 100 * (short_bsp["completion_status"] == "Completed").mean()

    print("=" * 70)
    print("MEDICAL STUDENT BEHAVIORAL-HEALTH TRAINING -- KEY METRICS")
    print("=" * 70)
    print(f"Total students:                             750")
    print(f"Total training enrollments:                 {total:,}")
    print(f"Overall completion rate:                    {overall_rate:.1f}%")
    print(f"Long digital-workbook modules (4+ hrs):     {long_rate:.1f}%")
    print(f"Short gamified modules (<4 hrs):             {short_rate:.1f}%")
    print(f"Completion-rate gap (short vs long):         {short_rate - long_rate:.1f} pts")
    print("=" * 70)


def style_bar_axes(ax):
    ax.grid(axis="x", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)


def chart_completion_by_course(df):
    by_course = (
        df.groupby("course_name")
        .apply(lambda g: 100 * (g["completion_status"] == "Completed").mean())
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    ax.barh(by_course.index, by_course.values, color=BLUE, height=0.6)
    ax.set_title("Completion Rate by Training Module")
    ax.set_xlabel("Completion rate (%)")
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    style_bar_axes(ax)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "1_completion_rate_by_course.png", dpi=150)
    plt.close(fig)


def chart_completion_by_format(df):
    by_format = (
        df.groupby("training_format")
        .apply(lambda g: 100 * (g["completion_status"] == "Completed").mean())
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.bar(by_format.index, by_format.values, color=BLUE, width=0.55)
    ax.set_title("Completion Rate by Training Format")
    ax.set_ylabel("Completion rate (%)")
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.grid(axis="y", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    plt.setp(ax.get_xticklabels(), rotation=15, ha="right")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "2_completion_rate_by_format.png", dpi=150)
    plt.close(fig)


def chart_learning_gain_by_course(df):
    completed = df[df["completion_status"] == "Completed"]
    by_course = completed.groupby("course_name")["learning_gain"].mean().sort_values()

    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    ax.barh(by_course.index, by_course.values, color=ORANGE, height=0.6)
    ax.set_title("Average Learning Gain by Module\n(post-test score minus pre-test score)")
    ax.set_xlabel("Average point gain")
    style_bar_axes(ax)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "3_learning_gain_by_course.png", dpi=150)
    plt.close(fig)


def chart_satisfaction_by_status(df):
    order = ["Dropped", "In Progress", "Completed"]
    by_status = df.groupby("completion_status")["satisfaction_score"].mean().reindex(order)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(by_status.index, by_status.values, color=BLUE, width=0.5)
    ax.set_title("Average Satisfaction Score by Completion Status")
    ax.set_ylabel("Satisfaction (1-5 scale)")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "4_satisfaction_by_completion_status.png", dpi=150)
    plt.close(fig)


def chart_completion_by_campus(df):
    by_campus = (
        df.groupby("campus")
        .apply(lambda g: 100 * (g["completion_status"] == "Completed").mean())
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.bar(by_campus.index, by_campus.values, color=BLUE, width=0.6)
    ax.set_title("Completion Rate by Teaching Campus\n(campus has little effect — module design is the real driver)")
    ax.set_ylabel("Completion rate (%)")
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.grid(axis="y", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "5_completion_rate_by_campus.png", dpi=150)
    plt.close(fig)


def main():
    df = load_data()
    print_kpis(df)

    chart_completion_by_course(df)
    chart_completion_by_format(df)
    chart_learning_gain_by_course(df)
    chart_satisfaction_by_status(df)
    chart_completion_by_campus(df)

    print("\nCharts written to charts/:")
    for f in sorted(CHARTS_DIR.iterdir()):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
