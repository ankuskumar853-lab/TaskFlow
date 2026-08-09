# 🚀 TaskFlow — AI-Assisted Task Management Platform

TaskFlow is a full-stack task and project management application built with FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript.

The application allows users to create and manage projects and tasks, search and sort tasks using custom algorithms, view task statistics, and create tasks using an AI-style deterministic Quick-Add parser.

The AI Quick-Add feature does not require an API key or network connection.

---

# 📌 Features

## Task Management

- Create tasks
- List tasks
- Get a task by ID
- Update tasks
- Delete tasks
- Mark tasks as completed or pending
- Priority levels:
  - Low
  - Medium
  - High
- Optional due dates
- Tasks belong to projects

## Project Management

- Create projects
- List projects
- Get project details
- Update projects
- Delete projects

## Dashboard Statistics

The dashboard displays:

- Total tasks
- Pending tasks
- Completed tasks

## Searching

TaskFlow supports:

- Normal title search
- Linear Search
- Binary Search

## Sorting

Tasks can be sorted using the implemented algorithm:

- Priority
- Newest first
- Oldest first
- Pending first

## AI Quick-Add

Users can enter natural-language task descriptions such as:

> Finish the report next Friday, it's urgent

The deterministic parser extracts:

- Task title
- Priority
- Due-date information

The parsed task is then stored in the normal `tasks` database table.

The Quick-Add parser works without:

- API keys
- External APIs
- Network requests
- Paid services

## Offline Cache

The frontend uses browser `localStorage` to cache the latest task list.

If the backend becomes temporarily unavailable, previously loaded tasks can still be displayed.

---

# 🛠️ Tech Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn

## Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API
- Browser LocalStorage

## Algorithms

- Insertion Sort
- Linear Search
- Binary Search

## AI Quick-Add

- Deterministic rule-based parser
- Keyword detection
- Date-hint detection
- Priority detection
- No external API required

---

# 📁 Project Structure

```text
TaskFlow/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── algorithms.py
│   ├── ai_parser.py
│   ├── benchmark.py
│   ├── check_algorithms.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── .gitignore
│   │
│   └── routes/
│       ├── users.py
│       ├── projects.py
│       ├── tasks.py
│       ├── algorithms.py
│       └── quick_add.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── styles.css
│
├── README.md
└── .gitignore
```

---

# ⚙️ Environment Setup

## 1. Clone the repository

```bash
git clone https://github.com/ankuskumar853-lab/TaskFlow.git
cd TaskFlow
```

## 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install backend dependencies

```powershell
cd backend
pip install -r requirements.txt
```

---

# ▶️ Running the Application

From the project root:

