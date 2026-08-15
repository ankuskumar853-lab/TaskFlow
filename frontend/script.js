const API_URL = "http://127.0.0.1:8000";


// ======================================================
// AUTHENTICATION
// ======================================================

function getToken() {
    return localStorage.getItem("taskflow_token");
}


// Optional helper
function authHeaders(extraHeaders = {}) {

    const token = getToken();

    return {
        ...extraHeaders,
        Authorization: `Bearer ${token}`
    };
}


// ======================================================
// AUTH FETCH
// ======================================================

async function authFetch(url, options = {}) {

    const token = getToken();

    // No token
    if (!token) {

        alert("Please login first.");

        window.location.href = "login.html";

        return null;
    }


    // Copy options so original object is not modified
    const fetchOptions = {
        ...options
    };


    // Existing headers
    fetchOptions.headers = {
        ...(options.headers || {}),
        Authorization: `Bearer ${token}`
    };


    try {

        const response = await fetch(
            url,
            fetchOptions
        );


        // Unauthorized
        if (response.status === 401) {

            localStorage.removeItem("taskflow_token");
            localStorage.removeItem("access_token");

            alert(
                "Session expired. Please login again."
            );

            window.location.href = "login.html";

            return null;
        }


        return response;

    }

    catch (error) {

        console.error(
            "Fetch Error:",
            error
        );

        throw error;
    }
}


// ======================================================
// DOM ELEMENTS
// ======================================================

const taskForm =
    document.getElementById("taskForm");

const taskList =
    document.getElementById("taskList");

const titleError =
    document.getElementById("titleError");

const deleteModal =
    document.getElementById("deleteModal");

const confirmDelete =
    document.getElementById("confirmDelete");

const cancelDelete =
    document.getElementById("cancelDelete");

const searchTask =
    document.getElementById("searchTask");

const sortTasks =
    document.getElementById("sortTasks");

const successToast =
    document.getElementById("successToast");


// ======================================================
// AI QUICK ADD ELEMENTS
// ======================================================

const quickAddBtn =
    document.getElementById("quickAddBtn");

const quickDescription =
    document.getElementById("quickDescription");

const quickProjectId =
    document.getElementById("quickProjectId");

const quickTaskPreview =
    document.getElementById("quickTaskPreview");

const quickPreviewDescription =
    document.getElementById(
        "quickPreviewDescription"
    );

const quickTaskDueDate =
    document.getElementById(
        "quickTaskDueDate"
    );

const confirmQuickTaskBtn =
    document.getElementById(
        "confirmQuickTaskBtn"
    );

const cancelQuickTaskBtn =
    document.getElementById(
        "cancelQuickTaskBtn"
    );

const priorityOptions =
    document.querySelectorAll(
        ".priority-option"
    );


// ======================================================
// ALGORITHM SEARCH ELEMENTS
// ======================================================

const algorithmSearch =
    document.getElementById(
        "algorithmSearch"
    );

const searchAlgorithm =
    document.getElementById(
        "searchAlgorithm"
    );

const algorithmSearchBtn =
    document.getElementById(
        "algorithmSearchBtn"
    );

const clearSearchBtn =
    document.getElementById(
        "clearSearchBtn"
    );


// ======================================================
// VARIABLES
// ======================================================

let editingTaskId = null;

let deleteTaskId = null;

let quickTaskData = null;

let selectedQuickPriority = "medium";


// ======================================================
// PAGINATION VARIABLES
// ======================================================

let currentPage = 1;

const tasksPerPage = 5;


// ======================================================
// SUCCESS TOAST
// ======================================================

function showSuccessToast(message) {

    if (!successToast) {
        return;
    }


    successToast.innerText = message;

    successToast.classList.add("show");


    setTimeout(() => {

        successToast.classList.remove("show");

    }, 3000);
}


// ======================================================
// LOAD TASKS
// ======================================================

