from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
import logging

app = Flask(__name__, static_folder='static', template_folder='templates')

# Setup logging
logging.basicConfig(level=logging.INFO)

def load_menu():
    try:
        with open('data/menu.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading menu: {e}")
        os.makedirs('data', exist_ok=True)
        default_menu = {
            "categories": [
                { "icon": "star", "label": "All", "itemCount": "15 Items", "active": True },
                { "icon": "fire", "label": "Diwali", "itemCount": "6 Items" },
                { "icon": "fill-drip", "label": "Holi", "itemCount": "3 Items" },
                { "icon": "om", "label": "Ganesh Chaturthi", "itemCount": "2 Items" },
                { "icon": "sun", "label": "Gudi Padwa", "itemCount": "2 Items" },
                { "icon": "feather", "label": "Makar Sankranti", "itemCount": "2 Items" }
            ],
            "foodItems": [
                {
                    "image": "/static/images/food1.jpg",
                    "title": "Chakali",
                    "price": 6.99,
                    "type": "Veg",
                    "category": "Diwali"
                },
                {
                    "image": "/static/images/food2.jpg",
                    "title": "Chivda",
                    "price": 4.99,
                    "type": "Veg",
                    "category": "Diwali"
                },
                {
                    "image": "/static/images/food3.jpg",
                    "title": "Karanji (Gujiya)",
                    "price": 7.49,
                    "type": "Veg",
                    "category": "Diwali"
                },
                {
                    "image": "/static/images/food4.jpg",
                    "title": "Laadoo",
                    "price": 5.49,
                    "discount": 10,
                    "type": "Veg",
                    "category": "Diwali"
                },
                {
                    "image": "/static/images/food5.jpg",
                    "title": "Vadi (Vadya)",
                    "price": 3.99,
                    "type": "Veg",
                    "category": "Diwali"
                },
                {
                    "image": "/static/images/food6.jpg",
                    "title": "Anarse",
                    "price": 8.99,
                    "type": "Veg",
                    "category": "Diwali"
                },
                {
                    "image": "/static/images/food1.jpg",
                    "title": "Puran Poli",
                    "price": 9.99,
                    "type": "Veg",
                    "category": "Holi"
                },
                {
                    "image": "/static/images/food2.jpg",
                    "title": "Gujiya (Sweet Dumpling)",
                    "price": 7.99,
                    "type": "Veg",
                    "category": "Holi"
                },
                {
                    "image": "/static/images/food3.jpg",
                    "title": "Thandai",
                    "price": 4.99,
                    "type": "Veg",
                    "category": "Holi"
                },
                {
                    "image": "/static/images/food4.jpg",
                    "title": "Modak (Fried)",
                    "price": 6.49,
                    "type": "Veg",
                    "category": "Ganesh Chaturthi"
                },
                {
                    "image": "/static/images/food5.jpg",
                    "title": "Ukadiche Modak",
                    "price": 7.49,
                    "type": "Veg",
                    "category": "Ganesh Chaturthi"
                },
                {
                    "image": "/static/images/food6.jpg",
                    "title": "Shrikhand",
                    "price": 8.99,
                    "type": "Veg",
                    "category": "Gudi Padwa"
                },
                {
                    "image": "/static/images/food1.jpg",
                    "title": "Kokum Sarbat",
                    "price": 3.49,
                    "type": "Veg",
                    "category": "Gudi Padwa"
                },
                {
                    "image": "/static/images/food2.jpg",
                    "title": "Tilgul Laddu",
                    "price": 4.49,
                    "type": "Veg",
                    "category": "Makar Sankranti"
                },
                {
                    "image": "/static/images/food3.jpg",
                    "title": "Gul Poli",
                    "price": 5.99,
                    "type": "Veg",
                    "category": "Makar Sankranti"
                }
            ]
        }
        with open('data/menu.json', 'w') as f:
            json.dump(default_menu, f, indent=4)
        return default_menu

def load_orders():
    try:
        with open('data/orders.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading orders: {e}")
        default_orders = {"orders": []}
        os.makedirs('data', exist_ok=True)
        with open('data/orders.json', 'w') as f:
            json.dump(default_orders, f, indent=4)
        return default_orders

def save_orders(orders):
    try:
        with open('data/orders.json', 'w') as f:
            json.dump(orders, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving orders: {e}")

@app.route('/')
def home():
    menu_data = load_menu()
    orders_data = load_orders()
    return render_template(
        'index.html',
        active_page='menu',
        categories=menu_data['categories'],
        foodItems=menu_data['foodItems'],
        orders=orders_data['orders']
    )

@app.route('/table-services')
def table_services():
    return render_template('table_services.html', active_page='table')

@app.route('/reservation')
def reservation():
    return render_template('reservation.html', active_page='reservation')

@app.route('/delivery')
def delivery():
    return render_template('delivery.html', active_page='delivery')

@app.route('/accounting')
def accounting():
    """
    Show a table of all orders from orders.json
    """
    data = load_orders()
    all_orders = data.get('orders', [])
    return render_template('accounting.html', active_page='accounting', orders=all_orders)

@app.route('/settings')
def settings():
    return render_template('settings.html', active_page='settings')

@app.route('/logout')
def logout():
    # Placeholder for logout
    return "<h2>You have been logged out (placeholder)</h2>"

# API Endpoints
@app.route('/api/menu', methods=['GET'])
def get_menu():
    return jsonify(load_menu())

@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify(load_orders())

@app.route('/api/place-order', methods=['POST'])
def place_order():
    """
    Receives JSON data:
    {
      "table": "Table 4",
      "customer": "Floyd Miles",
      "items": [...],
      "subtotal": 45.97,
      "tax": 2.30,
      "total": 48.27,
      "paymentMethod": "cash/card/qr"
    }
    """
    try:
        order_data = request.json
        orders = load_orders()

        order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        new_order = {
            "id": order_id,
            "table": order_data.get('table', 'Unknown'),
            "customer": order_data.get('customer', 'Guest'),
            "items": len(order_data.get('items', [])),
            "subtotal": order_data.get('subtotal', 0),
            "tax": order_data.get('tax', 0),
            "total": order_data.get('total', 0),
            "status": "Pending",
            "timestamp": datetime.now().isoformat(),
            "kitchen": "Kitchen",
            "paymentMethod": order_data.get('paymentMethod', 'Not Selected')
        }

        orders['orders'].append(new_order)
        save_orders(orders)
        logging.info(f"Order {order_id} placed successfully.")
        return jsonify({"success": True, "message": "Order placed successfully", "order_id": order_id})
    except Exception as e:
        logging.error(f"Error placing order: {e}")
        return jsonify({"success": False, "message": "Error placing order"}), 500

if __name__ == '__main__':
    app.run(debug=True)