```powershell
cd backend
.\..\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

The FastAPI backend will normally be available at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

Open the Swagger page in a browser to test the API.

---

# 🌐 Running the Frontend

Open the following file in a browser:

```text
frontend/index.html
```

The frontend communicates with the FastAPI backend using the Fetch API.

The frontend provides:

- Task dashboard
- Task creation
- Task editing
- Task deletion
- Task search
- Task sorting
- Quick-Add
- LocalStorage caching

---

# 🔌 API Endpoints

The following are the main endpoint categories implemented by TaskFlow.

> Request and response examples should be checked against the Swagger documentation at `/docs` if the implementation changes.

---

## 👤 Users

### Create User

```http
POST /users
```

Example request:

```json
{
  "name": "Rahul",
  "email": "rahul@example.com"
}
```

Example response:

```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@example.com"
}
```

### List Users

```http
GET /users
```

Example response:

```json
[
  {
    "id": 1,
    "name": "Rahul",
    "email": "rahul@example.com"
  }
]
```

---

# 📂 Projects

### Create Project

```http
POST /projects
```

Example request:

```json
{
  "name": "TaskFlow Development",
  "description": "Development of the TaskFlow platform"
}
```

Example response:

```json
{
  "id": 1,
  "name": "TaskFlow Development",
  "description": "Development of the TaskFlow platform"
}
```

### List Projects

```http
GET /projects
```

Example response:

```json
[
  {
    "id": 1,
    "name": "TaskFlow Development",
    "description": "Development of the TaskFlow platform"
  }
]
```

### Get Project by ID

```http
GET /projects/1
```

Example response:

```json
{
  "id": 1,
  "name": "TaskFlow Development",
  "description": "Development of the TaskFlow platform"
}
```

### Update Project

```http
PUT /projects/1
```

Example request:

```json
{
  "name": "TaskFlow Backend",
  "description": "Backend development"
}
```

### Delete Project

```http
DELETE /projects/1
```

Example response:

```json
{
  "message": "Project deleted successfully"
}
```

---

# ✅ Tasks

## Create Task

```http
POST /tasks
```

Example request:

```json
{
  "title": "Complete README",
  "description": "Finish project documentation",
  "priority": "high",
  "project_id": 1
}
```

Example response:

```json
{
  "id": 1,
  "title": "Complete README",
  "description": "Finish project documentation",
  "priority": "high",
  "completed": false,
  "project_id": 1
}
```

## List Tasks

```http
GET /tasks
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Complete README",
    "priority": "high",
    "completed": false,
    "project_id": 1
  }
]
```

## Get Task by ID

```http
GET /tasks/1
```

Example response:

```json
{
  "id": 1,
  "title": "Complete README",
  "priority": "high",
  "completed": false,
  "project_id": 1
}
```

## Update Task

```http
PUT /tasks/1
```

Example request:

```json
{
  "title": "Complete final README",
  "priority": "high",
  "completed": true
}
```

## Delete Task

```http
DELETE /tasks/1
```

Example response:

```json
{
  "message": "Task deleted successfully"
}
```

---

# 📊 Task Statistics

```http
GET /tasks/stats
```

Example response:

```json
{
  "total": 10,
  "completed": 4,
  "pending": 6
}
```

The statistics endpoint is used by the frontend dashboard.

---

# 🔢 Algorithm-Based Sorting

```http
GET /tasks?sort=priority
```

Example response:

```json
[
  {
    "id": 3,
    "title": "Fix production issue",
    "priority": "high"
  },
  {
    "id": 2,
    "title": "Update documentation",
    "priority": "medium"
  },
  {
    "id": 1,
    "title": "Clean old files",
    "priority": "low"
  }
]
```

The backend uses the custom sorting implementation rather than relying only on a database `ORDER BY`.

---

# 🔎 Algorithm-Based Search

## Linear Search

```http
GET /tasks/search?title=report&algo=linear
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Complete report",
    "priority": "high"
  }
]
```

## Binary Search

```http
GET /tasks/search?title=report&algo=binary
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Complete report",
    "priority": "high"
  }
]
```

Binary search requires the data to be ordered appropriately before searching.

---

# 🤖 AI Quick-Add

```http
POST /tasks/quick-add
```

Example request:

```json
{
  "text": "Finish the report tomorrow, urgent"
}
```

Example response:

```json
{
  "title": "Finish the report",
  "priority": "high",
  "due_date": "tomorrow"
}
```

The parser is deterministic and runs locally.

No external LLM or API is required.

---

# 🧠 Algorithms

TaskFlow implements the following algorithms.

## Insertion Sort

Insertion sort builds the sorted list one element at a time.

### Time Complexity

| Case | Complexity |
|---|---|
| Best | O(n) |
| Average | O(n²) |
| Worst | O(n²) |

### Space Complexity

```text
O(1)
```

Insertion sort is useful when the dataset is relatively small or partially sorted.

---

## Linear Search

Linear search checks elements sequentially until a matching task is found.

### Time Complexity

| Case | Complexity |
|---|---|
| Best | O(1) |
| Average | O(n) |
| Worst | O(n) |

### Space Complexity

```text
O(1)
```

---

## Binary Search

Binary search repeatedly divides a sorted dataset into two halves.

### Time Complexity

| Case | Complexity |
|---|---|
| Best | O(1) |
| Average | O(log n) |
| Worst | O(log n) |

### Space Complexity

```text
O(1)
```

Binary search is faster than linear search for large sorted datasets.

---

# 📈 Benchmarking

The project contains benchmarking utilities:

```text
backend/benchmark.py
```

The benchmark compares algorithm performance for different dataset sizes.

Example benchmark command:

```powershell
cd backend
python benchmark.py
```

Example result format:

```text
Dataset size: 100
Insertion Sort: ...
Linear Search: ...
Binary Search: ...

Dataset size: 1000
Insertion Sort: ...
Linear Search: ...
Binary Search: ...