async function loadTasks() {

    console.log("Loading tasks...");


    try {

        const response =
            await authFetch(
                `${API_URL}/tasks/`
            );


        if (!response) {
            return;
        }


        if (!response.ok) {

            const errorText =
                await response.text();

            throw new Error(
                `GET /tasks/ failed: ${response.status} ${errorText}`
            );
        }


        const tasks =
            await response.json();


        console.log(
            "Tasks received:",
            tasks
        );


        renderTasks(tasks);

    }

    catch (error) {

        console.error(
            "Load Tasks Error:",
            error
        );


        if (taskList) {

            taskList.innerHTML = `
                <p style="color:red;">
                    ❌ Could not load tasks.
                    <br><br>
                    Check whether FastAPI is running.
                    <br><br>
                    ${error.message}
                </p>
            `;
        }
    }
}


// ======================================================
// RENDER TASKS
// ======================================================

function renderTasks(tasks) {

    if (!Array.isArray(tasks)) {

        console.error(
            "Tasks is not an array:",
            tasks
        );

        return;
    }


    // ==================================================
    // SORT TASKS
    // ==================================================

    const sortValue =
        sortTasks
            ? sortTasks.value
            : "newest";


    if (sortValue === "oldest") {

        tasks.sort(
            (a, b) => a.id - b.id
        );
    }


    else if (sortValue === "newest") {

        tasks.sort(
            (a, b) => b.id - a.id
        );
    }


    else if (sortValue === "priority") {

        const rank = {
            high: 3,
            medium: 2,
            low: 1
        };


        tasks.sort(
            (a, b) =>
                (rank[b.priority] || 0) -
                (rank[a.priority] || 0)
        );
    }


    else if (sortValue === "status") {

        tasks.sort((a, b) => {

            if (
                a.status === "pending" &&
                b.status !== "pending"
            ) {

                return -1;
            }


            if (
                a.status !== "pending" &&
                b.status === "pending"
            ) {

                return 1;
            }


            return 0;
        });
    }


    // ==================================================
    // STATISTICS
    // ==================================================

    const total =
        tasks.length;


    const pending =
        tasks.filter(
            task =>
                task.status === "pending"
        ).length;


    const completed =
        tasks.filter(
            task =>
                task.status === "completed"
        ).length;


    const totalElement =
        document.getElementById(
            "totalTasks"
        );


    const pendingElement =
        document.getElementById(
            "pendingTasks"
        );


    const completedElement =
        document.getElementById(
            "completedTasks"
        );


    if (totalElement) {

        totalElement.innerText =
            total;
    }


    if (pendingElement) {

        pendingElement.innerText =
            pending;
    }


    if (completedElement) {

        completedElement.innerText =
            completed;
    }


    // ==================================================
    // NORMAL SEARCH
    // ==================================================

    const keyword =
        searchTask
            ? searchTask.value
                .toLowerCase()
                .trim()
            : "";


    const filteredTasks =
        tasks.filter(task => {

            const title =
                String(
                    task.title || ""
                ).toLowerCase();


            const description =
                String(
                    task.description || ""
                ).toLowerCase();


            return (
                title.includes(keyword) ||
                description.includes(keyword)
            );
        });


    // ==================================================
    // TASK LIST
    // ==================================================

    if (!taskList) {
        return;
    }


    taskList.innerHTML = "";


    // ==================================================
    // NO TASK
    // ==================================================

    if (filteredTasks.length === 0) {

        taskList.innerHTML = `
            <p>
                📭 No tasks found.
            </p>
        `;

        removePaginationControls();

        return;
    }


    // ==================================================
    // PAGINATION - SLICE TASKS
    // ==================================================

    const totalPages =
        Math.ceil(filteredTasks.length / tasksPerPage) || 1;


    if (currentPage > totalPages) {

        currentPage = totalPages;
    }


    if (currentPage < 1) {

        currentPage = 1;
    }


    const startIndex =
        (currentPage - 1) * tasksPerPage;


    const endIndex =
        startIndex + tasksPerPage;


    const paginatedTasks =
        filteredTasks.slice(startIndex, endIndex);


    // ==================================================
    // CREATE TASK CARDS
    // ==================================================

    paginatedTasks.forEach(task => {

        const card =
            document.createElement("div");


        card.className =
            task.status === "completed"
                ? "task-item completed-task"
                : "task-item pending-task";


        // ==================================================
        // TITLE
        // ==================================================

        const title =
            document.createElement("h3");


        title.textContent =
            task.title ||
            "Untitled Task";


        // ==================================================
        // DESCRIPTION
        // ==================================================

        const description =
            document.createElement("p");


        description.textContent =
            `Description: ${
                task.description || ""
            }`;


        // ==================================================
        // STATUS
        // ==================================================

        const status =
            document.createElement("p");


        status.textContent =
            `Status: ${
                task.status || "pending"
            }`;


        // ==================================================
        // PRIORITY
        // ==================================================

        const priority =
            document.createElement("p");


        priority.textContent =
            `Priority: ${
                task.priority || "medium"
            }`;


        // ==================================================
        // DUE DATE
        // ==================================================

        const dueDate =
            document.createElement("p");


        dueDate.textContent =
            `Due Date: ${
                task.due_date || "-"
            }`;


        // ==================================================
        // BUTTON CONTAINER
        // ==================================================

        const buttons =
            document.createElement("div");


        buttons.className =
            "task-buttons";


        // ==================================================
        // EDIT BUTTON
        // ==================================================

        const editButton =
            document.createElement("button");


        editButton.type =
            "button";


        editButton.className =
            "edit-btn";


        editButton.textContent =
            "✏️ Edit";


        editButton.addEventListener(
            "click",
            () => {

                showEditForm(task.id);

            }
        );


        // ==================================================
        // DELETE BUTTON
        // ==================================================

        const deleteButton =
            document.createElement("button");


        deleteButton.type =
            "button";


        deleteButton.className =
            "delete-btn";


        deleteButton.textContent =
            "🗑 Delete";


        deleteButton.addEventListener(
            "click",
            () => {

                openDeleteModal(task.id);

            }
        );


        // ==================================================
        // COMPLETE BUTTON
        // ==================================================

        const completeButton =
            document.createElement("button");


        completeButton.type =
            "button";


        completeButton.className =
            "complete-btn";


        completeButton.textContent =
            task.status === "pending"
                ? "✅ Complete"
                : "🔄 Pending";


        completeButton.addEventListener(
            "click",
            () => {

                toggleStatus(
                    task.id,
                    task.status
                );

            }
        );


        // ==================================================
        // APPEND BUTTONS
        // ==================================================

        buttons.appendChild(
            editButton
        );


        buttons.appendChild(
            deleteButton
        );


        buttons.appendChild(
            completeButton
        );


        // ==================================================
        // APPEND TASK DATA
        // ==================================================

        card.appendChild(title);

        card.appendChild(description);

        card.appendChild(status);

        card.appendChild(priority);

        card.appendChild(dueDate);

        card.appendChild(buttons);


        taskList.appendChild(card);

    });


    // ==================================================
    // PAGINATION CONTROLS
    // ==================================================

    renderPaginationControls(totalPages);

}


