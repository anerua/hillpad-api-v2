
load_countries();

function load_countries() {

    const countries_list_element = document.getElementById("search-countries-list");

    // Continents
    let continents = {
        "Africa": "_AF",
        "Asia": "_AS",
        "Europe": "_EU",
        "North America": "_NA",
        "South America": "_SA",
        "Oceania": "_OC"
    }
    for (const continent in continents) {
        countries_list_element.innerHTML += `
            <li>
                <a class="dropdown-item" href="#">
                    <span class="dropdown-item-value d-none">${continents[continent]}</span>
                    <span class="dropdown-item-label hivepress-advanced">${continent}</span>
                </a>
            </li>`;
    }
 
    // Horizontal divide between continents and countries
    countries_list_element.innerHTML += `
        <div class="dropdown-item text-decoration-none">
            <hr>
        </div>`;

    // Fetch countries from backend and add to DOM
    fetch(api_url + "/academics/country/list", {
        method: "GET",
    })
    .then((response) => response.json())
    .then((countries_list) => {
        
        // Sort countries alphabetically
        countries_list.sort((country_a, country_b) => {
            let name_country_a = country_a["name"];
            let name_country_b = country_b["name"];
            
            if (name_country_a < name_country_b) return -1;
            if (name_country_a > name_country_b) return 1;
            return 0;
        });

        let alphabet_headings = [];
        countries_list.forEach((country) => {
            const country_name = country["name"];
            const country_short_code = country["short_code"];

            // Create Alphabet heading elements
            if (!alphabet_headings.includes(country_name[0])) {
                countries_list_element.innerHTML += `<div class="dropdown-item text-decoration-none">${country_name[0]}</div>`;
                alphabet_headings.push(country_name[0]);
            }

            // Country name and flag
            countries_list_element.innerHTML += `
                <li>
                    <a class="dropdown-item" href="#">
                        <i class="fg fg-${country_short_code} fs-lg opacity-60 me-2"></i>
                        <span class="dropdown-item-value d-none">${country_short_code}</span>
                        <span class="dropdown-item-label hivepress-advanced">${country_name}</span>
                    </a>
                </li>`;
            

        });
    })
    .catch((error) => {
        console.log(error);
    });
}


function load_courses() {

    // Fetch courses from backend and add to DOM
    fetch(api_url + "/academics/course/list", {
        method: "GET",
    })
    .then((response) => response.json())
    .then((courses_list) => {
        
        // Sort countries and display only featured courses
        
        // Add courses to DOM
        courses_list.forEach((course) => {
            const course_name = course["name"];

            // Create Alphabet heading elements
            if (!alphabet_headings.includes(country_name[0])) {
                countries_list_element.innerHTML += `<div class="dropdown-item text-decoration-none">${country_name[0]}</div>`;
                alphabet_headings.push(country_name[0]);
            }

            // Country name and flag
            countries_list_element.innerHTML += `
                <li>
                    <a class="dropdown-item" href="#">
                        <i class="fg fg-${country["short_code"]} fs-lg opacity-60 me-2"></i>
                        <span class="dropdown-item-value d-none">${country["short_code"]}</span>
                        <span class="dropdown-item-label hivepress-advanced">${country_name}</span>
                    </a>
                </li>`;
            

        });
    })
    .catch((error) => {
        console.log(error);
    });

}