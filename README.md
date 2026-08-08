const API_URL = "http://127.0.0.1:8000";

const taskForm = document.getElementById("taskForm");
const taskList = document.getElementById("taskList");
const titleError = document.getElementById("titleError");

const deleteModal = document.getElementById("deleteModal");
const confirmDelete = document.getElementById("confirmDelete");
const cancelDelete = document.getElementById("cancelDelete");
const successToast = document.getElementById("successToast");
const searchTask = document.getElementById("searchTask");
const sortTasks = document.getElementById("sortTasks");

let editingTaskId = null;
let deleteTaskId = null;

// ===============================
// Load Tasks
// ===============================
async function loadTasks() {

    taskList.innerHTML = "";

    try {

        const response = await fetch(`${API_URL}/tasks/`);

        const tasks = await response.json();

        const sortValue = sortTasks.value;

if (sortValue === "oldest") {

    tasks.sort((a, b) => a.id - b.id);

}

else if (sortValue === "newest") {

    tasks.sort((a, b) => b.id - a.id);

}

else if (sortValue === "priority") {

    const order = {
        high: 1,
        medium: 2,
        low: 3
    };

    tasks.sort((a, b) => order[a.priority] - order[b.priority]);

}

else if (sortValue === "status") {

    tasks.sort((a, b) => {
        if (a.status === "pending" && b.status !== "pending") return -1;
        if (a.status !== "pending" && b.status === "pending") return 1;
        return 0;
    });

}



        document.getElementById("totalTasks").innerText = tasks.length;

const pending = tasks.filter(
    task => task.status === "pending"
).length;

document.getElementById("pendingTasks").innerText = pending;

const completed = tasks.filter(
    task => task.status === "completed"
).length;

document.getElementById("completedTasks").innerText = completed;

        localStorage.setItem("tasks", JSON.stringify(tasks));

        const keyword = searchTask.value.toLowerCase();

tasks
.filter(task =>
    task.title.toLowerCase().includes(keyword)
)
.forEach(task => {

            const card = document.createElement("div");

            card.className =
    task.status === "completed"
        ? "task-item completed-task"
        : "task-item pending-task";

            card.innerHTML = `
                <h3>${task.title}</h3>

                <p><strong>Description:</strong> ${task.description ?? ""}</p>

                <p><strong>Status:</strong> ${task.status}</p>

                <p><strong>Priority:</strong> ${task.priority}</p>

                <p><strong>Due Date:</strong> ${task.due_date ?? "-"}</p>

                <div class="task-buttons">

    <button
        class="edit-btn"
        onclick="showEditForm(${task.id})"
    >
        ✏️ Edit
    </button>

    <button
        class="delete-btn"
        onclick="deleteTask(${task.id})"
    >
        🗑 Delete
    </button>

    <button
        class="complete-btn"
        onclick="toggleStatus(${task.id}, '${task.status}')"
    >
        ${task.status === "pending"
            ? "✅ Complete"
            : "🔄 Pending"}
    </button>

</div>
            `;

            taskList.appendChild(card);

        });

    }

    catch (error) {

        console.log(error);

        const cached = localStorage.getItem("tasks");

        if (cached) {

            const tasks = JSON.parse(cached);

            tasks.forEach(task => {

                const card = document.createElement("div");

                card.className = "task-item";

                card.innerHTML = `
                    <h3>${task.title}</h3>

                    <p>${task.priority}</p>
                `;

                taskList.appendChild(card);

            });

        }

    }

}

// ===============================
// Add Task
// ===============================

