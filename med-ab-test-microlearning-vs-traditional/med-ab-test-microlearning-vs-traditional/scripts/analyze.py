"""
analyze.py

Runs the statistical analysis for the microlearning vs. traditional
training A/B test: a balance check, the primary significance tests, effect
sizes, and 5 charts (including a confidence-interval / effect-size plot).

Run:
    python3 scripts/analyze.py
"""

import sqlite3
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "ab_test.db"
CHARTS_DIR = ROOT / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

BLUE = "#2a78d6"     # Control
ORANGE = "#eb6834"   # Treatment
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

GROUP_COLOR = {"Control": BLUE, "Treatment": ORANGE}


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql('SELECT * FROM ab_test_results', conn)
    conn.close()
    df["post_test_score"] = pd.to_numeric(df["post_test_score"], errors="coerce")
    df["satisfaction_score"] = pd.to_numeric(df["satisfaction_score"], errors="coerce")
    df["completion_time_days"] = pd.to_numeric(df["completion_time_days"], errors="coerce")
    return df


def two_proportion_ztest(x1, n1, x2, n2):
    """Two-sided two-proportion z-test. Returns z, p, diff, 95% CI for diff."""
    p1, p2 = x1 / n1, x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se_pooled = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se_pooled
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    se_unpooled = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    diff = p1 - p2
    ci_low = diff - 1.96 * se_unpooled
    ci_high = diff + 1.96 * se_unpooled
    return z, p_value, diff, (ci_low, ci_high)


def cohens_d(a, b):
    n1, n2 = len(a), len(b)
    pooled_std = np.sqrt(((n1 - 1) * a.std(ddof=1) ** 2 + (n2 - 1) * b.std(ddof=1) ** 2) / (n1 + n2 - 2))
    return (a.mean() - b.mean()) / pooled_std


