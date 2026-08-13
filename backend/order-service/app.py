from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)

CORS(app)


# ==========================================
# TEMPORARY ORDER STORAGE
# ==========================================

orders = []


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "service": "order-service",
        "status": "healthy"
    })


# ==========================================
# CREATE ORDER
# ==========================================

@app.route("/api/orders", methods=["POST"])
def create_order():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400


    # --------------------------------------
    # Customer
    # --------------------------------------

    customer = data.get("customer")


    if not customer:

        return jsonify({
            "error": "Customer information is required"
        }), 400


    name = customer.get("name")
    email = customer.get("email")
    phone = customer.get("phone")


    if not name or not email or not phone:

        return jsonify({
            "error":
                "Customer name, email and phone are required"
        }), 400


    # --------------------------------------
    # Delivery Address
    # --------------------------------------

    delivery_address = data.get("deliveryAddress")


    if not delivery_address:

        return jsonify({
            "error":
                "Delivery address is required"
        }), 400


    # --------------------------------------
    # Items
    # --------------------------------------

    items = data.get("items")


    if not items:

        return jsonify({
            "error":
                "At least one item is required"
        }), 400


    # --------------------------------------
    # Payment
    # --------------------------------------

    payment_method =   data.get("paymentMethod")


    if not payment_method:

        return jsonify({
            "error":
                "Payment method is required"
        }), 400


    # --------------------------------------
    # Amount
    # --------------------------------------

    subtotal = data.get("subtotal", 0)

    delivery_fee =        data.get("deliveryFee", 40)

    tax =    data.get("tax", 0)

    total =     data.get("total", 0)


    # --------------------------------------
    # Generate Order ID
    # --------------------------------------

    order_id = (
        "FG-" +
        datetime.now().strftime("%Y%m%d") +
        "-" +
        str(uuid.uuid4())[:8].upper()
    )


    # --------------------------------------
    # Create Order
    # --------------------------------------

    order = {

        "order_id": order_id,

        "customer": {

            "name": name,

            "email": email,

            "phone": phone

        },

        "delivery_address":
            delivery_address,

        "items": items,

        "payment_method":
            payment_method,

        "subtotal":
            subtotal,

        "delivery_fee":
            delivery_fee,

        "tax":
            tax,

        "total":
            total,

        "status":
            "Order Placed",

        "created_at":
            datetime.now().isoformat()

    }


    orders.append(order)


    return jsonify({

        "message":
            "Order created successfully",

        "order":
            order

    }), 201


# ==========================================
# GET ALL ORDERS
# ==========================================

@app.route("/api/orders", methods=["GET"])
def get_orders():

    return jsonify(orders)


# ==========================================
# GET ORDER BY ID
# ==========================================

@app.route("/api/orders/<order_id>",
           methods=["GET"])
def get_order(order_id):

    for order in orders:

        if order["order_id"] == order_id:

            return jsonify(order)


    return jsonify({
        "error": "Order not found"
    }), 404


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@app.route(
    "/api/orders/<order_id>/status",
    methods=["PUT"]
)
def update_order_status(order_id):

    data = request.get_json()


    if not data:

        return jsonify({
            "error":
                "Request body is required"
        }), 400


    new_status =        data.get("status")


    if not new_status:

        return jsonify({
            "error":
                "Status is required"
        }), 400


    allowed_statuses = [

        "Order Placed",

        "Confirmed",

        "Preparing",

        "Out for Delivery",

        "Delivered",

        "Cancelled"

    ]


    if new_status not in allowed_statuses:

        return jsonify({

            "error":
                "Invalid order status",

            "allowed_statuses":
                allowed_statuses

        }), 400


    for order in orders:

        if order["order_id"] == order_id:

            order["status"] =                new_status


            return jsonify({

                "message":
                    "Order status updated",

                "order":
                    order

            })


    return jsonify({
        "error":
            "Order not found"
    }), 404


# ==========================================
# DELETE ORDER
# ==========================================

@app.route(
    "/api/orders/<order_id>",
    methods=["DELETE"]
)
def delete_order(order_id):

    for order in orders:

        if order["order_id"] == order_id:

            orders.remove(order)


            return jsonify({

                "message":
                    "Order deleted successfully"

            })


    return jsonify({
        "error":
            "Order not found"
    }), 404


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5003,

        debug=True

    )

