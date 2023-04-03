
window.addEventListener("DOMContentLoaded", (event) => {
    getAccountDetails();
});


function getAccountDetails() {

    refreshAccessToken();

    // Get user details
    fetch(api_url + "/account/detail", {
        method: "GET",
        credentials: 'include'
    })

    .then(response => {
        if (response.status === 200) {
            return response.json();
        } 
        else {
            // TODO: redirect to an error occured page
            throw new Error("Could not get detail. An error occured.");
        }

    })

    .then((response) => {
        const account_details_div = document.getElementById("account-details-div");
        account_details_div.innerHTML += `
        <img alt='Avatar'
            src='${frontend_static_url}/wp-content/uploads/2023/03/user.png'
            srcset='${frontend_static_url}/wp-content/uploads/2023/03/user.png 2x'
            class='avatar avatar-48 photo rounded-circle' height='48' width='48'
            decoding='async' />
        <div class="pt-md-2 pt-lg-0 ps-3 ps-md-0 ps-lg-3">
            <h2 class="fs-lg mb-0 ">${response["first_name"]} ${response["last_name"]}</h2>
            <ul class="list-unstyled fs-sm mt-3 mb-0">
                <li>
                    <a class="nav-link fw-normal p-0" href="mailto:${response["email"]}">
                        <i class="fi-mail opacity-60 me-2"></i>
                        ${response["email"]}
                    </a>
                </li>
            </ul>
        </div>`;
    })

    .catch((error) => {
        console.log(error);
    });
    
    

}
