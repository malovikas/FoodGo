from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


# ==========================================
# RESTAURANT DATA
# ==========================================

restaurants = [

    {
        "id": 1,
        "name": "Pizza Palace",
        "cuisine": "Italian • Pizza • Fast Food",
        "rating": 4.5,
        "delivery_time": "30-40 min",
        "price_for_two": 200
    },

    {
        "id": 2,
        "name": "Burger House",
        "cuisine": "Burgers • Fast Food • Beverages",
        "rating": 4.3,
        "delivery_time": "25-35 min",
        "price_for_two": 250
    },

    {
        "id": 3,
        "name": "Spice Garden",
        "cuisine": "Indian • North Indian • Thali",
        "rating": 4.6,
        "delivery_time": "30-45 min",
        "price_for_two": 350
    },

    {
        "id": 4,
        "name": "Dragon Wok",
        "cuisine": "Chinese • Asian • Noodles",
        "rating": 4.4,
        "delivery_time": "25-40 min",
        "price_for_two": 300
    }

]


# ==========================================
# MENU DATA
# ==========================================

menus = {

    1: [

        {
            "id": 1,
            "restaurant_id": 1,
            "name": "Margherita Pizza",
            "description":
                "Classic pizza with tomato sauce, mozzarella and fresh basil.",
            "price": 249,
            "image": "🍕"
        },

        {
            "id": 2,
            "restaurant_id": 1,
            "name": "Farmhouse Pizza",
            "description":
                "Loaded with fresh vegetables, mushrooms and mozzarella.",
            "price": 349,
            "image": "🍕"
        },

        {
            "id": 3,
            "restaurant_id": 1,
            "name": "Pepperoni Pizza",
            "description":
                "Cheesy pizza topped with delicious pepperoni slices.",
            "price": 399,
            "image": "🍕"
        },

        {
            "id": 4,
            "restaurant_id": 1,
            "name": "Cheese Burst Pizza",
            "description":
                "Extra cheesy pizza with a delicious cheese-filled crust.",
            "price": 449,
            "image": "🧀"
        },

        {
            "id": 5,
            "restaurant_id": 1,
            "name": "Garlic Bread",
            "description":
                "Freshly baked garlic bread with herbs and butter.",
            "price": 149,
            "image": "🥖"
        },

        {
            "id": 6,
            "restaurant_id": 1,
            "name": "Chocolate Lava Cake",
            "description":
                "Warm chocolate cake filled with rich molten chocolate.",
            "price": 179,
            "image": "🍫"
        }

    ],

    2: [

        {
            "id": 7,
            "restaurant_id": 2,
            "name": "Classic Burger",
            "description":
                "Juicy chicken patty with lettuce, tomato and sauce.",
            "price": 199,
            "image": "🍔"
        },

        {
            "id": 8,
            "restaurant_id": 2,
            "name": "Cheese Burger",
            "description":
                "Classic burger topped with melted cheese.",
            "price": 249,
            "image": "🍔"
        },

        {
            "id": 9,
            "restaurant_id": 2,
            "name": "Crispy Chicken Burger",
            "description":
                "Crispy chicken patty with fresh vegetables and sauce.",
            "price": 299,
            "image": "🍔"
        }

    ],

    3: [

        {
            "id": 10,
            "restaurant_id": 3,
            "name": "Paneer Butter Masala",
            "description":
                "Soft paneer cooked in a rich creamy tomato gravy.",
            "price": 249,
            "image": "🍛"
        },

        {
            "id": 11,
            "restaurant_id": 3,
            "name": "Veg Thali",
            "description":
                "Complete Indian meal with vegetables, dal, rice and bread.",
            "price": 299,
            "image": "🍛"
        },

        {
            "id": 12,
            "restaurant_id": 3,
            "name": "Biryani",
            "description":
                "Aromatic basmati rice cooked with Indian spices.",
            "price": 279,
            "image": "🍚"
        }

    ],

    4: [

        {
            "id": 13,
            "restaurant_id": 4,
            "name": "Hakka Noodles",
            "description":
                "Stir-fried noodles with vegetables and Asian sauces.",
            "price": 199,
            "image": "🍜"
        },

        {
            "id": 14,
            "restaurant_id": 4,
            "name": "Manchurian",
            "description":
                "Crispy vegetable balls tossed in spicy Manchurian sauce.",
            "price": 229,
            "image": "🥡"
        },

        {
            "id": 15,
            "restaurant_id": 4,
            "name": "Fried Rice",
            "description":
                "Chinese-style fried rice with fresh vegetables.",
            "price": 189,
            "image": "🍚"
        }

    ]

}


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "service": "restaurant-service",
        "status": "healthy"
    })


# ==========================================
# GET ALL RESTAURANTS
# ==========================================

@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():

    return jsonify(restaurants)


# ==========================================
# GET RESTAURANT BY ID
# ==========================================

@app.route("/api/restaurants/<int:restaurant_id>",
           methods=["GET"])
def get_restaurant(restaurant_id):

    for restaurant in restaurants:

        if restaurant["id"] == restaurant_id:

            return jsonify(restaurant)


    return jsonify({
        "error": "Restaurant not found"
    }), 404


# ==========================================
# GET RESTAURANT MENU
# ==========================================

@app.route("/api/restaurants/<int:restaurant_id>/menu",
           methods=["GET"])
def get_restaurant_menu(restaurant_id):

    # Check restaurant exists

    restaurant_exists = any(
        restaurant["id"] == restaurant_id
        for restaurant in restaurants
    )


    if not restaurant_exists:

        return jsonify({
            "error": "Restaurant not found"
        }), 404


    return jsonify(
        menus.get(restaurant_id, [])
    )


# ==========================================
# GET ALL MENU ITEMS
# ==========================================

@app.route("/api/menu", methods=["GET"])
def get_all_menu():

    all_items = []


    for restaurant_menu in menus.values():

        all_items.extend(restaurant_menu)


    return jsonify(all_items)




# ==========================================
# GET MENU ITEM BY ID
# ==========================================
@app.route("/api/menu/<int:item_id>", methods=["GET"])
def get_menu_item(item_id):

    for restaurant_menu in menus.values():

        for item in restaurant_menu:

            if item["id"] == item_id:

                return jsonify(item)

    return jsonify({
        "error": "Menu item not found"
    }), 404

# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True
    )

