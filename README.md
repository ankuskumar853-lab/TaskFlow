# 🚀 TaskFlow — AI-Assisted Task Management Platform

TaskFlow is a full-stack task and project management application built with FastAPI, SQLAlchemy, JavaScript, HTML, and CSS.

It allows users to create, update, delete, search, sort, and complete tasks. It also includes an AI Quick-Add feature that converts a natural-language task description into a structured task using a deterministic rule-based parser.

---

## 📌 Features

### Task Management

- Create tasks
- View all tasks
- View a task by ID
- Update tasks
- Delete tasks
- Mark tasks as completed or pending
- Task priority:
  - Low
  - Medium
  - High
- Optional due dates
- Tasks belong to projects

### Dashboard

The frontend displays:

- Total tasks
- Pending tasks
- Completed tasks

### Search

Normal frontend search allows users to search tasks by title.

The backend also provides algorithm-based search:

- Linear Search
- Binary Search

### Sorting

Tasks can be sorted by:

- Newest First
- Oldest First
- High Priority
- Pending First

### AI Quick-Add

Users can enter a natural-language description such as:

> Finish the report next Friday, it's urgent

The parser extracts:

- Task title
- Priority
- Due-date hint

The resulting task is stored in the same `tasks` database table.

### Offline Cache

The frontend stores the latest task list in `localStorage` so previously loaded tasks can still be displayed if the backend is temporarily unavailable.

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

- Deterministic rule-based mock parser
- No API key required
- No network call required

---

# 📁 Project Structure

```text
taskflow/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── algorithms.py
│   ├── ai_parser.py
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
│   ├── styles.css
│   └── script.js
│
├── seed.py
├── check_algorithms.py
└── README.md