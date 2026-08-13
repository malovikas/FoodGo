
// ================================
// GET CART
// ================================

const cart =
    JSON.parse(localStorage.getItem("cart")) || [];


// ================================
// CART COUNT
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
// DISPLAY ORDER SUMMARY
// ================================

function displayCheckoutSummary() {

    const container =
        document.getElementById("checkout-items");

    if (!container) {
        return;
    }


    container.innerHTML = "";


    cart.forEach(item => {

        const quantity =
            item.quantity || 1;

        const itemTotal =
            item.price * quantity;


        const itemElement =
            document.createElement("div");

        itemElement.className =
            "checkout-item";


        itemElement.innerHTML = `

            <div class="checkout-item-name">

                <span>
                    ${item.image}
                </span>

                <span>
                    ${item.name}
                    × ${quantity}
                </span>

            </div>

            <strong>
                ₹${itemTotal}
            </strong>

        `;


        container.appendChild(
            itemElement
        );

    });


    calculateTotal();
}


// ================================
// CALCULATE TOTAL
// ================================

function calculateTotal() {

    let subtotal = 0;


    cart.forEach(item => {

        const quantity =
            item.quantity || 1;

        subtotal +=
            item.price * quantity;

    });


    const deliveryFee =
        subtotal > 0 ? 40 : 0;


    const tax =
        Math.round(subtotal * 0.05);


    const total =
        subtotal +
        deliveryFee +
        tax;


    document.getElementById(
        "checkout-subtotal"
    ).textContent = `₹${subtotal}`;


    document.getElementById(
        "checkout-delivery"
    ).textContent = `₹${deliveryFee}`;


    document.getElementById(
        "checkout-tax"
    ).textContent = `₹${tax}`;


    document.getElementById(
        "checkout-total"
    ).textContent = `₹${total}`;
}


// ================================
// PLACE ORDER
// ================================

const checkoutForm =
    document.getElementById("checkout-form");


checkoutForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();
        
        console.log("CHECKOUT SUBMIT FUNCTION CALLED");

        if (cart.length === 0) {

            alert(
                "Your cart is empty."
            );

            window.location.href =
                "menu.html";

            return;
        }


        // Get customer details

        const name =
            document.getElementById("name")
                .value.trim();


        const email =
            document.getElementById("email")
                .value.trim();


        const phone =
            document.getElementById("phone")
                .value.trim();


        const address =
            document.getElementById("address")
                .value.trim();


        const city =
            document.getElementById("city")
                .value.trim();


        const pincode =
            document.getElementById("pincode")
                .value.trim();


        const payment =
            document.querySelector(
                'input[name="payment"]:checked'
            ).value;


        // Calculate order amount

        let subtotal = 0;


        cart.forEach(item => {

            const quantity =
                item.quantity || 1;

            subtotal +=
                item.price * quantity;

        });


        const deliveryFee = 40;

        const tax =
            Math.round(subtotal * 0.05);

        const total =
            subtotal +
            deliveryFee +
            tax;


        // Generate Order ID

        const orderId =
            "FG" +
            Date.now();


        // Create order object

        const order = {

            orderId: orderId,

            customer: {

                name: name,

                email: email,

                phone: phone

            },

            deliveryAddress: {

                address: address,

                city: city,

                pincode: pincode

            },

            paymentMethod: payment,

            items: cart,

            subtotal: subtotal,

            deliveryFee: deliveryFee,

            tax: tax,

            total: total,

            status: "Order Placed",

            orderDate:
                new Date().toISOString()

        };

        // ================================
// SEND ORDER TO BACKEND
// ================================

try {

    const response = await fetch(
        `${API_BASE_URL}/api/orders`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(order)
        }
    );


    if (!response.ok) {

        const errorData =
            await response.json()
                .catch(() => ({}));

        throw new Error(
            errorData.error ||
            "Failed to place order"
        );
    }


    const backendOrder =
        await response.json();


// ================================
// CREATE PAYMENT
// ================================

const createdOrder =
    backendOrder.order || backendOrder;


const paymentResponse =
    await fetch(
        `${API_BASE_URL}/api/payments`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                order_id:
                    createdOrder.order_id,

                amount:
                    createdOrder.total,

                payment_method:
                    createdOrder.payment_method

            })
        }
    );


if (!paymentResponse.ok) {

    const paymentError =
        await paymentResponse.json()
            .catch(() => ({}));

    throw new Error(
        paymentError.error ||
        "Payment processing failed"
    );
}


const paymentData =
    await paymentResponse.json();

    localStorage.setItem(
    "latestPayment",
    JSON.stringify(
        paymentData.payment
        )
    );


console.log(
    "Payment created successfully:",
    paymentData
);


    console.log(
        "Order created successfully:",
        backendOrder
    );


    // Keep the backend response
    // available for order-success.js

    localStorage.setItem(
        "latestOrder",
        JSON.stringify(
            backendOrder.order || backendOrder
        )
    );


    // Empty cart only after
    // successful backend response

    localStorage.removeItem(
        "cart"
    );


    // Go to success page

    window.location.href =
        "order-success.html";


} catch (error) {

    console.error(
        "Order API error:",
        error
    );


    alert(
        "Unable to place your order. Please try again."
    );

    }
        
}
);


// ================================
// INITIALIZE
// ================================

updateCartCount();

displayCheckoutSummary();
