from datetime import datetime


def explain_schedule(tasks, conflicts):
    """Generate a plain-language explanation of the schedule."""
    if not tasks:
        return "No tasks are available to explain."

    explanation = []
    explanation.append(
        f"The schedule includes {len(tasks)} task(s), organized by scheduled time."
    )

    high_priority = [task for task in tasks if task.priority == 3]
    if high_priority:
        explanation.append(
            f"There are {len(high_priority)} high-priority task(s) that may need extra attention."
        )

    recurring = [task for task in tasks if task.frequency in ["daily", "weekly"]]
    if recurring:
        explanation.append(
            f"There are {len(recurring)} recurring task(s), which helps maintain consistent pet care routines."
        )

    if conflicts:
        explanation.append(
            f"The scheduler found {len(conflicts)} conflict warning(s), so the owner should review overlapping task times."
        )
    else:
        explanation.append("No scheduling conflicts were found.")

    return " ".join(explanation)


def calculate_reliability_score(tasks, conflicts):
    """Score schedule reliability from 1 to 5."""
    if not tasks:
        return 1, ["No tasks were provided."]

    score = 5
    reasons = []

    if conflicts:
        score -= 1
        reasons.append("Conflicts were detected in the schedule.")

    missing_titles = [task for task in tasks if not task.title.strip()]
    if missing_titles:
        score -= 1
        reasons.append("Some tasks are missing titles.")

    missing_types = [task for task in tasks if not task.task_type.strip()]
    if missing_types:
        score -= 1
        reasons.append("Some tasks are missing task types.")

    if not reasons:
        reasons.append("The schedule is complete and no conflicts were detected.")

    return max(score, 1), reasons


def log_ai_check(tasks, conflicts, score):
    """Log schedule reliability checks to a text file."""
    with open("reliability_log.txt", "a", encoding="utf-8") as file:
        file.write(f"[{datetime.now()}] Tasks: {len(tasks)}, Conflicts: {len(conflicts)}, Score: {score}/5\n")
        
def suggest_action(conflicts, score):
    if conflicts:
        return "Resolve conflicts before proceeding."
    elif score < 4:
        return "Review schedule for improvements."
    else:
        return "Schedule looks good."        