def run_stats(df):
    control = df[df["group"] == "Control"]
    treatment = df[df["group"] == "Treatment"]

    print("=" * 70)
    print("TRAINING A/B TEST: MICROLEARNING (Treatment) vs. TRADITIONAL (Control)")
    print("=" * 70)
    print(f"Control n = {len(control)}   |   Treatment n = {len(treatment)}\n")

    # --- 0. Balance check on pre-test score ---------------------------------
    t_bal, p_bal = stats.ttest_ind(control["pre_test_score"], treatment["pre_test_score"])
    print("[Balance check] Pre-test score (should NOT be significant)")
    print(f"  Control mean = {control['pre_test_score'].mean():.1f}, "
          f"Treatment mean = {treatment['pre_test_score'].mean():.1f}")
    print(f"  t = {t_bal:.2f}, p = {p_bal:.3f}  -> "
          f"{'groups balanced (good)' if p_bal > 0.05 else 'WARNING: groups not balanced'}\n")

    # --- 1. Completion rate: two-proportion z-test --------------------------
    x1 = (treatment["completion_status"] == "Completed").sum()
    n1 = len(treatment)
    x2 = (control["completion_status"] == "Completed").sum()
    n2 = len(control)
    z, p_val, diff, ci = two_proportion_ztest(x1, n1, x2, n2)
    print("[Primary outcome] Completion rate")
    print(f"  Treatment: {x1}/{n1} = {100*x1/n1:.1f}%   Control: {x2}/{n2} = {100*x2/n2:.1f}%")
    print(f"  Difference (Treatment - Control) = {100*diff:.1f} points, "
          f"95% CI [{100*ci[0]:.1f}, {100*ci[1]:.1f}]")
    print(f"  z = {z:.2f}, p = {p_val:.6f}  -> "
          f"{'statistically significant (p < 0.05)' if p_val < 0.05 else 'not significant'}\n")

    # --- 2. Post-test score: t-test + Cohen's d -----------------------------
    ctrl_scores = control.loc[control["completion_status"] == "Completed", "post_test_score"].dropna()
    treat_scores = treatment.loc[treatment["completion_status"] == "Completed", "post_test_score"].dropna()
    t_score, p_score = stats.ttest_ind(treat_scores, ctrl_scores)
    d = cohens_d(treat_scores, ctrl_scores)
    mean_diff = treat_scores.mean() - ctrl_scores.mean()
    se_diff = np.sqrt(treat_scores.var(ddof=1) / len(treat_scores) + ctrl_scores.var(ddof=1) / len(ctrl_scores))
    ci_low, ci_high = mean_diff - 1.96 * se_diff, mean_diff + 1.96 * se_diff
    print("[Secondary outcome] Post-test score (completers only)")
    print(f"  Treatment mean = {treat_scores.mean():.1f}   Control mean = {ctrl_scores.mean():.1f}")
    print(f"  Difference = {mean_diff:.1f} points, 95% CI [{ci_low:.1f}, {ci_high:.1f}]")
    print(f"  t = {t_score:.2f}, p = {p_score:.6f}, Cohen's d = {d:.2f} "
          f"({'large' if abs(d) >= 0.8 else 'medium' if abs(d) >= 0.5 else 'small'} effect)\n")

    # --- 3. Satisfaction: Mann-Whitney U (ordinal scale) --------------------
    ctrl_sat = control["satisfaction_score"].dropna()
    treat_sat = treatment["satisfaction_score"].dropna()
    u_stat, p_sat = stats.mannwhitneyu(treat_sat, ctrl_sat, alternative="two-sided")
    print("[Secondary outcome] Satisfaction score (1-5 scale, Mann-Whitney U)")
    print(f"  Treatment median = {treat_sat.median():.1f}   Control median = {ctrl_sat.median():.1f}")
    print(f"  U = {u_stat:.0f}, p = {p_sat:.6f}  -> "
          f"{'statistically significant' if p_sat < 0.05 else 'not significant'}\n")

    # --- 4. Completion time (a nuance, not just "treatment wins") -----------
    ctrl_days = control.loc[control["completion_status"] == "Completed", "completion_time_days"].dropna()
    treat_days = treatment.loc[treatment["completion_status"] == "Completed", "completion_time_days"].dropna()
    print("[Nuance] Calendar days to complete (completers only)")
    print(f"  Treatment mean = {treat_days.mean():.1f} days   Control mean = {ctrl_days.mean():.1f} days")
    print("  (Treatment is delivered over 2 weeks by design, so it takes longer in calendar")
    print("   time even though far more students actually finish it.)")
    print("=" * 70)

    return {
        "completion_diff_pct": 100 * diff,
        "completion_ci": (100 * ci[0], 100 * ci[1]),
        "completion_p": p_val,
        "score_diff": mean_diff,
        "score_ci": (ci_low, ci_high),
        "score_p": p_score,
        "cohens_d": d,
    }


def chart_completion_rate(df):
    summary = df.groupby("group")["completion_status"].apply(lambda s: (s == "Completed").mean() * 100)
    n = df.groupby("group").size()
    # 95% CI for each proportion (normal approximation)
    ci = {}
    for g in ["Control", "Treatment"]:
        p = summary[g] / 100
        se = np.sqrt(p * (1 - p) / n[g])
        ci[g] = 1.96 * se * 100

    groups = ["Control", "Treatment"]
    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.bar(groups, [summary[g] for g in groups], yerr=[ci[g] for g in groups],
           color=[GROUP_COLOR[g] for g in groups], width=0.5, capsize=6)
    ax.set_title("Completion Rate: Traditional vs. Microlearning\n(error bars = 95% confidence interval)")
    ax.set_ylabel("Completion rate (%)")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "1_completion_rate_by_group.png", dpi=150)
    plt.close(fig)


