from flask import Flask, render_template, jsonify, abort
from flask_cors import CORS
import json
import os
import urllib.parse

app = Flask(__name__)
CORS(app)

WHATSAPP_NUMBER = "918958595983"  # FIX: Add country code

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "products.json")


def load_products():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        products = json.load(f)

    # FIX: remove duplicate IDs
    unique = {}
    for p in products:
        unique[p['id']] = p
    return list(unique.values())


@app.route('/')
def home():
    return render_template('index.html', products=load_products())

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)

    if not product:
        abort(404)

    message = f"Hi, I want to order {product['name']} (₹{product['price']})"
    encoded = urllib.parse.quote(message)

    whatsapp_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"

    return render_template('product.html', product=product, whatsapp_link=whatsapp_link)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
