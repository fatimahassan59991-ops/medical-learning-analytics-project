"""
generate_data.py

Generates a fully SYNTHETIC (fictional) randomized controlled experiment
comparing two training formats for the same mandatory behavioral-health
course content, at a fictional medical school:

  Control (Group A):    one 3-hour, single-sitting eLearning module
  Treatment (Group B):  the same content split into six 30-minute
                         microlearning modules delivered over two weeks

600 fictional medical students (a subset of the same fictional medical
school used in the companion "Medical Student Behavioral-Health Training
Effectiveness & Learning Analytics" project) are randomly assigned to one
of the two groups, stratified by teaching campus so both groups have a
near-identical campus mix.

No real medical school, student, or patient data is used anywhere here.

Run:
    python3 scripts/generate_data.py

Outputs (relative to project root):
    data/ab_test_results.csv
    data/ab_test.db   (SQLite, same table loaded)
"""

import random
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 23
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

CAMPUSES = [
    "Meridian Main Campus", "Riverside Teaching Hospital", "Lakeside Medical Center",
    "University Health Partners", "Community Health Institute",
]
N_STUDENTS = 600
COURSE_NAME = "Suicide Risk Assessment & Safety Planning"


def assign_groups_stratified(students: pd.DataFrame) -> pd.DataFrame:
    """Randomly assign Control/Treatment within each campus, ~50/50,
    so the two groups end up balanced on campus by design."""
    students = students.copy()
    students["group"] = ""
    for campus, idx in students.groupby("campus").groups.items():
        idx = list(idx)
        random.shuffle(idx)
        half = len(idx) // 2
        for i in idx[:half]:
            students.loc[i, "group"] = "Control"
        for i in idx[half:]:
            students.loc[i, "group"] = "Treatment"
    return students


def simulate_results(students: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, stu in students.iterrows():
        group = stu["group"]
        ability = np.random.normal(0, 1)  # per-student trait, independent of group (randomization)

        # --- Baseline (pre-test) is drawn the SAME way regardless of group,
        # since the test happens before either training format is delivered.
        # This is the balance check the analysis verifies.
        pre_test_score = float(np.clip(np.random.normal(60 + ability * 8, 10), 20, 95))

        # --- Completion probability differs by group (the treatment effect)
        if group == "Treatment":
            completion_prob = np.clip(0.90 + ability * 0.03 + np.random.normal(0, 0.03), 0.5, 0.99)
        else:
            completion_prob = np.clip(0.68 + ability * 0.03 + np.random.normal(0, 0.03), 0.3, 0.95)

        roll = random.random()
        if roll < completion_prob:
            status = "Completed"
        elif roll < completion_prob + (1 - completion_prob) * 0.5:
            status = "In Progress"
        else:
            status = "Dropped"

        # --- Assessment attempts
        attempts_mean = 1.3 if group == "Treatment" else 1.8
        attempts = 0 if status == "Dropped" and random.random() < 0.3 else int(
            np.clip(round(np.random.normal(attempts_mean - ability * 0.2, 0.6)), 1, 4)
        )

        # --- Post-test score & learning gain (Completed only)
        if status == "Completed":
            gain_mean = 16.0 if group == "Treatment" else 7.0
            gain = np.random.normal(gain_mean, 4.5) + ability * 3
            post_test_score = float(np.clip(pre_test_score + gain, 0, 100))
        else:
            post_test_score = None

        # --- Satisfaction (1-5)
        if status != "Not Started":
            base = 4.3 if group == "Treatment" else 3.0
            status_adj = {"Completed": 0.2, "In Progress": -0.3, "Dropped": -0.8}[status]
            satisfaction = float(np.clip(round(base + status_adj + np.random.normal(0, 0.35), 1), 1.0, 5.0))
        else:
            satisfaction = None

        # --- Completion time in calendar days.
        # Treatment is delivered over two weeks BY DESIGN (six modules,
        # spaced out), so it typically takes longer in calendar days even
        # though far more students actually finish it -- a real nuance
        # worth calling out rather than a format that "wins" on everything.
        if status == "Completed":
            if group == "Treatment":
                completion_time_days = int(np.clip(np.random.normal(13, 3), 5, 30))
            else:
                completion_time_days = int(np.clip(np.random.normal(6, 3), 1, 25))
        else:
            completion_time_days = None

        rows.append(
            {
                "student_id": stu["student_id"],
                "campus": stu["campus"],
                "group": group,
                "course_name": COURSE_NAME,
                "pre_test_score": round(pre_test_score, 1),
                "completion_status": status,
                "completion_time_days": completion_time_days if completion_time_days else "",
                "post_test_score": round(post_test_score, 1) if post_test_score is not None else "",
                "assessment_attempts": attempts,
                "satisfaction_score": satisfaction if satisfaction is not None else "",
            }
        )

    return pd.DataFrame(rows)


def main():
    print(f"Assigning {N_STUDENTS} medical students to Control/Treatment, stratified by campus...")
    students = pd.DataFrame(
        {
            "student_id": range(70001, 70001 + N_STUDENTS),
            "campus": [random.choice(CAMPUSES) for _ in range(N_STUDENTS)],
        }
    )
    students = assign_groups_stratified(students)
    print(students["group"].value_counts().to_string())

    print("\nSimulating training outcomes...")
    results = simulate_results(students)

    results.to_csv(DATA_DIR / "ab_test_results.csv", index=False)

    db_path = DATA_DIR / "ab_test.db"
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    results.to_sql("ab_test_results", conn, index=False)
    conn.commit()
    conn.close()

    print("\nDone. Files written to data/:")
    for f in sorted(DATA_DIR.iterdir()):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