// ======================================================
// PAGINATION CONTROLS
// ======================================================

function removePaginationControls() {

    const oldPagination =
        document.getElementById("paginationControls");


    if (oldPagination) {

        oldPagination.remove();
    }
}


function renderPaginationControls(totalPages) {

    removePaginationControls();


    const paginationDiv =
        document.createElement("div");


    paginationDiv.id =
        "paginationControls";


    paginationDiv.className =
        "pagination-controls";


    // ==================================================
    // PREVIOUS BUTTON
    // ==================================================

    const prevBtn =
        document.createElement("button");


    prevBtn.type =
        "button";


    prevBtn.textContent =
        "⬅ Previous";


    prevBtn.disabled =
        currentPage === 1;


    prevBtn.addEventListener(
        "click",
        () => {

            currentPage--;

            loadTasks();
        }
    );


    // ==================================================
    // PAGE INFO
    // ==================================================

    const pageInfo =
        document.createElement("span");


    pageInfo.textContent =
        `Page ${currentPage} of ${totalPages}`;


    // ==================================================
    // NEXT BUTTON
    // ==================================================

    const nextBtn =
        document.createElement("button");


    nextBtn.type =
        "button";


    nextBtn.textContent =
        "Next ➡";


    nextBtn.disabled =
        currentPage === totalPages;


    nextBtn.addEventListener(
        "click",
        () => {

            currentPage++;

            loadTasks();
        }
    );


    // ==================================================
    // APPEND CONTROLS
    // ==================================================

    paginationDiv.appendChild(prevBtn);

    paginationDiv.appendChild(pageInfo);

    paginationDiv.appendChild(nextBtn);


    taskList.insertAdjacentElement(
        "afterend",
        paginationDiv
    );
}


