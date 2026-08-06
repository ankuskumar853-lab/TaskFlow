from database import SessionLocal, engine, Base
import models

# Create Tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# -----------------------
# Create Sample User
# -----------------------
user = models.User(
    name="Rahul",
    email="rahul@gmail.com"
)

db.add(user)
db.commit()
db.refresh(user)

# -----------------------
# Create Sample Project
# -----------------------
project = models.Project(
    name="TaskFlow Project",
    owner_id=user.id
)

db.add(project)
db.commit()
db.refresh(project)

# -----------------------
# Sample Tasks
# -----------------------
tasks = [

    models.Task(
        title="Complete Backend",
        description="Finish FastAPI APIs",
        status="pending",
        priority="high",
        due_date="tomorrow",
        project_id=project.id
    ),

    models.Task(
        title="Build Frontend",
        description="HTML CSS JS",
        status="pending",
        priority="medium",
        due_date="next week",
        project_id=project.id
    ),

    models.Task(
        title="Write README",
        description="Documentation",
        status="pending",
        priority="low",
        due_date="friday",
        project_id=project.id
    )

]

db.add_all(tasks)
db.commit()

print("✅ Sample Data Added Successfully")

db.close()