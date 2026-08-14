// ==========================================
// GET RESTAURANT ID FROM URL
// ==========================================

const urlParams =
    new URLSearchParams(window.location.search);

const restaurantId =
    urlParams.get("restaurant") || "1";


// ==========================================
// MENU CONTAINER
// ==========================================

const menuContainer =
    document.getElementById("menu-container");


// ==========================================
// LOAD MENU FROM API
// ==========================================

async function loadMenu() {

    try {

        const response =
            await fetch(
                `${RESTAURANT_API_BASE_URL}/api/restaurants/${restaurantId}/menu`
            );

        if (!response.ok) {

            throw new Error(
                "Failed to load menu"
            );

        }

        const menuItems =
            await response.json();

        displayMenu(menuItems);

        loadRestaurantDetails();

    }
    catch (error) {

        console.error(
            "Menu API Error:",
            error
        );

        if (menuContainer) {

            menuContainer.innerHTML = `
                <p>
                    Unable to load menu.
                    Please try again.
                </p>
            `;

        }

    }

}


// ==========================================
// DISPLAY MENU
// ==========================================

function displayMenu(menuItems) {

    if (!menuContainer) {
        return;
    }

    menuContainer.innerHTML = "";


    menuItems.forEach(item => {

        const menuCard =
            document.createElement("div");

        menuCard.className =
            "menu-card";


        menuCard.innerHTML = `

            <div class="menu-image">
                ${item.image}
            </div>

            <div class="menu-info">

                <h3>
                    ${item.name}
                </h3>

                <p class="menu-description">
                    ${item.description}
                </p>

                <div class="menu-bottom">

                    <span class="menu-price">
                        ₹${item.price}
                    </span>

                    <button
                        class="add-cart-btn"
                        onclick='addToCart(${JSON.stringify(item)})'
                    >
                        Add to Cart
                    </button>

                </div>

            </div>

        `;


        menuContainer.appendChild(menuCard);

    });

}


// ==========================================
// LOAD RESTAURANT DETAILS
// ==========================================

async function loadRestaurantDetails() {

    try {

        const response =
            await fetch(
                `${RESTAURANT_API_BASE_URL}/api/restaurants/${restaurantId}`
            );

        if (!response.ok) {
            return;
        }

        const restaurant =
            await response.json();


        const restaurantName =
            document.querySelector(
                ".restaurant-header h1"
            );


        const restaurantDescription =
            document.querySelector(
                ".restaurant-header p"
            );


        const rating =
            document.querySelector(
                ".restaurant-meta .rating"
            );


        const meta =
            document.querySelectorAll(
                ".restaurant-meta span"
            );


        if (restaurantName) {

            restaurantName.textContent =
                restaurant.name;

        }


        if (restaurantDescription) {

            restaurantDescription.textContent =
                restaurant.cuisine;

        }


        if (rating) {

            rating.textContent =
                `★ ${restaurant.rating}`;

        }


        if (meta.length > 1) {

            meta[1].textContent =
                restaurant.delivery_time;

        }


        if (meta.length > 2) {

            meta[2].textContent =
                `₹${restaurant.price_for_two} for two`;

        }

    }
    catch (error) {

        console.error(
            "Restaurant API Error:",
            error
        );

    }

}


// ==========================================
// ADD TO CART
// ==========================================

function addToCart(item) {

    let cart =
        JSON.parse(
            localStorage.getItem("cart")
        ) || [];


    // --------------------------------------
    // Check if item already exists
    // --------------------------------------

    const existingItem =
        cart.find(
            cartItem =>
                cartItem.id === item.id
        );


    if (existingItem) {

        existingItem.quantity =
            (existingItem.quantity || 1) + 1;

    }
    else {

        item.quantity = 1;

        cart.push(item);

    }


    // --------------------------------------
    // Save cart
    // --------------------------------------

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );


    // --------------------------------------
    // Update cart count immediately
    // --------------------------------------

    updateCartCount();


    // --------------------------------------
    // Message
    // --------------------------------------

    alert(
        `${item.name} added to cart!`
    );

}


// ==========================================
// UPDATE CART COUNT
// ==========================================

function updateCartCount() {

    const cart =
        JSON.parse(
            localStorage.getItem("cart")
        ) || [];


    const cartCount =
        document.getElementById(
            "cart-count"
        );


    if (!cartCount) {
        return;
    }


    let totalItems = 0;


    cart.forEach(item => {

        totalItems +=
            item.quantity || 1;

    });


    cartCount.textContent =
        totalItems;

}


// ==========================================
// INITIALIZE
// ==========================================

loadMenu();

updateCartCount();