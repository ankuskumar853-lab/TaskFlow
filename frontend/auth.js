const API_URL = "https://taskflow-1-is4v.onrender.com";

const loginForm = document.getElementById("loginForm");
const loginEmail = document.getElementById("loginEmail");
const loginPassword = document.getElementById("loginPassword");

const loginError = document.getElementById("loginError");
const loginSuccess = document.getElementById("loginSuccess");

const loginButton = document.getElementById("loginButton");

const loginPasswordToggle =
    document.getElementById("loginPasswordToggle");


// ==========================================
// PASSWORD SHOW / HIDE
// ==========================================

if (loginPasswordToggle) {

    loginPasswordToggle.addEventListener("click", () => {

        if (loginPassword.type === "password") {

            loginPassword.type = "text";
            loginPasswordToggle.innerText = "🙈";

        } else {

            loginPassword.type = "password";
            loginPasswordToggle.innerText = "👁";

        }

    });

}


// ==========================================
// LOGIN
// ==========================================

if (loginForm) {

    loginForm.addEventListener("submit", async (event) => {

        event.preventDefault();


        // Clear old messages

        loginError.innerText = "";
        loginSuccess.innerText = "";


        const email = loginEmail.value.trim();
        const password = loginPassword.value;


        // ======================================
        // VALIDATION
        // ======================================

        if (!email || !password) {

            loginError.innerText =
                "Please enter email and password.";

            return;
        }


        // ======================================
        // DISABLE BUTTON
        // ======================================

        loginButton.disabled = true;
        loginButton.innerText = "Logging in...";


        try {

            // ==================================
            // LOGIN API
            // ==================================

            const response = await fetch(
                `${API_URL}/users/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                }
            );


            const data = await response.json();


            console.log("Login response:", data);


            // ==================================
            // BACKEND ERROR
            // ==================================

            if (!response.ok) {

                loginError.innerText =
                    data.detail ||
                    "Invalid email or password.";

                return;
            }


            // ==================================
            // CHECK TOKEN
            // ==================================

            if (!data.access_token) {

                loginError.innerText =
                    "Login successful, but token was not received.";

                return;
            }


            // ==================================
            // SAVE TOKEN
            // IMPORTANT:
            // index.html uses taskflow_token
            // ==================================

            localStorage.setItem(
                "taskflow_token",
                data.access_token
            );


            // ==================================
            // SUCCESS
            // ==================================

            loginSuccess.innerText =
                "✅ Login successful! Opening dashboard...";


            // ==================================
            // GO TO DASHBOARD
            // ==================================

            setTimeout(() => {

                window.location.href = "index.html";

            }, 500);

        }


        catch (error) {

            console.error("Login Error:", error);

            loginError.innerText =
                "❌ Could not connect to FastAPI. Make sure the backend is running.";

        }


        finally {

            loginButton.disabled = false;
            loginButton.innerText = "Login";

        }

    });

}

// ==========================================
// REGISTER PASSWORD SHOW / HIDE
// ==========================================

const registerPassword =
    document.getElementById("registerPassword");

const registerPasswordToggle =
    document.getElementById("registerPasswordToggle");


if (
    registerPassword &&
    registerPasswordToggle
) {

    registerPasswordToggle.addEventListener(
        "click",
        () => {

            if (
                registerPassword.type === "password"
            ) {

                registerPassword.type = "text";

                registerPasswordToggle.innerText = "🙈";

            }

            else {

                registerPassword.type = "password";

                registerPasswordToggle.innerText = "👁";

            }

        }
    );

}