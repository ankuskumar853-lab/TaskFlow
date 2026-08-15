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
        loginSuccess.classList.remove("show");


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

            loginSuccess.classList.add("show");


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


// ==========================================
// CONFIRM PASSWORD SHOW / HIDE
// ==========================================

const confirmPasswordField =
    document.getElementById("confirmPassword");

const confirmPasswordToggle =
    document.getElementById("confirmPasswordToggle");


if (
    confirmPasswordField &&
    confirmPasswordToggle
) {

    confirmPasswordToggle.addEventListener(
        "click",
        () => {

            if (
                confirmPasswordField.type === "password"
            ) {

                confirmPasswordField.type = "text";

                confirmPasswordToggle.innerText = "🙈";

            }

            else {

                confirmPasswordField.type = "password";

                confirmPasswordToggle.innerText = "👁";

            }

        }
    );

}


// ==========================================
// REGISTER
// ==========================================

const registerForm = document.getElementById("registerForm");
const registerName = document.getElementById("registerName");
const registerEmail = document.getElementById("registerEmail");
const confirmPassword = document.getElementById("confirmPassword");

const registerError = document.getElementById("registerError");
const registerSuccess = document.getElementById("registerSuccess");
const registerButton = document.getElementById("registerButton");


if (registerForm) {

    registerForm.addEventListener("submit", async (event) => {

        event.preventDefault();


        registerError.innerText = "";
        registerSuccess.innerText = "";
        registerSuccess.classList.remove("show");


        const name = registerName.value.trim();
        const email = registerEmail.value.trim();
        const password = registerPassword.value;
        const confirmPass = confirmPassword.value;


        // ======================================
        // VALIDATION
        // ======================================

        if (!name || !email || !password || !confirmPass) {

            registerError.innerText =
                "Please fill all fields.";

            return;
        }


        if (password !== confirmPass) {

            registerError.innerText =
                "Passwords do not match.";

            return;
        }


        // ======================================
        // DISABLE BUTTON
        // ======================================

        registerButton.disabled = true;
        registerButton.innerText = "Creating account...";


        try {

            const response = await fetch(
                `${API_URL}/users/`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: name,
                        email: email,
                        password: password
                    })
                }
            );


            const data = await response.json();


            console.log("Register response:", data);


            if (!response.ok) {

                registerError.innerText =
                    data.detail ||
                    "Registration failed.";

                return;
            }


            registerSuccess.innerText =
                "✅ Account created successfully! Redirecting to login...";

            registerSuccess.classList.add("show");


            setTimeout(() => {

                window.location.href = "login.html";

            }, 1000);

        }

        catch (error) {

            console.error("Register Error:", error);

            registerError.innerText =
                "❌ Could not connect to FastAPI. Make sure the backend is running.";

        }

        finally {

            registerButton.disabled = false;
            registerButton.innerText = "Create Account";

        }

    });

}