def chart_score_distribution(df):
    ctrl = df[(df["group"] == "Control") & (df["completion_status"] == "Completed")]["post_test_score"].dropna()
    treat = df[(df["group"] == "Treatment") & (df["completion_status"] == "Completed")]["post_test_score"].dropna()

    fig, ax = plt.subplots(figsize=(7.5, 5))
    bins = np.linspace(30, 100, 20)
    ax.hist(ctrl, bins=bins, alpha=0.65, color=BLUE, label="Control (Traditional)")
    ax.hist(treat, bins=bins, alpha=0.65, color=ORANGE, label="Treatment (Microlearning)")
    ax.set_title("Post-Test Score Distribution (Completers Only)")
    ax.set_xlabel("Post-test score")
    ax.set_ylabel("Number of students")
    ax.legend(frameon=False)
    ax.grid(axis="y", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "2_post_test_score_distribution.png", dpi=150)
    plt.close(fig)


def chart_pre_vs_post(df):
    completed = df[df["completion_status"] == "Completed"]
    means = completed.groupby("group")[["pre_test_score", "post_test_score"]].mean()
    groups = ["Control", "Treatment"]
    x = np.arange(len(groups))
    width = 0.32

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(x - width / 2, [means.loc[g, "pre_test_score"] for g in groups], width,
           color=INK_MUTED, label="Pre-test")
    ax.bar(x + width / 2, [means.loc[g, "post_test_score"] for g in groups], width,
           color=[GROUP_COLOR[g] for g in groups], label="Post-test")
    ax.set_xticks(x)
    ax.set_xticklabels(groups)
    ax.set_title("Pre- vs. Post-Test Scores by Group\n(both groups started even; the gap opens up after training)")
    ax.set_ylabel("Average score")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False)
    ax.grid(axis="y", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "3_pre_vs_post_scores.png", dpi=150)
    plt.close(fig)


def chart_satisfaction(df):
    means = df.groupby("group")["satisfaction_score"].mean()
    groups = ["Control", "Treatment"]

    fig, ax = plt.subplots(figsize=(6.5, 5))
    ax.bar(groups, [means[g] for g in groups], color=[GROUP_COLOR[g] for g in groups], width=0.5)
    ax.set_title("Average Satisfaction Score by Group")
    ax.set_ylabel("Satisfaction (1-5 scale)")
    ax.set_ylim(0, 5)
    ax.grid(axis="y", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "4_satisfaction_by_group.png", dpi=150)
    plt.close(fig)


def chart_effect_sizes(results):
    labels = [
        "Completion rate\n(percentage points)",
        "Post-test score\n(points)",
    ]
    diffs = [results["completion_diff_pct"], results["score_diff"]]
    los = [results["completion_ci"][0], results["score_ci"][0]]
    his = [results["completion_ci"][1], results["score_ci"][1]]
    errs = [[d - lo for d, lo in zip(diffs, los)], [hi - d for d, hi in zip(diffs, his)]]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    y_pos = np.arange(len(labels))
    ax.errorbar(diffs, y_pos, xerr=errs, fmt="o", color=ORANGE, ecolor=INK_SECONDARY,
                elinewidth=2, capsize=5, markersize=9)
    ax.axvline(0, color=INK_MUTED, linewidth=1, linestyle="--")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_ylim(-0.5, len(labels) - 0.5)
    ax.set_xlabel("Treatment - Control (95% confidence interval)")
    ax.set_title(
        "Effect Size Summary\n(intervals that don't cross zero are statistically significant)",
        fontsize=12,
    )
    ax.grid(axis="x", linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(CHARTS_DIR / "5_effect_size_summary.png", dpi=150)
    plt.close(fig)


def main():
    df = load_data()
    results = run_stats(df)

    chart_completion_rate(df)
    chart_score_distribution(df)
    chart_pre_vs_post(df)
    chart_satisfaction(df)
    chart_effect_sizes(results)

    print("\nCharts written to charts/:")
    for f in sorted(CHARTS_DIR.iterdir()):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
