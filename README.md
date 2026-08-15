# 🚀 TaskFlow — AI-Assisted Task Management Platform

TaskFlow is a full-stack task and project management platform built with **FastAPI, SQLAlchemy, HTML, CSS, and JavaScript**.

The application provides secure user authentication, task and project management, dashboard statistics, task searching and sorting, pagination, algorithm-based search, and an AI-assisted Quick-Add feature.

The project is designed as a single full-stack application with a FastAPI backend and a browser-based frontend dashboard.

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Tech Stack](#-tech-stack)
4. [Authentication](#-authentication)
5. [Task Management](#-task-management)
6. [Pagination](#-pagination)
7. [Project Management](#-project-management)
8. [Dashboard Statistics](#-dashboard-statistics)
9. [Searching](#-searching)
10. [Sorting](#-sorting)
11. [AI Quick-Add](#-ai-quick-add)
12. [LocalStorage](#-localstorage)
13. [Project Structure](#-project-structure)
14. [Environment Setup](#-environment-setup)
15. [Running the Application](#-running-the-application)
16. [API Endpoints](#-api-endpoints)
17. [Algorithms](#-algorithms)
18. [Benchmarking](#-benchmarking)
19. [AI Quick-Add Design](#-ai-quick-add-design)
20. [Testing and Verification](#-testing-and-verification)
21. [CORS](#-cors)
22. [Git Workflow](#-git-workflow)
23. [Academic Integrity](#-academic-integrity)
24. [Final Summary](#-final-summary)

---

# 📌 Project Overview

TaskFlow was designed as an internal task and project management platform for small engineering teams.

The application allows users to:

* Create and manage tasks
* Organize tasks inside projects
* Set task priorities
* Set task status
* Set due dates
* Search tasks
* Sort tasks
* Browse tasks using pagination
* Mark tasks as completed or pending
* Edit and delete tasks
* Create tasks using AI-style Quick-Add
* View dashboard statistics
* Register an account
* Login securely
* Logout from the dashboard

The backend and frontend communicate using HTTP requests through the Fetch API.

---

# ✨ Features

## 🔐 User Authentication

TaskFlow includes user authentication with:

* User registration
* User login
* Password validation
* Password hashing on the backend
* JWT-based authentication
* Bearer token authentication
* Protected authenticated requests
* Session/token validation
* Automatic handling of unauthorized requests
* Logout functionality

After successful login, the frontend stores the authentication token in browser `localStorage`.

The frontend uses the stored token when communicating with protected backend endpoints.

The login flow uses:

```http
POST /users/login
```

The frontend stores:

```text
access_token
token_type
```

in `localStorage`.

---

# 🔑 Authentication Flow

The authentication flow works as follows:

```text
User
  │
  ▼
Register
  │
  ▼
POST /users/
  │
  ▼
Account Created
  │
  ▼
Login
  │
  ▼
POST /users/login
  │
  ▼
FastAPI verifies credentials
  │
  ▼
JWT access token generated
  │
  ▼
Frontend stores access_token
  │
  ▼
Dashboard
  │
  ▼
Authenticated API Requests
  │
  ▼
Logout
  │
  ▼
Token removed from localStorage
```

The login implementation saves the returned access token and token type in browser storage.

---

# 🚪 Logout

TaskFlow includes a logout button on the dashboard.

When the user clicks Logout:

* `access_token` is removed from `localStorage`
* `token_type` is removed from `localStorage`
* Dashboard is hidden
* Login page is displayed again
* Login fields are cleared
* Login error messages are cleared

This prevents the previously stored authentication token from being reused by the frontend after logout.

---

# 📋 Task Management

TaskFlow supports complete task management.

Users can:

* Create tasks
* View tasks
* View a single task
* Update tasks
* Delete tasks
* Edit tasks
* Mark tasks as completed
* Mark completed tasks as pending
* Assign priorities
* Add due dates
* Assign tasks to projects

Supported priority values:

```text
low
medium
high
```

Supported task statuses include:

```text
pending
completed
```

---

# 📄 Pagination

TaskFlow also supports **task pagination**.

Pagination is used to avoid loading a very large number of tasks on a single page.

Instead of displaying every task at once, tasks can be loaded page-by-page.

Conceptually:

```text
Page 1
 ├── Task 1
 ├── Task 2
 ├── Task 3
 └── ...

Page 2
 ├── Task 11
 ├── Task 12
 ├── Task 13
 └── ...

Page 3
 ├── Task 21
 ├── Task 22
 ├── Task 23
 └── ...
```

Pagination improves the usability and scalability of the dashboard when the number of tasks becomes large.

The frontend keeps track of the currently displayed task page and requests the corresponding task data from the backend.

### Pagination Benefits

Pagination helps with:

* Large task lists
* Faster frontend rendering
* Smaller API responses
* Better browser performance
* Easier task navigation
* Improved dashboard usability

> **Note:** The exact pagination query parameters and response structure should be checked from the current FastAPI Swagger documentation at `/docs`, because those details depend on the final backend implementation.

---

# 📂 Project Management

Projects are used to organize tasks.

A task belongs to a project using:

```json
{
  "project_id": 1
}
```

TaskFlow supports:

* Creating projects
* Listing projects
* Getting a project by ID
* Updating projects
* Deleting projects
* Associating tasks with projects
* Project-level task statistics

Example project:

```json
{
  "id": 1,
  "name": "TaskFlow Development",
  "description": "Development of the TaskFlow platform",
  "owner_id": 1
}
```

---

# 📊 Dashboard Statistics

The frontend dashboard displays task statistics.

The dashboard contains:

```text
Total Tasks
Pending Tasks
Completed Tasks
```

Example:

```text
Total Tasks:     20
Pending Tasks:   12
Completed Tasks: 8
```

These statistics provide a quick overview of project progress.

---

# 🔎 Searching

TaskFlow provides multiple ways to search tasks.

## Normal Search

The dashboard provides a normal search field.

Users can search task titles and descriptions.

Example:

```text
Search:
frontend
```

The frontend filters matching tasks.

---

## Linear Search

TaskFlow also implements Linear Search.

Example:

```http
GET /algorithms/tasks/search?q=Fix
```

Linear search checks task records sequentially.

### Complexity

```text
Best Case:    O(1)
Average Case: O(n)
Worst Case:   O(n)
Space:        O(1)
```

---

## Binary Search

TaskFlow also provides Binary Search for title-based searching.

The data must first be arranged appropriately before binary search is performed.

Conceptually:

```text
1. Prepare/sort task data
2. Locate the search range
3. Divide the search range
4. Compare the middle element
5. Continue searching left or right
6. Return matching tasks
```

Binary search provides:

```text
Search: O(log n)
```

for the search operation itself when the required ordering is already available.

---

# 🔃 Sorting

TaskFlow supports task sorting.

The dashboard can sort tasks by:

* Newest first
* Oldest first
* Priority
* Pending first

Priority ordering:

```text
High
  ↓
Medium
  ↓
Low
```

Sorting makes it easier to find important or unfinished tasks.

---

# 🤖 AI Quick-Add

TaskFlow provides an AI-style Quick-Add feature.

Users can enter a natural-language task description such as:

```text
Finish the frontend tomorrow high priority
```

The Quick-Add parser extracts structured information such as:

* Task title
* Priority
* Due date
* Description

The resulting information is then used to create a normal TaskFlow task.

---

# 🧠 Deterministic AI Parser

The Quick-Add feature uses a deterministic rule-based parser.

It does not require:

* Paid API
* API key
* External LLM
* Network connection
* Paid subscription

The parser uses predefined keywords and date hints to extract task information.

This makes the feature:

* Free
* Predictable
* Reproducible
* Easy to test
* Suitable for local development
* Suitable for academic evaluation

---

# 📝 Quick-Add Examples

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

---

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

---

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

---

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

---

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

# 💾 LocalStorage

The frontend uses browser `localStorage`.

Authentication information is stored locally after successful login.

The authentication flow uses:

```text
access_token
token_type
```

The dashboard also uses browser storage for frontend-side task/session handling where required.

When the user logs out, the authentication information is removed from `localStorage`.

---

# 🛠️ Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* JWT Authentication
* Password Hashing
* Uvicorn
* PostgreSQL/SQLAlchemy-compatible database configuration

## Frontend

* HTML5
* CSS3
* JavaScript
* Fetch API
* Browser LocalStorage

## Algorithms

* Merge Sort
* Binary Search
* Linear Search

## AI Quick-Add

* Deterministic rule-based parser
* Keyword detection
* Priority detection
* Date-hint detection
* Structured task extraction

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
│   │
│   └── routes/
│       ├── __init__.py
│       ├── users.py
│       ├── projects.py
│       ├── tasks.py
│       ├── algorithms.py
│       └── quick_add.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── script.js
│   ├── auth.js
│   ├── logout.js
│   └── styles.css
│
├── README.md
└── .gitignore
```

> Keep this structure synchronized with the actual files committed to the repository.

---

# ⚙️ Environment Setup

## 1. Clone the Repository

```bash
git clone https://github.com/ankuskumar853-lab/TaskFlow.git
cd TaskFlow
```

---

## 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

# 📦 Install Dependencies

Move into the backend directory:

```powershell
cd backend
```

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

---

# ▶️ Running the Backend

From the `backend` directory:

```powershell
uvicorn main:app --reload
```

The FastAPI server will normally run at:

```text
http://127.0.0.1:8000
```

---

# 📚 Swagger API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger can be used to:

* View available endpoints
* Check request schemas
* Check response schemas
* Test API endpoints
* Test authenticated endpoints
* Verify pagination parameters
* Test task CRUD
* Test search
* Test algorithms
* Test Quick-Add

---

# 🌐 Running the Frontend

Open the `frontend` directory using VS Code Live Server.

Recommended:

```text
frontend/index.html
```

Right-click:

```text
Open with Live Server
```

The frontend can then communicate with the FastAPI backend running on:

```text
http://127.0.0.1:8000
```

Both backend and frontend should be running during development.

---

# 🔌 API Endpoints

The exact endpoint schemas should always be verified against the current Swagger documentation because the backend implementation is the source of truth.

## 👤 Users

### Create User

```http
POST /users/
```

Example request:

```json
{
  "name": "Rahul",
  "email": "rahul@example.com",
  "password": "password123"
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

---

### Login

```http
POST /users/login
```

Example request:

```json
{
  "email": "rahul@example.com",
  "password": "password123"
}
```

Example response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

The frontend stores the returned token in `localStorage`.

---

### List Users

```http
GET /users/
```

---

### Get User by ID

```http
GET /users/{user_id}
```

---

# 📂 Projects

### Create Project

```http
POST /projects/
```

Example request:

```json
{
  "name": "TaskFlow Development",
  "description": "Development of the TaskFlow platform",
  "owner_id": 1
}
```

---

### List Projects

```http
GET /projects/
```

---

### Get Project by ID

```http
GET /projects/{project_id}
```

---

### Project Statistics

```http
GET /projects/stats
```

Example response:

```json
[
  {
    "project_id": 1,
    "project_name": "TaskFlow Development",
    "total_tasks": 5,
    "pending_tasks": 2,
    "in_progress_tasks": 2,
    "completed_tasks": 1
  }
]
```

---

# ✅ Tasks

## Create Task

```http
POST /tasks/
```

Example request:

```json
{
  "title": "Complete README",
  "description": "Finish project documentation",
  "priority": "high",
  "due_date": "2026-08-20",
  "status": "pending",
  "project_id": 1
}
```

---

## List Tasks

```http
GET /tasks/
```

The task listing supports pagination in the current implementation.

Use the Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

to see the exact pagination parameters and response structure implemented in the current version.

---

## Get Task by ID

```http
GET /tasks/{task_id}
```

Example:

```http
GET /tasks/1
```

---

## Update Task

```http
PUT /tasks/{task_id}
```

Example request:

```json
{
  "status": "completed",
  "priority": "high"
}
```

---

## Delete Task

```http
DELETE /tasks/{task_id}
```

Example response:

```json
{
  "message": "Task deleted successfully"
}
```

---

# 📄 Pagination Workflow

The task pagination workflow is:

```text
Frontend
   │
   ▼
Request task page
   │
   ▼
FastAPI
   │
   ▼
Database query
   │
   ▼
Requested page of tasks
   │
   ▼
JSON response
   │
   ▼
Frontend renders current page
```

When the user changes the page, the frontend requests the corresponding page of tasks instead of loading the entire task collection again.

This becomes especially useful as the number of tasks increases.

---

# 📊 Task Statistics

The dashboard provides statistics for:

```text
Total Tasks
Pending Tasks
Completed Tasks
```

These values are displayed in the TaskFlow dashboard.

---

# 🔢 Algorithms Engine

TaskFlow contains a custom algorithms engine.

The project includes:

* Merge Sort
* Binary Search
* Linear Search

These algorithms are used for task ordering and searching.

---

# 🧮 Merge Sort

Merge Sort is used for task sorting in the algorithms engine.

The sorting process:

```text
1. Divide the list
2. Recursively sort each half
3. Merge the sorted halves
```

### Time Complexity

```text
Best Case:    O(n log n)
Average Case: O(n log n)
Worst Case:   O(n log n)
```

### Space Complexity

```text
O(n)
```

---

# 🔎 Binary Search

Binary Search works on appropriately ordered data.

The basic process is:

```text
1. Find middle element
2. Compare with search value
3. Search left half or right half
4. Continue until match is found
```

### Time Complexity

```text
Search: O(log n)
```

The overall endpoint can include additional work if the data must first be sorted.

---

# 🔍 Linear Search

Linear Search checks elements one by one.

### Time Complexity

```text
Best Case:    O(1)
Average Case: O(n)
Worst Case:   O(n)
```

### Space Complexity

```text
O(1)
```

---

# 📈 Benchmarking

The project contains benchmarking utilities.

Example:

```powershell
cd backend
python benchmark.py
```

The benchmark can be used to compare algorithm performance for different dataset sizes.

Typical expected behaviour:

```text
Dataset size increases
        ↓
Insertion/Merge sorting work increases
        ↓
Linear Search grows approximately linearly
        ↓
Binary Search remains logarithmic for the search operation
```

Exact benchmark timings depend on:

* Computer hardware
* Python version
* Database state
* Dataset size
* Operating system
* Current system load

Therefore benchmark timings should be generated on the machine running the project rather than copied from another machine.

---

# 🤖 AI Quick-Add Design

The Quick-Add feature follows this workflow:

```text
Natural Language Input
        ↓
Priority Detection
        ↓
Due-Date Detection
        ↓
Title Extraction
        ↓
Structured Task Data
        ↓
Task Creation
        ↓
Database
```

Example:

```text
Finish the frontend tomorrow high priority
```

can be interpreted as:

```json
{
  "title": "Finish the frontend",
  "priority": "high",
  "due_date": "tomorrow"
}
```

The resulting task uses the same normal task database as manually created tasks.

---

# 🧩 AI Prompting / Parsing Technique Rationale

The Quick-Add parser uses a deterministic extraction approach.

The input can contain:

```text
Task title + priority + due date
```

The parser identifies these components using predefined rules.

The main stages are:

1. Receive task text.
2. Detect priority keywords.
3. Detect due-date phrases.
4. Remove recognized hints where appropriate.
5. Generate the task title.
6. Build structured task information.
7. Store the task using the normal task workflow.

This approach provides predictable results without requiring an external AI service.

---

# 🧪 Testing and Verification

TaskFlow can be tested using FastAPI Swagger.

Open:

```text
http://127.0.0.1:8000/docs
```

Recommended testing order:

```text
1. Register a user
        ↓
2. Login
        ↓
3. Receive JWT access token
        ↓
4. Open dashboard
        ↓
5. Create a project
        ↓
6. Create tasks
        ↓
7. Test task pagination
        ↓
8. Test task update
        ↓
9. Test task completion
        ↓
10. Test task deletion
        ↓
11. Test normal search
        ↓
12. Test algorithm search
        ↓
13. Test sorting
        ↓
14. Test AI Quick-Add
        ↓
15. Test logout
```

---

# 🔐 Protected Requests

Authenticated requests use the JWT access token.

The frontend sends the token using the Bearer authentication format:

```http
Authorization: Bearer <access_token>
```

If the backend returns:

```http
401 Unauthorized
```

the frontend can clear the stored authentication information and redirect the user to the login page.

This prevents an invalid or expired session from continuing to access protected functionality.

---

# 🌐 CORS

The FastAPI backend is configured to allow the frontend to communicate with the API during local development.

The frontend uses JavaScript `fetch()` requests to communicate with FastAPI.

The backend and frontend should therefore be started together during local development.

---

# 🗃️ Database

TaskFlow uses SQLAlchemy for database access.

The main entities are:

```text
Users
Projects
Tasks
```

The relationships allow tasks to belong to projects.

The database configuration is handled by the backend database module.

---

# 📦 Requirements

Backend dependencies are stored in:

```text
backend/requirements.txt
```

Install them using:

```powershell
pip install -r requirements.txt
```

---

# 🗂️ Local Development Workflow

Recommended development workflow:

```text
1. Clone repository
        ↓
2. Create virtual environment
        ↓
3. Activate virtual environment
        ↓
4. Install requirements
        ↓
5. Start FastAPI
        ↓
6. Open frontend using Live Server
        ↓
7. Register account
        ↓
8. Login
        ↓
9. Create project
        ↓
10. Create tasks
        ↓
11. Test pagination
        ↓
12. Test CRUD
        ↓
13. Test search
        ↓
14. Test sorting
        ↓
15. Test algorithms
        ↓
16. Test AI Quick-Add
        ↓
17. Test logout
        ↓
18. Run verification/benchmark scripts
```

---

# 🌿 Git Workflow

The project uses Git for version control.

The complete TaskFlow application is maintained in one repository.

Example feature-branch workflow:

```bash
git checkout -b feature/core-app
```

Make changes and commit:

```bash
git add .
git commit -m "feat: add task management functionality"
```

Additional feature commit:

```bash
git add .
git commit -m "feat: add authentication and pagination"
```

Merge back into main:

```bash
git checkout main
git merge feature/core-app --no-ff
```

View the repository history:

```bash
git log --graph --all --oneline
```

The project requirement is to demonstrate a feature branch that contains multiple commits and is merged back into `main`.

---

# 🚀 Main Application Components

TaskFlow consists of the following major components:

```text
                    TaskFlow
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
 Authentication     Dashboard      Backend API
        │              │              │
        │              │              │
        ▼              ▼              ▼
 Login/Register     Tasks/Stats    FastAPI
 Logout             Search         SQLAlchemy
 JWT                Sorting        Database
                    Pagination
                    Quick-Add
                       │
                       ▼
                  Algorithms
```

---

# 🎯 Key Project Capabilities

TaskFlow combines:

* Full-stack web development
* FastAPI REST APIs
* SQLAlchemy database access
* User registration
* User login
* JWT authentication
* Bearer token authorization
* Logout functionality
* Password security
* Task CRUD
* Project management
* Task pagination
* Dashboard statistics
* Normal task search
* Linear Search
* Binary Search
* Merge Sort
* AI Quick-Add
* Browser LocalStorage
* API integration using Fetch
* Git feature-branch workflow

---

# ⚠️ Important Development Notes

## Backend

Always start FastAPI before testing frontend API functionality:

```powershell
uvicorn main:app --reload
```

## Frontend

Open the frontend using a local development server such as VS Code Live Server.

## Authentication

Login must be completed before using protected dashboard functionality.

## Pagination

For the exact current pagination parameters and response structure, use the current Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

This keeps the README synchronized with the actual backend implementation.

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

Swagger should be considered the authoritative source for the exact request and response schemas of the current implementation.

---

# 📦 Submission Structure

The project is intended to be submitted as one GitHub repository containing:

```text
TaskFlow/
├── backend/
├── frontend/
├── README.md
└── .gitignore
```

The repository contains the complete full-stack application.

---

# 🔗 Repository

GitHub repository:

```text
https://github.com/ankuskumar853-lab/TaskFlow
```

---

# 🧠 Academic Integrity

The project should be understood by its author.

Documentation and AI coding assistants may be used as learning and development aids, but the author should understand and be able to explain the implementation submitted with the project.

---

# 🚀 Final Summary

TaskFlow is a full-stack AI-assisted task management platform that combines:

```text
FastAPI
+
SQLAlchemy
+
Database
+
HTML
+
CSS
+
JavaScript
+
JWT Authentication
+
Login/Register
+
Logout
+
Task CRUD
+
Project Management
+
Pagination
+
Task Search
+
Task Sorting
+
Merge Sort
+
Linear Search
+
Binary Search
+
AI Quick-Add
+
LocalStorage
+
Git
```

The application provides a complete workflow from user authentication to task creation, task management, searching, sorting, pagination, AI Quick-Add, and logout.

The entire project is maintained inside one GitHub repository.
