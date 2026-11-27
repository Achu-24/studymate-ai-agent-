from tools import (
    find_topics,
    calculate_study_time,
    draft_study_plan
)

print("\n--- READ TOOL ---")
print(find_topics.invoke({"subject": "DAA"}))

print("\n--- COMPUTE TOOL ---")
print(calculate_study_time.invoke({
    "subject": "DAA",
    "daily_hours": 2
}))

print("\n--- DRAFT TOOL ---")
print(draft_study_plan.invoke({
    "subject": "DAA",
    "available_days": 10,
    "daily_hours": 2
}))