// ======================================================
// ADD / UPDATE TASK
// ======================================================

if (taskForm) {

    taskForm.addEventListener(
        "submit",
        async function (e) {

            e.preventDefault();


            if (titleError) {

                titleError.innerText = "";

            }


            const titleElement =
                document.getElementById("title");


            const descriptionElement =
                document.getElementById("description");


            const priorityElement =
                document.getElementById("priority");


            const dueDateElement =
                document.getElementById("due_date");


            const projectIdElement =
                document.getElementById("project_id");


            if (
                !titleElement ||
                !descriptionElement ||
                !priorityElement ||
                !dueDateElement ||
                !projectIdElement
            ) {

                alert(
                    "❌ Some task form fields are missing."
                );

                return;
            }


            const title =
                titleElement.value.trim();


            const description =
                descriptionElement.value.trim();


            const priority =
                priorityElement.value;


            const due_date =
                dueDateElement.value.trim();


            const project_id =
                Number(
                    projectIdElement.value
                );


            // ==================================================
            // VALIDATION
            // ==================================================

            if (title.length < 3) {

                if (titleError) {

                    titleError.innerText =
                        "Title must be at least 3 characters";

                }

                return;
            }


            if (!project_id) {

                alert(
                    "Please enter Project ID."
                );

                return;
            }


            // ==================================================
            // REQUEST BODY
            // ==================================================

            const body = {

                title: title,

                description: description,

                status: "pending",

                priority: priority,

                due_date: due_date || null,

                project_id: project_id

            };


            console.log(
                "Task Body:",
                body
            );


            try {

                let response;


                // ==================================================
                // UPDATE
                // ==================================================

                if (
                    editingTaskId !== null
                ) {

                    response =
                        await authFetch(
                            `${API_URL}/tasks/${editingTaskId}`,
                            {

                                method: "PUT",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(body)

                            }
                        );
                }


                // ==================================================
                // CREATE
                // ==================================================

                else {

                    response =
                        await authFetch(
                            `${API_URL}/tasks/`,
                            {

                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(body)

                            }
                        );
                }


                if (!response) {
                    return;
                }


                // ==================================================
                // ERROR
                // ==================================================

                if (!response.ok) {

                    const error =
                        await response.text();


                    console.error(
                        "Task Backend Error:",
                        error
                    );


                    alert(
                        "❌ Task operation failed\n\n" +
                        error
                    );

                    return;
                }


                // ==================================================
                // SUCCESS
                // ==================================================

                if (
                    editingTaskId !== null
                ) {

                    showSuccessToast(
                        "🎉 Task Updated Successfully!"
                    );

                }

                else {

                    showSuccessToast(
                        "🎉 Task Created Successfully!"
                    );
                }


                // ==================================================
                // RESET
                // ==================================================

                taskForm.reset();


                editingTaskId = null;


                const submitButton =
                    taskForm.querySelector(
                        "button[type='submit']"
                    );


                if (submitButton) {

                    submitButton.innerText =
                        "Add Task";
                }


                await loadTasks();

            }

            catch (error) {

                console.error(
                    "Task Error:",
                    error
                );


                alert(
                    "❌ Server Connection Failed\n\n" +
                    error.message
                );
            }
        }
    );
}


