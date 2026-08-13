// ================================
// GET LATEST ORDER
// ================================

const order =
    JSON.parse(
        localStorage.getItem("latestOrder")
    );


// ================================
// CHECK ORDER
// ================================

if (!order) {

    alert("No recent order was found.");

    window.location.href = "index.html";

}


// ================================
// DISPLAY ORDER ID
// ================================

document.getElementById(
    "order-id"
).textContent =
    order.order_id || order.orderId;


// ================================
// ORDER STATUS
// ================================

document.getElementById(
    "order-status"
).textContent =
    order.status;


// ================================
// CUSTOMER DETAILS
// ================================

document.getElementById(
    "customer-name"
).textContent =
    order.customer.name;


document.getElementById(
    "customer-email"
).textContent =
    order.customer.email;


document.getElementById(
    "customer-phone"
).textContent =
    order.customer.phone;


// ================================
// DELIVERY ADDRESS
// ================================

const deliveryAddress =
    order.delivery_address ||
    order.deliveryAddress;


document.getElementById(
    "delivery-address"
).textContent =
    order.delivery_address.address;


document.getElementById(
    "delivery-city"
).textContent =
    `City: ${order.delivery_address.city}`;

document.getElementById(
    "delivery-pincode"
).textContent =
    `PIN Code: ${order.delivery_address.pincode}`;


// ================================
// PAYMENT
// ================================

document.getElementById(
    "payment-method"
).textContent =
    order.payment_method ||
    order.paymentMethod;


// ================================
// ORDERED ITEMS
// ================================

const orderedItemsContainer =
    document.getElementById(
        "ordered-items"
    );


// Clear existing items

orderedItemsContainer.innerHTML = "";


order.items.forEach(item => {

    const quantity =
        item.quantity || 1;


    const itemTotal =
        item.price * quantity;


    const itemElement =
        document.createElement("div");


    itemElement.className =
        "success-order-item";


    itemElement.innerHTML = `

        <div class="success-item-name">

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


    orderedItemsContainer.appendChild(
        itemElement
    );

});


// ================================
// TOTAL
// ================================

document.getElementById(
    "order-total"
).textContent =
    `₹${order.total}`;