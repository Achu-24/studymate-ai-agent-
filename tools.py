
import csv
import math
from pathlib import Path
from langchain_core.tools import tool

DATA_FILE = Path(__file__).parent / "data" / "study_topics.csv"



def load_data():
    """Load study topics from the project's CSV file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(
                line for line in file if line.strip()
            )
            return list(reader)
    except FileNotFoundError:
        return None
    except Exception:
        return None



def clip(text, limit=1200):
    """Keep tool results short and readable."""
    return text[:limit] + "..." if len(text) > limit else text


def get_subject_topics(subject):
    """Find topics belonging to a subject."""
    if not subject or not subject.strip():
        return []

    rows = load_data()
    if rows is None:
        return None

    return [
        row for row in rows
        if row.get("subject", "").strip().lower() == subject.strip().lower()
    ]


@tool
def find_topics(subject: str) -> str:
    """Read the study dataset and find all topics for a given subject."""
    if not subject or not subject.strip():
        return "Error: Please provide a subject name."

    topics = get_subject_topics(subject)

    if topics is None:
        return "Error: Study dataset could not be loaded."

    if not topics:
        return f"No topics found for subject: {subject}."

    result = f"Topics available for {subject}:\n"

    for row in topics:
        result += (
            f"- {row['topic']} | "
            f"Difficulty: {row['difficulty']} | "
            f"Hours: {row['estimated_hours']}\n"
        )

    return clip(result)


@tool
def calculate_study_time(subject: str, daily_hours: float) -> str:
    """Calculate total study hours and required days for a subject."""
    if not subject or not subject.strip():
        return "Error: Please provide a subject name."

    try:
        daily_hours = float(daily_hours)

        if not math.isfinite(daily_hours) or daily_hours <= 0:
            return "Error: Daily study hours must be positive."

        topics = get_subject_topics(subject)

        if topics is None:
            return "Error: Study dataset could not be loaded."

        if not topics:
            return f"No topics found for subject: {subject}."

        total = sum(float(row["estimated_hours"]) for row in topics)
        days = math.ceil(total / daily_hours)

        return (
            f"Subject: {subject}\n"
            f"Total topics: {len(topics)}\n"
            f"Total study hours: {total:g}\n"
            f"Daily study hours: {daily_hours:g}\n"
            f"Required days: {days}"
        )

    except (ValueError, TypeError, KeyError):
        return "Error: Invalid study data or input."


@tool
def draft_study_plan(
    subject: str,
    available_days: int,
    daily_hours: float
) -> str:
    """Draft a study schedule using the topics, available days and daily hours."""
    if not subject or not subject.strip():
        return "Error: Please provide a subject name."

    try:
        if isinstance(available_days, bool):
            return "Error: Available days must be a positive integer."

        available_days = int(available_days)
        daily_hours = float(daily_hours)

        if available_days <= 0:
            return "Error: Available days must be positive."

        if not math.isfinite(daily_hours) or daily_hours <= 0:
            return "Error: Daily study hours must be positive."

        topics = get_subject_topics(subject)

        if topics is None:
            return "Error: Study dataset could not be loaded."

        if not topics:
            return f"No topics found for subject: {subject}."

        total = sum(float(row["estimated_hours"]) for row in topics)

        if total > available_days * daily_hours:
            return (
                f"Not enough time! This subject needs {total:g} hours, "
                f"but your available time is "
                f"{available_days * daily_hours:g} hours."
            )

        schedule = [[] for _ in range(available_days)]
        loads = [0.0] * available_days

        for row in topics:
            hours = float(row["estimated_hours"])
            day = min(range(available_days), key=lambda i: loads[i])

            schedule[day].append(row["topic"])
            loads[day] += hours

        plan = f"STUDY PLAN FOR {subject.upper()}\n\n"

        for i, topics_for_day in enumerate(schedule):
            if topics_for_day:
                plan += (
                    f"Day {i + 1} ({loads[i]:g} hours):\n"
                )
                for topic in topics_for_day:
                    plan += f"- {topic}\n"
            else:
                plan += f"Day {i + 1}: Revision and practice\n"

        plan += (
            "\nTip: Take short breaks and revise completed topics."
        )

        return clip(plan)

    except (ValueError, TypeError, KeyError):
        return "Error: Please check your study plan inputs and dataset."
