
// ================================
// GET CART
// ================================

let cart =
    JSON.parse(localStorage.getItem("cart")) || [];


// ================================
// DISPLAY CART
// ================================

function displayCart() {

    const cartContainer =
        document.getElementById("cart-items");

    if (!cartContainer) {
        return;
    }


    // Empty cart
    if (cart.length === 0) {

        cartContainer.innerHTML = `

            <div class="empty-cart">

                <div class="empty-cart-icon">
                    🛒
                </div>

                <h2>
                    Your cart is empty
                </h2>

                <p>
                    Add some delicious food to get started.
                </p>

                <a
                    href="menu.html"
                    class="browse-food-btn"
                >
                    Browse Food
                </a>

            </div>

        `;

        updateSummary();

        return;
    }


    cartContainer.innerHTML = "";


    cart.forEach((item, index) => {

        const cartItem =
            document.createElement("div");

        cartItem.className = "cart-item";


        cartItem.innerHTML = `

            <div class="cart-item-info">

                <div class="cart-item-image">
                    ${item.image}
                </div>

                <div class="cart-item-details">

                    <h3>
                        ${item.name}
                    </h3>

                    <p class="cart-item-price">
                        ₹${item.price} per item
                    </p>

                </div>

            </div>


            <div class="quantity-control">

                <button
                    class="quantity-btn"
                    onclick="decreaseQuantity(${index})"
                >
                    −
                </button>

                <span class="quantity">
                    ${item.quantity || 1}
                </span>

                <button
                    class="quantity-btn"
                    onclick="increaseQuantity(${index})"
                >
                    +
                </button>

            </div>


            <strong>
                ₹${item.price * (item.quantity || 1)}
            </strong>


            <button
                class="remove-btn"
                onclick="removeItem(${index})"
            >
                Remove
            </button>

        `;


        cartContainer.appendChild(cartItem);

    });


    updateSummary();

    updateCartCount();
}


// ================================
// INCREASE QUANTITY
// ================================

function increaseQuantity(index) {

    if (!cart[index].quantity) {
        cart[index].quantity = 1;
    }

    cart[index].quantity++;

    saveCart();

    displayCart();
}


// ================================
// DECREASE QUANTITY
// ================================

function decreaseQuantity(index) {

    if (!cart[index].quantity) {
        cart[index].quantity = 1;
    }

    if (cart[index].quantity > 1) {

        cart[index].quantity--;

    } else {

        cart.splice(index, 1);

    }

    saveCart();

    displayCart();
}


// ================================
// REMOVE ITEM
// ================================

function removeItem(index) {

    cart.splice(index, 1);

    saveCart();

    displayCart();
}


// ================================
// SAVE CART
// ================================

function saveCart() {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );
}


// ================================
// UPDATE CART COUNT
// ================================

function updateCartCount() {

    const cartCount =
        document.getElementById("cart-count");

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


// ================================
// CALCULATE SUMMARY
// ================================

function updateSummary() {

    let subtotal = 0;


    cart.forEach(item => {

        const quantity =
            item.quantity || 1;

        subtotal +=
            item.price * quantity;

    });


    const deliveryFee =
        subtotal > 0 ? 40 : 0;


    const taxes =
        Math.round(subtotal * 0.05);


    const total =
        subtotal +
        deliveryFee +
        taxes;


    document.getElementById("subtotal")
        .textContent = `₹${subtotal}`;

    document.getElementById("delivery-fee")
        .textContent = `₹${deliveryFee}`;

    document.getElementById("taxes")
        .textContent = `₹${taxes}`;

    document.getElementById("total")
        .textContent = `₹${total}`;


    const checkoutButton =
        document.getElementById("checkout-btn");


    if (checkoutButton) {

        checkoutButton.disabled =
            cart.length === 0;

        checkoutButton.style.opacity =
            cart.length === 0 ? "0.5" : "1";

    }
}


// ================================
// CHECKOUT
// ================================

function proceedToCheckout() {

    if (cart.length === 0) {

        alert(
            "Your cart is empty."
        );

        return;
    }


    window.location.href =
        "checkout.html";
}


// ================================
// INITIALIZE
// ================================

displayCart();
updateCartCount();
