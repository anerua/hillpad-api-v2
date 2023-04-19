window.addEventListener("DOMContentLoaded", () => {
    loadCourses();
});


function getFilterURL() {
    let urlString = window.location.href;
    let paramString = urlString.split('?')[1];
    let queryString = new URLSearchParams(paramString);

    let newQueryString = "?";

    for (let pair of queryString.entries()) {
        if (!pair[1]) {
            continue;
        } else if (pair[0] === "location") {
            if (pair[1][0] === "_") {
                newQueryString += `continent=${pair[1].substring(1)}&`;
            } else {
                newQueryString += `country=${pair[1]}&`;
            }
        } else {
            newQueryString += `${pair[0]}=${pair[1]}&`;
        }
    }

    // Get courses with new query string
    console.log(newQueryString);
    return newQueryString;
}

function loadCourses() {
    const courses_list_div = document.getElementById("courses-list-div");
    
    fetch(api_url + "/academics/course/list" + getFilterURL(), {
        method: "GET",
    })
    .then((response) => response.json())
    .then((response) => {
        if (response["count"] == 0) {
            console.log("No result");
            courses_list_div.innerHTML = `
                <p>No results</p>
            `;
        }
        console.log(response["results"]);

        courses = response["results"];

        courses.forEach((course) => {
            courses_list_div.innerHTML += `
                <div class="col pb-sm-2">
                    <article class="position-relative">
                        <div class="position-relative mb-3">
                            <a class="btn btn-icon btn-light btn-xs text-primary rounded-circle position-absolute top-0 end-0 m-3 zindex-5 hp-listing__action hp-listing__action--favorite active-state-v1"
                                data-bs-toggle="modal" href="#" data-component="toggle"><i
                                    class="hp-icon heart fi-heart"></i></a>
                            <div>
                                <div class="aspect-ratio aspect-w-219 aspect-h-100">
                                    <img class="w-full h-full object-center object-cover finder-hp-listing-images rounded-3"
                                        src=${frontend_static_url}/wp-content/uploads/2021/11/01.jpg
                                        alt="Course Image" loading="lazy">
                                </div>
                            </div>
                        </div>
                        <h4	class="mb-1 fs-xs fw-normal text-primary">
                            S.B.
                        </h4>
                        <h3 class="finder-hp-listing-title mb-1 fs-lg">
                            <a class="nav-link stretched-link" href=${course_detail_url}>
                                ${course["name"]}
                            </a>
                        </h3>
                        <p class="mb-2 fs-sm">
                            Harvard University<br>
                            <span class="mb-2 fs-xs text-muted">
                                Cambridge, MA, United States
                            </span>
                        </p>
                        <ul class="list-inline mb-0 fs-xs hp-listing__attributes hp-listing__attributes--secondary">
                            <li class="list-inline-item pe-1">
                                <i class="fi-cash mt-n1 me-1 fs-base align-middle"></i>
                                <span class="fw-bold">$${course["tuition_fee"]}</span>/year
                            </li>
                            <li class="list-inline-item pe-1">
                                <i class="fi-calendar mt-n1 me-1 fs-base align-middle"></i>
                                <span class="fw-bold">4 years</span>
                            </li>
                            <li class="list-inline-item pe-1">
                                <i class="fi-clock mt-n1 me-1 fs-base align-middle"></i>
                                <span class="fw-bold">Full-time</span>
                            </li>
                            <li class="list-inline-item pe-1">
                                <i class="fi-map-pin mt-n1 me-1 fs-base align-middle"></i>
                                <span class="fw-bold">On Campus</span>
                            </li>
                        </ul>
                    </article>
                </div>
            `;

        });

        
    })
    .catch((error) => {
        console.log(error);
    });
}