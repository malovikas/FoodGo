
// ================================
// CART COUNT
// ================================

// ================================
// CART COUNT
// ================================

function updateCartCount() {

    const cart =
        JSON.parse(
            localStorage.getItem("cart")
        ) || [];


    const cartCount =
        document.getElementById("cart-count");


    if (cartCount) {

        let totalItems = 0;


        cart.forEach(item => {

            totalItems +=
                item.quantity || 1;

        });


        cartCount.textContent =
            totalItems;

    }
}

updateCartCount();

// ================================
// SEARCH
// ================================

function searchFood() {

    const searchInput =
        document.getElementById("search-input");

    const searchValue =
        searchInput.value.trim();

    if (searchValue === "") {
        alert("Please enter food or restaurant name.");
        return;
    }

    alert(
        `Searching for "${searchValue}"...`
    );
}


// ================================
// LOAD RESTAURANTS FROM API
// ================================

async function loadRestaurants() {

    const container =
        document.getElementById(
            "restaurant-container"
        );

    if (!container) {
        return;
    }

    try {

        const response = await fetch(
            `${RESTAURANT_API_BASE_URL}/api/restaurants`
        );

        if (!response.ok) {

            throw new Error(
                "Failed to load restaurants"
            );

        }

        const restaurants =
            await response.json();

        console.log(
            "Restaurants from API:",
            restaurants
        );

        if (
            !Array.isArray(restaurants) ||
            restaurants.length === 0
        ) {

            console.log(
                "No restaurants returned by API."
            );

            return;
        }


        // Remove existing hard-coded cards

        container.innerHTML = "";


        // Create cards from API data

        restaurants.forEach(restaurant => {

            const card =
                document.createElement("div");

            card.className =
                "restaurant-card";


            card.innerHTML = `

                <div class="restaurant-image">
                    ${restaurant.image || "🍽️"}
                </div>

                <div class="restaurant-info">

                    <h3>
                        ${restaurant.name}
                    </h3>

                    <p class="cuisine">
                        ${restaurant.cuisine || ""}
                    </p>

                    <div class="restaurant-details">

                        <span class="rating">
                            ★ ${restaurant.rating || "4.5"}
                        </span>

                        <span>
                            ${restaurant.delivery_time || "30-40 min"}
                        </span>

                    </div>

                    <a
                        href="menu.html"
                        class="view-menu"
                    >
                        View Menu
                    </a>

                </div>
            `;


            container.appendChild(card);

        });


    } catch (error) {

        console.error(
            "Restaurant API error:",
            error
        );

    }
}


loadRestaurants();

// ================================
// SEARCH
// ================================

function searchFood() {

    const searchInput =
        document.getElementById("search-input");

    const searchValue =
        searchInput.value.trim();

    if (searchValue === "") {
        alert("Please enter food or restaurant name.");
        return;
    }

    alert(
        `Searching for "${searchValue}"...`
    );
}

