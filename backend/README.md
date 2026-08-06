# 🚀 TaskFlow

## AI-Assisted Task Management Platform

TaskFlow is a full-stack task management application developed using FastAPI, PostgreSQL (Supabase), HTML, CSS, and JavaScript.

The application allows users to create projects, manage tasks, search and sort tasks, use AI to generate tasks from natural language, and track project progress.

## ✨ Features

- Create Project
- View Projects
- Create Task
- Update Task
- Delete Task
- AI Quick Add
- Search Tasks
- Sort Tasks
- Task Status (Pending / Completed)
- Project Statistics Dashboard
- Benchmark Testing


## Tech Stack

- FastAPI
- SQLAlchemy
- Supabase
- HTML
- CSS
- JavaScript

## Project Structure

backend/
frontend/
README.md


## 🛠 Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL (Supabase)
- Pydantic

### Frontend
- HTML
- CSS
- JavaScript

### Algorithms
- Insertion Sort
- Binary Search
- Linear Search

## 📁 Project Structure

backend/
│── routes/
│ ├── projects.py
│ ├── tasks.py
│ ├── algorithms.py
│ └── quick_add.py
│
│── main.py
│── database.py
│── models.py
│── schemas.py
│── ai_parser.py
│── algorithms.py
│── benchmark.py
│── requirements.txt
│── README.md2

## ⚙️ Installation

### Clone the repository

```bash
git clone <repository-url>
```

### Go to project folder

```bash
cd backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment (Windows)

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run FastAPI

```bash
uvicorn main:app --reload
```

## 📌 API Endpoints

### Projects

- POST /projects
- GET /projects

### Tasks

- POST /tasks
- GET /tasks
- GET /tasks/{id}
- PUT /tasks/{id}
- DELETE /tasks/{id}

### AI Quick Add

- POST /quick-add

### Algorithms

- GET /algorithms/tasks/sort
- GET /algorithms/tasks/search

### Statistics

- GET /tasks/stats/projects

## 👨‍💻 Author

**DHEERAJ KUMAR**

Built as a Full-Stack AI-Assisted Task Management Platform using FastAPI, PostgreSQL (Supabase), HTML, CSS, and JavaScript.