// ======================================================
// EDIT TASK
// ======================================================

async function showEditForm(id) {

    console.log(
        "Editing task:",
        id
    );


    try {

        const response =
            await authFetch(
                `${API_URL}/tasks/${id}`
            );


        if (!response) {
            return;
        }


        if (!response.ok) {

            const error =
                await response.text();


            console.error(
                "Edit Error:",
                error
            );


            alert(
                "❌ Could not find task."
            );

            return;
        }


        const task =
            await response.json();


        // ==================================================
        // FILL FORM
        // ==================================================

        const titleElement =
            document.getElementById("title");


        const descriptionElement =
            document.getElementById("description");


        const priorityElement =
            document.getElementById("priority");


        const dueDateElement =
            document.getElementById("due_date");


        const projectIdElement =
            document.getElementById("project_id");


        if (titleElement) {

            titleElement.value =
                task.title || "";
        }


        if (descriptionElement) {

            descriptionElement.value =
                task.description || "";
        }


        if (priorityElement) {

            priorityElement.value =
                task.priority || "medium";
        }


        if (dueDateElement) {

            dueDateElement.value =
                task.due_date || "";
        }


        if (projectIdElement) {

            projectIdElement.value =
                task.project_id || "";
        }


        // ==================================================
        // SAVE EDIT ID
        // ==================================================

        editingTaskId = id;


        // ==================================================
        // CHANGE BUTTON
        // ==================================================

        const submitButton =
            taskForm
                ? taskForm.querySelector(
                    "button[type='submit']"
                )
                : null;


        if (submitButton) {

            submitButton.innerText =
                "Update Task";
        }


        // ==================================================
        // SCROLL TO FORM
        // ==================================================

        const formSection =
            document.querySelector(
                ".form-section"
            );


        if (formSection) {

            formSection.scrollIntoView({

                behavior: "smooth",

                block: "start"

            });
        }

    }

    catch (error) {

        console.error(
            "Edit Error:",
            error
        );


        alert(
            "❌ Could not load task.\n\n" +
            error.message
        );
    }
}


// ======================================================
// DELETE MODAL
// ======================================================

function openDeleteModal(id) {

    deleteTaskId = id;


    console.log(
        "Delete task:",
        id
    );


    if (deleteModal) {

        deleteModal.classList.add(
            "show"
        );
    }
}


// ======================================================
// CANCEL DELETE
// ======================================================

if (cancelDelete) {

    cancelDelete.addEventListener(
        "click",
        () => {

            if (deleteModal) {

                deleteModal.classList.remove(
                    "show"
                );
            }


            deleteTaskId = null;

        }
    );
}


// ======================================================
// CONFIRM DELETE
// ======================================================

if (confirmDelete) {

    confirmDelete.addEventListener(
        "click",
        async () => {

            if (
                deleteTaskId === null
            ) {

                alert(
                    "No task selected."
                );

                return;
            }


            try {

                console.log(
                    "Deleting:",
                    deleteTaskId
                );


                const response =
                    await authFetch(
                        `${API_URL}/tasks/${deleteTaskId}`,
                        {
                            method: "DELETE"
                        }
                    );


                if (!response) {
                    return;
                }


                const result =
                    await response.text();


                console.log(
                    "Delete response:",
                    response.status,
                    result
                );


                if (!response.ok) {

                    alert(
                        "❌ Delete failed\n\n" +
                        result
                    );

                    return;
                }


                if (deleteModal) {

                    deleteModal.classList.remove(
                        "show"
                    );
                }


                deleteTaskId = null;


                showSuccessToast(
                    "🗑️ Task Deleted Successfully!"
                );


                await loadTasks();

            }

            catch (error) {

                console.error(
                    "Delete Error:",
                    error
                );


                alert(
                    "❌ Server Connection Failed\n\n" +
                    error.message
                );
            }
        }
    );
}


// ======================================================
// TOGGLE TASK STATUS
// ======================================================

