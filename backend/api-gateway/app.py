from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# MICROSERVICE URLs
# ==========================================

USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL"
)

RESTAURANT_SERVICE_URL = os.getenv(
    "RESTAURANT_SERVICE_URL"
)

ORDER_SERVICE_URL = os.getenv(
    "ORDER_SERVICE_URL"
)

PAYMENT_SERVICE_URL = os.getenv(
    "PAYMENT_SERVICE_URL"
)


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    services = {}

    # -------------------------------
    # User Service
    # -------------------------------

    try:

        response = requests.get(
            f"{USER_SERVICE_URL}/health",
            timeout=3
        )

        services["user-service"] = (
            "healthy"
            if response.status_code == 200
            else "unhealthy"
        )

    except requests.exceptions.RequestException:

        services["user-service"] = "unavailable"


    # -------------------------------
    # Restaurant Service
    # -------------------------------

    try:

        response = requests.get(
            f"{RESTAURANT_SERVICE_URL}/health",
            timeout=3
        )

        services["restaurant-service"] = (
            "healthy"
            if response.status_code == 200
            else "unhealthy"
        )

    except requests.exceptions.RequestException:

        services["restaurant-service"] = "unavailable"


    # -------------------------------
    # Order Service
    # -------------------------------

    try:

        response = requests.get(
            f"{ORDER_SERVICE_URL}/health",
            timeout=3
        )

        services["order-service"] = (
            "healthy"
            if response.status_code == 200
            else "unhealthy"
        )

    except requests.exceptions.RequestException:

        services["order-service"] = "unavailable"


    # -------------------------------
    # Payment Service
    # -------------------------------

    try:

        response = requests.get(
            f"{PAYMENT_SERVICE_URL}/health",
            timeout=3
        )

        services["payment-service"] = (
            "healthy"
            if response.status_code == 200
            else "unhealthy"
        )

    except requests.exceptions.RequestException:

        services["payment-service"] = "unavailable"


    return jsonify({

        "service": "api-gateway",

        "status": "running",

        "services": services

    })


# ==========================================
# USER SERVICE
# ==========================================

@app.route(
    "/api/users",
    methods=["GET", "POST"]
)
def users():

    try:

        if request.method == "POST":

            response = requests.post(

                f"{USER_SERVICE_URL}/api/users",

                json=request.get_json(),

                timeout=5

            )

        else:

            response = requests.get(

                f"{USER_SERVICE_URL}/api/users",

                timeout=5

            )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "User service unavailable"

        }), 503


# ==========================================
# USER BY ID
# ==========================================

@app.route(
    "/api/users/<user_id>",
    methods=["GET", "DELETE"]
)
def user_by_id(user_id):

    try:

        url = (
            f"{USER_SERVICE_URL}"
            f"/api/users/{user_id}"
        )


        if request.method == "DELETE":

            response = requests.delete(

                url,

                timeout=5

            )

        else:

            response = requests.get(

                url,

                timeout=5

            )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "User service unavailable"

        }), 503


# ==========================================
# RESTAURANTS
# ==========================================

@app.route(
    "/api/restaurants",
    methods=["GET"]
)
def restaurants():

    try:

        response = requests.get(

            f"{RESTAURANT_SERVICE_URL}"
            "/api/restaurants",

            timeout=5

        )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Restaurant service unavailable"

        }), 503


# ==========================================
# RESTAURANT BY ID
# ==========================================

@app.route(
    "/api/restaurants/<int:restaurant_id>",
    methods=["GET"]
)
def restaurant_by_id(restaurant_id):

    try:

        response = requests.get(

            f"{RESTAURANT_SERVICE_URL}"
            f"/api/restaurants/{restaurant_id}",

            timeout=5

        )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Restaurant service unavailable"

        }), 503


# ==========================================
# RESTAURANT MENU
# ==========================================

@app.route(
    "/api/restaurants/<int:restaurant_id>/menu",
    methods=["GET"]
)
def restaurant_menu(restaurant_id):

    try:

        response = requests.get(

            f"{RESTAURANT_SERVICE_URL}"
            f"/api/restaurants/{restaurant_id}/menu",

            timeout=5

        )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Restaurant service unavailable"

        }), 503


# ==========================================
# ALL MENU ITEMS
# ==========================================

@app.route(
    "/api/menu",
    methods=["GET"]
)
def menu():

    try:

        response = requests.get(

            f"{RESTAURANT_SERVICE_URL}"
            "/api/menu",

            timeout=5

        )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Restaurant service unavailable"

        }), 503


# ==========================================
# ORDERS
# ==========================================

@app.route(
    "/api/orders",
    methods=["GET", "POST"]
)
def orders():

    try:

        if request.method == "POST":

            response = requests.post(

                f"{ORDER_SERVICE_URL}/api/orders",

                json=request.get_json(),

                timeout=5

            )

        else:

            response = requests.get(

                f"{ORDER_SERVICE_URL}/api/orders",

                timeout=5

            )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Order service unavailable"

        }), 503


# ==========================================
# ORDER BY ID
# ==========================================

@app.route(
    "/api/orders/<order_id>",
    methods=["GET", "DELETE"]
)
def order_by_id(order_id):

    try:

        url = (
            f"{ORDER_SERVICE_URL}"
            f"/api/orders/{order_id}"
        )


        if request.method == "DELETE":

            response = requests.delete(

                url,

                timeout=5

            )

        else:

            response = requests.get(

                url,

                timeout=5

            )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Order service unavailable"

        }), 503


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@app.route(
    "/api/orders/<order_id>/status",
    methods=["PUT"]
)
def order_status(order_id):

    try:

        response = requests.put(

            f"{ORDER_SERVICE_URL}"
            f"/api/orders/{order_id}/status",

            json=request.get_json(),

            timeout=5

        )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Order service unavailable"

        }), 503


# ==========================================
# PAYMENTS
# ==========================================

@app.route(
    "/api/payments",
    methods=["GET", "POST"]
)
def payments():

    try:

        if request.method == "POST":

            response = requests.post(

                f"{PAYMENT_SERVICE_URL}"
                "/api/payments",

                json=request.get_json(),

                timeout=5

            )

        else:

            response = requests.get(

                f"{PAYMENT_SERVICE_URL}"
                "/api/payments",

                timeout=5

            )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Payment service unavailable"

        }), 503


# ==========================================
# PAYMENT BY ID
# ==========================================

@app.route(
    "/api/payments/<payment_id>",
    methods=["GET"]
)
def payment_by_id(payment_id):

    try:

        response = requests.get(

            f"{PAYMENT_SERVICE_URL}"
            f"/api/payments/{payment_id}",

            timeout=5

        )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Payment service unavailable"

        }), 503


# ==========================================
# UPDATE PAYMENT STATUS
# ==========================================

@app.route(
    "/api/payments/<payment_id>/status",
    methods=["PUT"]
)
def payment_status(payment_id):

    try:

        response = requests.put(

            f"{PAYMENT_SERVICE_URL}"
            f"/api/payments/{payment_id}/status",

            json=request.get_json(),

            timeout=5

        )


        return (

            response.content,

            response.status_code,

            response.headers.items()

        )


    except requests.exceptions.RequestException:

        return jsonify({

            "error":
                "Payment service unavailable"

        }), 503


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )

