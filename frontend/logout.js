// ==========================================
// TASKFLOW LOGOUT
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    const logoutBtn = document.getElementById("logoutBtn");

    if (!logoutBtn) {
        console.error("Logout button not found");
        return;
    }

    console.log("Logout button found");

    logoutBtn.addEventListener("click", function (event) {

        event.preventDefault();

        console.log("Logout button clicked");

        // Remove login token
        localStorage.removeItem("taskflow_token");
        localStorage.removeItem("access_token");
        localStorage.removeItem("token");

        // Clear session
        sessionStorage.clear();

        console.log("Token removed");

        // Redirect to login page
        window.location.href = "login.html";

    });

});