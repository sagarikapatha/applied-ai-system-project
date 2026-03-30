import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

st.subheader("Owner Information")
owner_name = st.text_input("Owner name")

# Initialize session state objects
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id="o1", name=owner_name, contact_info="")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 1

owner = st.session_state.owner
scheduler = st.session_state.scheduler
owner.name = owner_name

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name")
species = st.selectbox("Species", ["Select species", "dog", "cat", "other"])
custom_species = ""
if species == "other":
    custom_species = st.text_input("Please specify the species", key="custom_species")
age = st.number_input("Age", min_value=0)
breed = st.text_input("Breed")

if st.button("Add Pet"):
    # determine final species
    final_species = custom_species.strip() if species == "other" else species

    pet_id = f"p{st.session_state.pet_counter}"
    st.session_state.pet_counter += 1

    new_pet = Pet(
        pet_id=pet_id,
        name=pet_name,
        species=final_species,
        age=age,
        breed=breed
    )

    owner.add_pet(new_pet)
    scheduler.add_pet(new_pet)

    st.success(f"Added pet: {pet_name}")

st.subheader("Your Pets")
pets = owner.view_pets()
if pets:
    for pet in pets:
        st.write(f"- {pet.name} ({pet.species}, {pet.age} years old, {pet.breed})")
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")
st.caption("Add tasks to a pet and use the scheduler to build a daily plan.")

if pets:
    pet_labels = [f"{pet.name} ({pet.pet_id})" for pet in pets]
    selected_label = st.selectbox("Select pet", pet_labels)
    selected_pet = pets[pet_labels.index(selected_label)]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title")
    with col2:
        task_type = st.text_input("Task type")
    with col3:
        priority_label = st.selectbox("Priority", ["Select Priority", "low", "medium", "high"])

    scheduled_time = st.datetime_input("Scheduled time")
    frequency = st.selectbox("Frequency", ["none", "daily", "weekly"], index=0)

    priority_map = {"low": 1, "medium": 2, "high": 3}

    if "task_counter" not in st.session_state:
        st.session_state.task_counter = 1

    if st.button("Add Task"):
        new_task = Task(
            task_id=f"t{st.session_state.task_counter}",
            title=task_title,
            task_type=task_type,
            scheduled_time=scheduled_time,
            priority=priority_map[priority_label],
            frequency=frequency,
        )
        st.session_state.task_counter += 1
        selected_pet.add_task(new_task)
        st.success(f"Added task '{task_title}' for {selected_pet.name}")
else:
    st.info("Add a pet first before creating tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a sorted schedule and review any conflicts.")

if st.button("Generate Schedule"):
    sorted_tasks = scheduler.sort_by_time()

    if sorted_tasks:
        schedule_rows = []
        for task in sorted_tasks:
            pet_name = next((pet.name for pet in scheduler.pets if task in pet.tasks), "Unknown")
            schedule_rows.append(
                {
                    "Time": task.scheduled_time.strftime("%Y-%m-%d %H:%M"),
                    "Pet": pet_name,
                    "Task": task.title,
                    "Type": task.task_type,
                    "Status": task.status,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                }
            )

        st.success("Schedule generated successfully.")
        st.info("Tasks are sorted by scheduled time so the owner can easily follow the daily plan.")
        st.dataframe(schedule_rows, use_container_width=True)
    else:
        st.info("No tasks available to schedule.")

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No task conflicts detected.")