taskForm.addEventListener("submit", async function (e) {

    e.preventDefault();

    titleError.innerText = "";

    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value;
    const priority = document.getElementById("priority").value;
    const due_date = document.getElementById("due_date").value;
    const project_id = Number(
        document.getElementById("project_id").value
    );

    if (title.length < 3) {

        titleError.innerText =
            "Title must be at least 3 characters";

        return;
    }

    const body = {
        title,
        description,
        status: "pending",
        priority,
        due_date,
        project_id
    };

    try {

    console.log("URL:", `${API_URL}/tasks/`);
    console.log("Body:", body);

    let response;

if (editingTaskId !== null) {

    response = await fetch(`${API_URL}/tasks/${editingTaskId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

} else {

    response = await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    });

}

    console.log("Status:", response.status);
    console.log("Response URL:", response.url);

    const data = await response.text();
    console.log("Response:", data);

    if (!response.ok) {
        alert("Task create failed");
        return;
    }

    showSuccessToast(
    editingTaskId !== null
        ? "🎉 Task Updated Successfully! ✨"
        : "🎉 Task Created Successfully! 🚀"
);

successToast.classList.add("show");

setTimeout(() => {
    successToast.classList.remove("show");
}, 3000);

    taskForm.reset();

editingTaskId = null;

taskForm.querySelector("button").innerText = "Add Task";

loadTasks();

} catch (error) {

    console.error(error);

    alert("❌ Server Connection Failed");

}

});

loadTasks();


// ===============================
// Edit Task
// ===============================
// ===============================
// Edit Task
// ===============================
async function showEditForm(id) {

    const response = await fetch(`${API_URL}/tasks/${id}`);
    const task = await response.json();

    document.getElementById("title").value = task.title;
    document.getElementById("description").value = task.description;
    document.getElementById("priority").value = task.priority;
    document.getElementById("due_date").value = task.due_date;
    document.getElementById("project_id").value = task.project_id;

    editingTaskId = id;

    taskForm.querySelector("button").innerText = "Update Task";
}

// ===============================
// Delete Task
// ===============================
function deleteTask(id) {
    deleteTaskId = id;
    deleteModal.classList.add("show");
}

cancelDelete.addEventListener("click", () => {
    deleteModal.classList.remove("show");
    deleteTaskId = null;
});

confirmDelete.addEventListener("click", async () => {

    const response = await fetch(`${API_URL}/tasks/${deleteTaskId}`, {
        method: "DELETE"
    });

    if (!response.ok) {
        alert("Delete failed");
        return;
    }

    deleteModal.classList.remove("show");
    deleteTaskId = null;

    showSuccessToast("🗑️ Task Deleted Successfully!");

    loadTasks();
});

// ===============================
// Toggle Task Status
// ===============================
async function toggleStatus(id, currentStatus) {

    const newStatus =
        currentStatus === "pending"
            ? "completed"
            : "pending";

    const response = await fetch(`${API_URL}/tasks/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            status: newStatus
        })
    });

    if (!response.ok) {
        alert("Status update failed");
        return;
    }

    showSuccessToast(
        newStatus === "completed"
            ? "🎉 Task Completed Successfully! ✅"
            : "📌 Task marked as Pending!"
    );

    loadTasks();
}


searchTask.addEventListener("input", loadTasks);

sortTasks.addEventListener("change", loadTasks);



// ===============================
// AI Quick Add
// ===============================

const quickAddBtn = document.getElementById("quickAddBtn");

quickAddBtn.addEventListener("click", async () => {

    const description = document
        .getElementById("quickDescription")
        .value
        .trim();

    const project_id = Number(
        document.getElementById("quickProjectId").value
    );

    if (description === "") {
        alert("Please enter task description.");
        return;
    }

    const response = await fetch(`${API_URL}/quick-add/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            description,
            project_id
        })
    });

    if (!response.ok) {
        alert("AI Quick Add Failed");
        return;
    }

    showSuccessToast("🤖 AI Task Created Successfully!");

    document.getElementById("quickDescription").value = "";
    document.getElementById("quickProjectId").value = "";

    loadTasks();
});



// ===============================
// Success Toast
// ===============================

// ===============================
// Success Toast
// ===============================
function showSuccessToast(message) {

    const toast = document.getElementById("successToast");

    toast.innerText = message;

    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}