async function toggleStatus(
    id,
    currentStatus
) {

    const newStatus =
        currentStatus === "pending"
            ? "completed"
            : "pending";


    try {

        const response =
            await authFetch(
                `${API_URL}/tasks/${id}`,
                {

                    method: "PUT",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            status: newStatus
                        })
                }
            );


        if (!response) {
            return;
        }


        if (!response.ok) {

            const error =
                await response.text();


            console.error(
                "Status Error:",
                error
            );


            alert(
                "❌ Status update failed\n\n" +
                error
            );

            return;
        }


        showSuccessToast(

            newStatus === "completed"
                ? "🎉 Task Completed!"
                : "📌 Task marked Pending!"

        );


        await loadTasks();

    }

    catch (error) {

        console.error(
            "Status Error:",
            error
        );


        alert(
            "❌ Server Connection Failed\n\n" +
            error.message
        );
    }
}


// ======================================================
// NORMAL SEARCH
// ======================================================

if (searchTask) {

    searchTask.addEventListener(
        "input",
        () => {

            currentPage = 1;

            loadTasks();
        }
    );
}


// ======================================================
// SORT
// ======================================================

if (sortTasks) {

    sortTasks.addEventListener(
        "change",
        () => {

            currentPage = 1;

            loadTasks();
        }
    );
}


// ======================================================
// AI QUICK ADD
// ======================================================

if (quickAddBtn) {

    quickAddBtn.addEventListener(
        "click",
        async () => {

            console.log(
                "🤖 QUICK ADD BUTTON CLICKED"
            );


            const description =
                quickDescription
                    ? quickDescription.value.trim()
                    : "";


            const project_id =
                quickProjectId
                    ? Number(
                        quickProjectId.value
                    )
                    : 0;


            if (!description) {

                alert(
                    "Please enter task description."
                );

                return;
            }


            if (!project_id) {

                alert(
                    "Please enter Project ID."
                );

                return;
            }


            try {

                const response =
                    await authFetch(
                        `${API_URL}/tasks/quick-add`,
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify({

                                    description:
                                        description,

                                    project_id:
                                        project_id

                                })
                        }
                    );


                if (!response) {
                    return;
                }


                const responseText =
                    await response.text();


                console.log(
                    "Quick Add Status:",
                    response.status
                );


                console.log(
                    "Quick Add Response:",
                    responseText
                );


                if (!response.ok) {

                    alert(
                        "❌ AI Quick Add Failed\n\n" +
                        responseText
                    );

                    return;
                }


                try {

                    quickTaskData =
                        JSON.parse(
                            responseText
                        );

                }

                catch (parseError) {

                    console.error(
                        "JSON Parse Error:",
                        parseError
                    );


                    alert(
                        "❌ Invalid response from server."
                    );

                    return;
                }


                console.log(
                    "🤖 AI Task Data:",
                    quickTaskData
                );


                // ==================================================
                // DESCRIPTION PREVIEW
                // ==================================================

                if (quickPreviewDescription) {

                    quickPreviewDescription.innerText =
                        quickTaskData.description ||
                        description;
                }


                // ==================================================
                // PRIORITY
                // ==================================================

                const detectedPriority =
                    quickTaskData.priority ||
                    "medium";


                selectedQuickPriority =
                    detectedPriority;


                priorityOptions.forEach(
                    button => {

                        button.classList.remove(
                            "active"
                        );


                        if (
                            button.dataset.priority ===
                            detectedPriority
                        ) {

                            button.classList.add(
                                "active"
                            );
                        }
                    }
                );


                // ==================================================
                // DUE DATE
                // ==================================================

                if (quickTaskDueDate) {

                    quickTaskDueDate.value =
                        quickTaskData.due_date ||
                        "";
                }


                // ==================================================
                // SHOW PREVIEW
                // ==================================================

                if (quickTaskPreview) {

                    quickTaskPreview.classList.add(
                        "show"
                    );
                }


                console.log(
                    "🤖 AI Preview Opened"
                );

            }

            catch (error) {

                console.error(
                    "Quick Add Error:",
                    error
                );


                alert(
                    "❌ Server Connection Failed\n\n" +
                    error.message
                );
            }
        }
    );
}


