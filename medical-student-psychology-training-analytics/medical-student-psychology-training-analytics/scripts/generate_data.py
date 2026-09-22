"""
generate_data.py

Generates a fully SYNTHETIC (fictional) medical student behavioral-health
training dataset for a made-up medical school ("Meridian School of
Medicine"), for practicing and demonstrating learning analytics /
instructional design skills: SQL, Python (pandas), data visualization, and
Power BI dashboarding.

No real medical school, student, or patient data is used anywhere in this
project. Student IDs are numeric and course names are invented.

Run:
    python3 scripts/generate_data.py

Outputs (relative to project root):
    data/students.csv
    data/courses.csv
    data/training_records.csv     (normalized fact table)
    data/training_data.csv        (flat, denormalized -- one row per
                                    student/course with every analysis
                                    column in one place)
    data/training.db              (SQLite, all tables + a flat view loaded)
"""

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_SEED = 17
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Medical school structure
# ---------------------------------------------------------------------------

CAMPUSES = [
    "Meridian Main Campus", "Riverside Teaching Hospital", "Lakeside Medical Center",
    "University Health Partners", "Community Health Institute",
]
CLASS_YEARS = ["M1", "M2", "M3", "M4"]
N_STUDENTS = 750

ACADEMIC_YEAR_START = date(2025, 1, 6)
ACADEMIC_YEAR_END = date(2025, 12, 19)

# ---------------------------------------------------------------------------
# Behavioral science / psychiatry curriculum
#
# The five "Behavioral Science & Psychiatry" modules are mandatory and
# assigned to every student, mirroring how psychiatric interviewing and
# mental health training is required across medical school curricula.
# Three are long, single-sitting "digital workbook" modules; two are short
# gamified microlearning modules -- built in on purpose, so the
# completion-rate and assessment gap between "long digital workbook" and
# "short gamified microlearning" is the central, discoverable finding of
# this project.
# ---------------------------------------------------------------------------

COURSES = [
    # course_id, course_name, category, format, duration_hours, mandatory
    (1, "Psychiatric Interviewing & Mental Status Examination", "Behavioral Science & Psychiatry", "Digital Workbook", 6.0, True),
    (2, "Recognizing Depression, Anxiety & Suicide Risk", "Behavioral Science & Psychiatry", "Digital Workbook", 5.5, True),
    (3, "Trauma-Informed Care & Communication", "Behavioral Science & Psychiatry", "Digital Workbook", 4.5, True),
    (4, "De-escalation Micro-Skills for Acute Distress", "Behavioral Science & Psychiatry", "Gamified Microlearning", 1.0, True),
    (5, "Empathic Communication Quick Course", "Behavioral Science & Psychiatry", "Gamified Microlearning", 1.5, True),
    (6, "Intro to Cognitive Behavioral Therapy for Primary Care", "Psychology", "Teacher-Led Virtual", 3.0, False),
    (7, "Motivational Interviewing Workshop", "Psychology", "Blended", 2.5, False),
    (8, "Physician Wellness & Burnout Prevention", "Psychology", "Teacher-Led Virtual", 4.0, False),
    (9, "Understanding Implicit Bias in Clinical Decision-Making", "Psychology", "Digital Workbook", 3.0, False),
    (10, "Peer Mentorship & Clinical Team Communication", "Leadership", "Blended", 6.0, False),
]

COURSES_DF = pd.DataFrame(
    COURSES,
    columns=["course_id", "course_name", "category", "format", "duration_hours", "mandatory"],
)

FORMAT_COMPLETION_BONUS = {
    "Gamified Microlearning": 0.06,
    "Blended": 0.02,
    "Teacher-Led Virtual": 0.00,
    "Digital Workbook": -0.03,
}
FORMAT_GAIN_BONUS = {
    "Gamified Microlearning": 4.0,
    "Blended": 2.5,
    "Teacher-Led Virtual": 1.0,
    "Digital Workbook": 0.0,
}
FORMAT_SATISFACTION_BONUS = {
    "Gamified Microlearning": 0.5,
    "Blended": 0.25,
    "Teacher-Led Virtual": 0.0,
    "Digital Workbook": -0.25,
}


