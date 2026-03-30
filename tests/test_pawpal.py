from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Scheduler


def test_task_mark_complete():
    task = Task(
        task_id="t1",
        title="Test Task",
        task_type="generic",
        scheduled_time=datetime.now(),
        priority=2,
        frequency="none",
        status="pending",
    )

    task.mark_complete()

    assert task.status == "completed"


def test_pet_add_task_increases_count():
    pet = Pet(
        pet_id="p1",
        name="Buddy",
        species="dog",
        age=3,
        breed="Labrador",
    )

    assert len(pet.tasks) == 0

    task = Task(
        task_id="t2",
        title="Feed Buddy",
        task_type="feeding",
        scheduled_time=datetime.now(),
        priority=1,
        frequency="none",
    )

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task


def test_sort_by_time_returns_chronological_order():
    pet = Pet(
        pet_id="p1",
        name="Milo",
        species="dog",
        age=4,
        breed="Beagle",
    )

    now = datetime(2026, 3, 30, 9, 0)

    task1 = Task(
        task_id="t1",
        title="Morning Walk",
        task_type="walk",
        scheduled_time=now + timedelta(hours=2),
        priority=3,
        frequency="none",
    )

    task2 = Task(
        task_id="t2",
        title="Feed Breakfast",
        task_type="feeding",
        scheduled_time=now + timedelta(hours=1),
        priority=2,
        frequency="none",
    )

    pet.add_task(task1)
    pet.add_task(task2)

    scheduler = Scheduler()
    scheduler.add_pet(pet)

    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0] == task2
    assert sorted_tasks[1] == task1


def test_daily_recurring_task_creates_next_day_task():
    pet = Pet(
        pet_id="p1",
        name="Buddy",
        species="dog",
        age=3,
        breed="Labrador",
    )

    start_time = datetime(2026, 3, 30, 9, 0)

    task = Task(
        task_id="t1",
        title="Daily Walk",
        task_type="walk",
        scheduled_time=start_time,
        priority=2,
        frequency="daily",
    )

    pet.add_task(task)

    scheduler = Scheduler()
    scheduler.add_pet(pet)

    scheduler.mark_task_complete(task)

    assert task.status == "completed"
    assert len(pet.tasks) == 2
    assert pet.tasks[1].title == "Daily Walk"
    assert pet.tasks[1].status == "pending"
    assert pet.tasks[1].scheduled_time == start_time + timedelta(days=1)


def test_conflict_detection_returns_warning():
    pet1 = Pet(
        pet_id="p1",
        name="Milo",
        species="dog",
        age=4,
        breed="Beagle",
    )

    pet2 = Pet(
        pet_id="p2",
        name="Luna",
        species="cat",
        age=2,
        breed="Siamese",
    )

    same_time = datetime(2026, 3, 30, 12, 0)

    task1 = Task(
        task_id="t1",
        title="Feed Breakfast",
        task_type="feeding",
        scheduled_time=same_time,
        priority=2,
        frequency="none",
    )

    task2 = Task(
        task_id="t2",
        title="Lunch Feeding",
        task_type="feeding",
        scheduled_time=same_time,
        priority=2,
        frequency="none",
    )

    pet1.add_task(task1)
    pet2.add_task(task2)

    scheduler = Scheduler()
    scheduler.add_pet(pet1)
    scheduler.add_pet(pet2)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Conflict detected" in conflicts[0]
    assert "Feed Breakfast" in conflicts[0]
    assert "Lunch Feeding" in conflicts[0]