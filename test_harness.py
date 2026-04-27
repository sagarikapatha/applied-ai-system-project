from datetime import datetime, timedelta
from pawpal_system import Pet, Task, Scheduler
from ai_helper import explain_schedule, calculate_reliability_score


def run_test_case(name, tasks):
    scheduler = Scheduler()
    pet = Pet("p1", "TestPet", "dog", 3, "lab")

    for task in tasks:
        pet.add_task(task)

    scheduler.add_pet(pet)

    sorted_tasks = scheduler.sort_by_time()
    conflicts = scheduler.detect_conflicts()
    explanation = explain_schedule(sorted_tasks, conflicts)
    score, _ = calculate_reliability_score(sorted_tasks, conflicts)

    print(f"\n=== {name} ===")
    print(f"Tasks: {len(tasks)}")
    print(f"Conflicts: {len(conflicts)}")
    print(f"Score: {score}/5")
    print(f"Explanation: {explanation}")


def main():
    now = datetime.now()

    # Test 1: No conflict
    run_test_case(
        "No Conflict",
        [
            Task("t1", "Walk", "exercise", now, 2),
            Task("t2", "Feed", "feeding", now + timedelta(hours=1), 2),
        ],
    )

    # Test 2: Conflict
    run_test_case(
        "Conflict Case",
        [
            Task("t3", "Feed", "feeding", now, 2),
            Task("t4", "Feed", "feeding", now, 2),
        ],
    )

    # Test 3: Empty input
    run_test_case("Empty Case", [])


if __name__ == "__main__":
    main()