def make_students() -> pd.DataFrame:
    rows = []
    for student_id in range(60001, 60001 + N_STUDENTS):
        campus = random.choice(CAMPUSES)
        class_year = random.choice(CLASS_YEARS)
        engagement = np.random.normal(0, 1)  # per-student trait, not exported
        ability = np.random.normal(0, 1)
        rows.append(
            {
                "student_id": student_id,
                "campus": campus,
                "class_year": class_year,
                "_engagement": engagement,
                "_ability": ability,
            }
        )
    return pd.DataFrame(rows)


def pick_elective_courses(rng: random.Random) -> list[int]:
    elective_ids = [c[0] for c in COURSES if not c[5]]
    k = rng.choice([1, 2, 2, 3])
    return rng.sample(elective_ids, k=min(k, len(elective_ids)))


def simulate_training_records(students: pd.DataFrame) -> pd.DataFrame:
    mandatory_ids = [c[0] for c in COURSES if c[5]]
    course_lookup = COURSES_DF.set_index("course_id")

    rows = []
    record_id = 1
    rng = random.Random(RANDOM_SEED)

    for _, stu in students.iterrows():
        course_ids = list(mandatory_ids) + pick_elective_courses(rng)

        for course_id in course_ids:
            course = course_lookup.loc[course_id]
            duration = course["duration_hours"]
            category = course["category"]
            fmt = course["format"]

            enroll_offset = rng.randint(0, (ACADEMIC_YEAR_END - ACADEMIC_YEAR_START).days - 30)
            enrollment_date = ACADEMIC_YEAR_START + timedelta(days=enroll_offset)

            duration_penalty = max(0.0, duration - 2.0) * 0.045
            category_penalty = 0.13 if (category == "Behavioral Science & Psychiatry" and duration >= 4.0) else 0.0
            format_bonus = FORMAT_COMPLETION_BONUS[fmt]
            engagement_effect = stu["_engagement"] * 0.06

            completion_prob = 0.94 - duration_penalty - category_penalty + format_bonus + engagement_effect
            completion_prob = float(np.clip(completion_prob, 0.35, 0.985))

            roll = rng.random()
            if roll < completion_prob:
                status = "Completed"
            elif roll < completion_prob + (1 - completion_prob) * 0.45:
                status = "In Progress"
            elif roll < completion_prob + (1 - completion_prob) * 0.75:
                status = "Not Started"
            else:
                status = "Dropped"

            if status == "Not Started":
                attempts = 0
            else:
                difficulty_effect = max(0.0, duration - 2.0) * 0.15
                attempts_mean = 1.3 + difficulty_effect - stu["_ability"] * 0.2
                attempts = int(np.clip(round(np.random.normal(attempts_mean, 0.7)), 1, 4))

            pre_test_score = np.clip(
                np.random.normal(58 + stu["_ability"] * 8, 10), 20, 95
            )
            if status == "Completed":
                gain = (
                    14
                    + FORMAT_GAIN_BONUS[fmt]
                    - (category_penalty * 60)
                    + stu["_ability"] * 3
                    + np.random.normal(0, 5)
                )
                post_test_score = float(np.clip(pre_test_score + gain, 0, 100))
            else:
                post_test_score = None

            pre_test_score = round(float(pre_test_score), 1)
            if post_test_score is not None:
                post_test_score = round(post_test_score, 1)

            if status == "Completed":
                base_satisfaction = 4.0
            elif status == "In Progress":
                base_satisfaction = 3.4
            elif status == "Dropped":
                base_satisfaction = 2.6
            else:
                base_satisfaction = None

            if base_satisfaction is not None:
                satisfaction = (
                    base_satisfaction
                    + FORMAT_SATISFACTION_BONUS[fmt]
                    - (0.5 if (category == "Behavioral Science & Psychiatry" and duration >= 4.0) else 0)
                    + np.random.normal(0, 0.4)
                )
                satisfaction_score = float(np.clip(round(satisfaction, 1), 1.0, 5.0))
            else:
                satisfaction_score = None

            if status == "Completed":
                training_hours = round(duration * np.random.uniform(0.85, 1.3), 1)
                completion_time_days = int(np.clip(
                    np.random.normal(duration * 3.2, duration * 1.1), 1, 120
                ))
                completion_date = enrollment_date + timedelta(days=completion_time_days)
            elif status == "In Progress":
                training_hours = round(duration * np.random.uniform(0.25, 0.7), 1)
                completion_time_days = None
                completion_date = None
            elif status == "Dropped":
                training_hours = round(duration * np.random.uniform(0.05, 0.4), 1)
                completion_time_days = None
                completion_date = None
            else:
                training_hours = 0.0
                completion_time_days = None
                completion_date = None

            rows.append(
                {
                    "record_id": record_id,
                    "student_id": stu["student_id"],
                    "course_id": course_id,
                    "enrollment_date": enrollment_date.isoformat(),
                    "completion_status": status,
                    "completion_date": completion_date.isoformat() if completion_date else "",
                    "completion_time_days": completion_time_days if completion_time_days else "",
                    "pre_test_score": pre_test_score,
                    "post_test_score": post_test_score if post_test_score is not None else "",
                    "assessment_attempts": attempts,
                    "satisfaction_score": satisfaction_score if satisfaction_score is not None else "",
                    "training_hours": training_hours,
                }
            )
            record_id += 1

    return pd.DataFrame(rows)


