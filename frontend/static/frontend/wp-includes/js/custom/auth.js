var path_to_home = ".";

window.addEventListener("DOMContentLoaded", (event) => {
    getLoginState();
});


async function refreshAccessToken() {
    
    try {
        await new Promise((resolve, reject) => {    
            fetch(api_url + "/account/token/refresh", {
                method: "POST",
                credentials: "include"
            })
            .then(() => resolve())
            .catch(() => reject());
        });
    }
    catch (err) {
    }
}


function getLoginState() {

    // Try to refresh access token first
    refreshAccessToken();

    // Make a request to backend url and get login state
    fetch(api_url + "/account/login-state", {
        method: "GET",
        credentials: "include"
    })
    
    .then(response => {

        // If user is logged in (Account Icon)
        if (response.status === 200) {

            // Get user details
            fetch(api_url + "/account/detail", {
                method: "GET",
                credentials: 'include'
            })

            .then(response => response.json())

            .then((response) => {
                load_account_button(response);
            })

            .catch((error) => {
                console.log(error);
            });

        }

        // If user is not logged in (Sign In button)
        else {
            load_signin_button();
        }
    })
    
    .catch((error) => {
        load_signin_button();
    });
    
}


function load_signin_button() {

    const signin_btn = document.createElement("a");
    signin_btn.classList.add("btn", "btn-sm", "d-none", "d-lg-block", "order-lg-3", "text-primary");
    signin_btn.setAttribute("data-bs-toggle", "modal");
    signin_btn.href = "#user_login_modal";
    signin_btn.innerHTML = `<i class="fi-user me-2"></i>Sign in`;

    // Get the reference node
    const referenceNode = document.getElementById("navbar-toggler-btn");

    // Insert the new node before the reference node
    referenceNode.after(signin_btn);
}


function load_account_button(response) {

    let account_div = document.createElement("div");
    account_div.classList.add("dropdown", "d-none", "d-lg-block", "order-lg-3", "my-n2", "me-3");
    account_div.innerHTML = `
        <a class="d-block py-2 text-decoration-none account-toogle"
            href="${path_to_home}/account">
            <img alt="" src="${frontend_static_url}/wp-content/uploads/2023/03/user.png"
                srcset="${frontend_static_url}/wp-content/uploads/2023/03/user.png 2x"
                class="avatar avatar-40 photo rounded-circle" height="24" width="24" loading="lazy"> </a>
        <div class="dropdown-menu dropdown-menu-end">
            <div class="d-flex align-items-start border-bottom px-3 py-1 mb-2" style="width: 16rem;">
                <img alt="" src="${frontend_static_url}/wp-content/uploads/2023/03/user.png"
                    srcset="${frontend_static_url}/wp-content/uploads/2023/03/user.png 2x"
                    class="avatar avatar-48 photo rounded-circle" height="48" width="48" loading="lazy">
                <div class="ps-2">
                    <h6 class="fs-base mb-0">${response["first_name"]} ${response["last_name"]}</h6>
                    <div class="fs-xs py-2">${response["email"]}</div>
                </div>
            </div>
            <a class="dropdown-item" href="${path_to_home}/account/listings.html">
                <i class="fi-heart opacity-60 me-2"></i>
                Wishlist </a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="${path_to_home}/account">
                <i class="fi-settings opacity-60 me-2"></i>
                Account Settings </a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="javascript:logout();">
                <i class="fi-logout opacity-60 me-2"></i>
                Sign Out </a>
        </div>`;

    // Get the reference node
    let referenceNode = document.getElementById("navbar-toggler-btn");

    // Insert the new node before the reference node
    referenceNode.after(account_div);

}


function login(redirect) {

    let loginForm, loginData;

    if (redirect) {
        loginForm = document.forms.signupForm;
        loginData = new FormData(signupForm);
    }
    else {
        loginForm = document.forms.loginForm;
        loginData = new FormData(loginForm);
    }

    const error_messages_div = document.getElementById("signin-form-messages");
    error_messages_div.style.display = "none";
    error_messages_div.innerHTML = "";
    
    fetch(api_url + "/account/token", {
        method: 'POST',
        credentials: 'include',
        body: loginData
    })
    .then(response => {
        if (response.status === 401) {
            throw new Error("401");
        }
        else if (!response.ok) {
            throw new Error("An error has occured. Try again later.");
        }
        
        // Redirect to page on successful login
        window.location.href = ".";
    })
    .catch((error) => {
        error_message = (error.message === "401") ? "Email or password incorrect" : "An error has occurred. Please try again later"

        error_messages_div.style.display = "block";
        error_messages_div.innerHTML = `<div>${error_message}</div>`;

        const signin_submit_btn = document.getElementById("signin-submit-btn");
        signin_submit_btn.removeAttribute("disabled");
        signin_submit_btn.removeAttribute("data-state");
    });
    
    return false;

}


function logout() {

    fetch(api_url + "/account/logout", {
        method: 'POST',
        credentials: 'include',
    })
    
    .then(() => window.location.href = "/")
    
    .catch(() => console.log("An error has occurred. Try again later."));
    
}


function signup() {

    const signupForm = document.forms.signupForm;
    const signupData = new FormData(signupForm);

    const error_messages_div = document.getElementById("signup-form-messages");
    error_messages_div.style.display = "none";
    error_messages_div.innerHTML = "";
    
    fetch(api_url + "/account/register", {
        method: 'POST',
        credentials: 'include',
        body: signupData
    })
    .then(async (response) => {
        let response_json = await response.json();
        return {
            "raw": response,
            "json": response_json
        };
    })
    .then(response => {
        if (response.raw.status === 400) {
            console.log(response.json);
            let error_messages = "";
            for (let error_item in response.json) {
                error_messages += capitalize(error_item) + ": " + capitalize(response.json[error_item][0]) + "<br>";
            }
            throw new Error(error_messages);
        }
        else if (!response.raw.ok) {
            throw new Error("An error has occured. Try again later.");
        }
    
        // Login user immediately
        login(true);

    })
    .catch((error) => {
        error_messages_div.style.display = "block";
        error_messages_div.innerHTML = `<div>${error.message}</div>`;

        const signup_submit_btn = document.getElementById("signup-submit-btn");
        signup_submit_btn.removeAttribute("disabled");
        signup_submit_btn.removeAttribute("data-state");
    });

    return false;

}


function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}