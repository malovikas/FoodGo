from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)

CORS(app)


# ==========================================
# TEMPORARY PAYMENT STORAGE
# ==========================================

payments = []


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "service": "payment-service",
        "status": "healthy"
    })


# ==========================================
# CREATE PAYMENT
# ==========================================

@app.route("/api/payments", methods=["POST"])
def create_payment():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400


    order_id = data.get("order_id")
    amount = data.get("amount")
    payment_method = data.get("payment_method")


    if not order_id:

        return jsonify({
            "error": "Order ID is required"
        }), 400


    if amount is None:

        return jsonify({
            "error": "Payment amount is required"
        }), 400


    if not payment_method:

        return jsonify({
            "error": "Payment method is required"
        }), 400


    # --------------------------------------
    # Generate Payment ID
    # --------------------------------------

    payment_id = (
        "PAY-" +
        str(uuid.uuid4())[:8].upper()
    )


    # --------------------------------------
    # Simulate Payment
    # --------------------------------------

    if payment_method == "Cash on Delivery":

        status = "Pending"

    else:

        status = "Success"


    payment = {

        "payment_id": payment_id,

        "order_id": order_id,

        "amount": amount,

        "payment_method": payment_method,

        "status": status,

        "created_at":
            datetime.now().isoformat()

    }


    payments.append(payment)


    return jsonify({

        "message":
            "Payment processed successfully",

        "payment":
            payment

    }), 201


# ==========================================
# GET ALL PAYMENTS
# ==========================================

@app.route("/api/payments", methods=["GET"])
def get_payments():

    return jsonify(payments)


# ==========================================
# GET PAYMENT BY ID
# ==========================================

@app.route("/api/payments/<payment_id>",
           methods=["GET"])
def get_payment(payment_id):

    for payment in payments:

        if payment["payment_id"] == payment_id:

            return jsonify(payment)


    return jsonify({
        "error": "Payment not found"
    }), 404


# ==========================================
# UPDATE PAYMENT STATUS
# ==========================================

@app.route(
    "/api/payments/<payment_id>/status",
    methods=["PUT"]
)
def update_payment_status(payment_id):

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "Request body is required"
        }), 400


    new_status = data.get("status")


    allowed_statuses = [

        "Pending",

        "Success",

        "Failed",

        "Refunded"

    ]


    if new_status not in allowed_statuses:

        return jsonify({

            "error":
                "Invalid payment status",

            "allowed_statuses":
                allowed_statuses

        }), 400


    for payment in payments:

        if payment["payment_id"] == payment_id:

            payment["status"] =  new_status


            return jsonify({

                "message":
                    "Payment status updated",

                "payment":
                    payment

            })


    return jsonify({
        "error": "Payment not found"
    }), 404


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5004,

        debug=True

    )