// ======================================================
// AI PRIORITY BUTTONS
// ======================================================

priorityOptions.forEach(
    button => {

        button.addEventListener(
            "click",
            () => {

                priorityOptions.forEach(
                    btn => {

                        btn.classList.remove(
                            "active"
                        );
                    }
                );


                button.classList.add(
                    "active"
                );


                selectedQuickPriority =
                    button.dataset.priority;


                console.log(
                    "Selected AI Priority:",
                    selectedQuickPriority
                );
            }
        );
    }
);


// ======================================================
// CONFIRM AI TASK
// ======================================================

if (confirmQuickTaskBtn) {

    confirmQuickTaskBtn.addEventListener(
        "click",
        async () => {

            console.log(
                "🤖 ADD AI TASK CLICKED"
            );


            if (!quickTaskData) {

                alert(
                    "❌ No AI task data available."
                );

                return;
            }


            const activePriority =
                document.querySelector(
                    ".priority-option.active"
                );


            const finalPriority =
                activePriority
                    ? activePriority.dataset.priority
                    : (
                        quickTaskData.priority ||
                        "medium"
                    );


            const finalDueDate =
                quickTaskDueDate
                    ? quickTaskDueDate.value.trim()
                    : (
                        quickTaskData.due_date ||
                        ""
                    );


            let finalProjectId = 0;


            if (quickTaskData.project_id) {

                finalProjectId =
                    Number(
                        quickTaskData.project_id
                    );
            }

            else if (quickProjectId) {

                finalProjectId =
                    Number(
                        quickProjectId.value
                    );
            }


            if (!finalProjectId) {

                alert(
                    "❌ Project ID is required."
                );

                return;
            }


            const taskBody = {

                title:
                    quickTaskData.title ||
                    quickTaskData.description ||
                    "New Task",

                description:
                    quickTaskData.description ||
                    "",

                status:
                    "pending",

                priority:
                    finalPriority,

                due_date:
                    finalDueDate ||
                    null,

                project_id:
                    finalProjectId
            };


            console.log(
                "Saving AI Task:",
                taskBody
            );


            try {

                const saveResponse =
                    await authFetch(
                        `${API_URL}/tasks/`,
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body:
                                JSON.stringify(
                                    taskBody
                                )
                        }
                    );


                if (!saveResponse) {
                    return;
                }


                const saveText =
                    await saveResponse.text();


                console.log(
                    "AI Save Status:",
                    saveResponse.status
                );


                console.log(
                    "AI Save Response:",
                    saveText
                );


                if (!saveResponse.ok) {

                    alert(
                        "❌ Could not save AI task\n\n" +
                        saveText
                    );

                    return;
                }


                // ==================================================
                // RESET PREVIEW
                // ==================================================

                if (quickTaskPreview) {

                    quickTaskPreview.classList.remove(
                        "show"
                    );
                }


                if (quickDescription) {

                    quickDescription.value =
                        "";
                }


                if (quickProjectId) {

                    quickProjectId.value =
                        "";
                }


                if (quickTaskDueDate) {

                    quickTaskDueDate.value =
                        "";
                }


                priorityOptions.forEach(
                    button => {

                        button.classList.remove(
                            "active"
                        );
                    }
                );


                const mediumButton =
                    document.querySelector(
                        '.priority-option[data-priority="medium"]'
                    );


                if (mediumButton) {

                    mediumButton.classList.add(
                        "active"
                    );
                }


                selectedQuickPriority =
                    "medium";


                quickTaskData =
                    null;


                await loadTasks();


                showSuccessToast(
                    "🤖 AI Task Added Successfully!"
                );


                console.log(
                    "✅ AI Task Added Successfully"
                );

            }

            catch (error) {

                console.error(
                    "AI Save Error:",
                    error
                );


                alert(
                    "❌ Server Connection Failed\n\n" +
                    error.message
                );
            }
        }
    );
}