Dataset size: 5000
Insertion Sort: ...
Linear Search: ...
Binary Search: ...
```

The exact timings depend on the computer running the benchmark.

The benchmark demonstrates that:

- Insertion Sort becomes slower as the dataset grows.
- Linear Search grows approximately linearly.
- Binary Search grows logarithmically when the data is sorted.

---

# 🤖 AI Quick-Add Design

The Quick-Add feature intentionally uses a deterministic parser instead of requiring a paid LLM.

The parser performs the following steps:

1. Receive natural-language task text.
2. Detect priority keywords.
3. Detect due-date keywords.
4. Remove or separate recognized hints.
5. Generate a clean task title.
6. Return structured task data.
7. Store the task using the normal task creation flow.

This approach makes the feature:

- Free
- Offline-capable
- Deterministic
- Easy to test
- Easy to reproduce during grading

---

# 🧩 AI Prompting / Parsing Technique Rationale

The project does not depend on an external LLM for grading.

The deterministic parser follows an intent-extraction approach.

The input is treated as a natural-language instruction containing several possible pieces of information:

```text
Task title + priority + due-date information
```

The parser identifies these pieces using predefined keywords and date phrases.

This provides predictable results and avoids dependency on:

- API availability
- API keys
- Network connectivity
- External model responses
- Paid subscriptions

---

# 📝 Five Quick-Add Examples

## Example 1

Input:

```text
Finish the project report urgently
```

Expected interpretation:

```json
{
  "title": "Finish the project report",
  "priority": "high"
}
```

## Example 2

Input:

```text
Review the pull request tomorrow
```

Expected interpretation:

```json
{
  "title": "Review the pull request",
  "due_date": "tomorrow"
}
```

## Example 3

Input:

```text
Prepare presentation next Friday, urgent
```

Expected interpretation:

```json
{
  "title": "Prepare presentation",
  "priority": "high",
  "due_date": "next Friday"
}
```

## Example 4

Input:

```text
Clean the documentation, low priority
```

Expected interpretation:

```json
{
  "title": "Clean the documentation",
  "priority": "low"
}
```

## Example 5

Input:

```text
Submit the assignment by Monday
```

Expected interpretation:

```json
{
  "title": "Submit the assignment",
  "due_date": "Monday"
}
```

---

# 💾 Database

TaskFlow uses SQLite with SQLAlchemy.

The main entities are:

- Users
- Projects
- Tasks

Tasks are associated with projects using a project relationship.

SQLite is used because it requires no separate database server and is suitable for local development and evaluation.

---

# 🔐 Security and Configuration

The required project functionality does not require any paid third-party service.

The AI Quick-Add feature uses a local deterministic parser.

No API key is required for the graded functionality.

---

# 🧪 Testing and Verification

Algorithm verification utilities are included in:

```text
backend/check_algorithms.py
```

Run:

```powershell
cd backend
python check_algorithms.py
```

The API can also be tested using FastAPI Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 CORS

The FastAPI backend is configured to allow the frontend to communicate with the API during local development.

The frontend uses JavaScript `fetch()` requests to communicate with the backend.

---

# 🗂️ Local Development Workflow

Recommended development flow:

```text
1. Create virtual environment
        ↓
2. Install requirements
        ↓
3. Start FastAPI with Uvicorn
        ↓
4. Open frontend/index.html
        ↓
5. Test API using Swagger
        ↓
6. Test task CRUD
        ↓
7. Test sorting/search
        ↓
8. Test Quick-Add
        ↓
9. Run algorithm verification
        ↓
10. Run benchmark
```

---

# 🌿 Git Workflow

The project uses Git for version control.

The repository contains the complete project in one GitHub repository.

The repository history also includes feature-branch development and merge history.

Example history:

```text
main
│
├── feature/readme
│   ├── Add tech stack
│   ├── Add project structure
│   └── Move README to project root
│
└── fix/remove-nested-repo
    ├── Remove nested repository
    └── Improve documentation
```

The feature branch was merged back into `main`.

This satisfies the project requirement for demonstrating branch-based Git workflow.

---

# 📦 Submission Requirements

The project is contained inside exactly one GitHub repository.

Repository:

```text
https://github.com/ankuskumar853-lab/TaskFlow
```

The repository contains:

```text
backend/
frontend/
README.md
```

The backend contains:

- FastAPI application
- SQLAlchemy models
- API routes
- Algorithms
- AI Quick-Add parser
- Benchmark utilities

The frontend contains:

- HTML
- CSS
- JavaScript

No screenshots, PDFs, presentations, videos, or audio files are required.

---

# ⚠️ Academic Integrity

All submitted work should be understood by the author.

Documentation and AI coding assistants may be used as learning and development aids, but the author should understand and be able to explain the submitted implementation.

---

# 🚀 Final Summary

TaskFlow combines:

- Full-stack web development
- FastAPI REST APIs
- SQLAlchemy database access
- SQLite
- JavaScript frontend
- LocalStorage caching
- Custom sorting
- Linear search
- Binary search
- Algorithm benchmarking
- Deterministic AI Quick-Add
- Git feature branches and merges

The entire project is provided through one public GitHub repository.