def main():
    print(f"Generating {N_STUDENTS} medical students across {len(CAMPUSES)} teaching sites...")
    students = make_students()

    print("Simulating course enrollments and outcomes (this takes a few seconds)...")
    records = simulate_training_records(students)
    print(f"  {len(records)} training records generated")

    students_public = students.drop(columns=["_engagement", "_ability"])
    courses_public = COURSES_DF.copy()

    students_public.to_csv(DATA_DIR / "students.csv", index=False)
    courses_public.to_csv(DATA_DIR / "courses.csv", index=False)
    records.to_csv(DATA_DIR / "training_records.csv", index=False)

    flat = records.merge(students_public, on="student_id").merge(courses_public, on="course_id")
    flat = flat.rename(columns={"format": "training_format"})
    flat_cols = [
        "student_id", "campus", "class_year", "course_name", "training_format",
        "pre_test_score", "post_test_score", "completion_status",
        "completion_time_days", "satisfaction_score", "assessment_attempts",
        "training_hours", "enrollment_date", "completion_date",
    ]
    flat = flat[flat_cols]
    flat.to_csv(DATA_DIR / "training_data.csv", index=False)

    db_path = DATA_DIR / "training.db"
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    students_public.to_sql("students", conn, index=False)
    courses_public.to_sql("courses", conn, index=False)
    records.to_sql("training_records", conn, index=False)
    conn.execute(
        """
        CREATE VIEW training_data AS
        SELECT
            r.record_id,
            s.student_id,
            s.campus,
            s.class_year,
            c.course_name,
            c.category,
            c.format AS training_format,
            c.duration_hours,
            r.enrollment_date,
            r.completion_status,
            r.completion_date,
            r.completion_time_days,
            r.pre_test_score,
            r.post_test_score,
            r.assessment_attempts,
            r.satisfaction_score,
            r.training_hours
        FROM training_records r
        JOIN students s ON s.student_id = r.student_id
        JOIN courses c ON c.course_id = r.course_id
        """
    )
    conn.execute("CREATE INDEX idx_records_student ON training_records(student_id)")
    conn.execute("CREATE INDEX idx_records_course ON training_records(course_id)")
    conn.commit()
    conn.close()

    print("\nDone. Files written to data/:")
    for f in sorted(DATA_DIR.iterdir()):
        print(f"  {f.name}")


if __name__ == "__main__":
    main()