// ======================================================
// CANCEL AI TASK
// ======================================================

if (cancelQuickTaskBtn) {

    cancelQuickTaskBtn.addEventListener(
        "click",
        () => {

            console.log(
                "❌ AI Task Cancelled"
            );


            if (quickTaskPreview) {

                quickTaskPreview.classList.remove(
                    "show"
                );
            }


            quickTaskData = null;


            if (quickTaskDueDate) {

                quickTaskDueDate.value =
                    "";
            }


            priorityOptions.forEach(
                button => {

                    button.classList.remove(
                        "active"
                    );
                }
            );


            const mediumButton =
                document.querySelector(
                    '.priority-option[data-priority="medium"]'
                );


            if (mediumButton) {

                mediumButton.classList.add(
                    "active"
                );
            }


            selectedQuickPriority =
                "medium";
        }
    );
}


// ======================================================
// ALGORITHM SEARCH
// ======================================================

if (algorithmSearchBtn) {

    algorithmSearchBtn.addEventListener(
        "click",
        async () => {

            // ------------------------------------------
            // GET TITLE
            // ------------------------------------------

            const title =
                algorithmSearch
                    ? algorithmSearch.value.trim()
                    : "";


            // ------------------------------------------
            // GET ALGORITHM
            // ------------------------------------------

            const algorithm =
                searchAlgorithm
                    ? searchAlgorithm.value
                    : "linear";


            // ------------------------------------------
            // VALIDATION
            // ------------------------------------------

            if (!title) {

                alert(
                    "Please enter task title."
                );

                return;
            }


            console.log(
                "Algorithm Search:",
                {
                    title: title,
                    algorithm: algorithm
                }
            );


            try {

                // --------------------------------------
                // API REQUEST
                // --------------------------------------

                const response =
                    await authFetch(
                        `${API_URL}/tasks/search?title=${encodeURIComponent(title)}&algo=${encodeURIComponent(algorithm)}`
                    );


                if (!response) {
                    return;
                }


                // --------------------------------------
                // RESPONSE
                // --------------------------------------

                const text =
                    await response.text();


                console.log(
                    "Algorithm Search Status:",
                    response.status
                );


                console.log(
                    "Algorithm Search Response:",
                    text
                );


                // --------------------------------------
                // ERROR
                // --------------------------------------

                if (!response.ok) {

                    alert(
                        "❌ Search failed\n\n" +
                        text
                    );

                    return;
                }


                // --------------------------------------
                // PARSE JSON
                // --------------------------------------

                let result;


                try {

                    result =
                        JSON.parse(text);

                }

                catch (parseError) {

                    console.error(
                        "Search JSON Error:",
                        parseError
                    );


                    alert(
                        "❌ Server returned invalid JSON."
                    );

                    return;
                }


                console.log(
                    "Search Result:",
                    result
                );


                // --------------------------------------
                // HANDLE RESULT
                // --------------------------------------

                currentPage = 1;


                if (Array.isArray(result)) {

                    renderTasks(result);

                }

                else {

                    renderTasks([result]);

                }

            }

            catch (error) {

                console.error(
                    "Algorithm Search Error:",
                    error
                );


                alert(
                    "❌ Server Connection Failed\n\n" +
                    error.message
                );
            }
        }
    );
}


// ======================================================
// CLEAR ALGORITHM SEARCH
// ======================================================

if (clearSearchBtn) {

    clearSearchBtn.addEventListener(
        "click",
        () => {

            if (algorithmSearch) {

                algorithmSearch.value =
                    "";
            }


            currentPage = 1;


            loadTasks();
        }
    );
}





// ======================================================
// PAGE LOAD
// ======================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "🚀 TaskFlow JavaScript loaded."
        );


        // Check token
        const token =
            getToken();


        if (!token) {

            console.warn(
                "⚠️ No TaskFlow token found."
            );

            return;
        }


        // Load tasks
        loadTasks();

    }
);