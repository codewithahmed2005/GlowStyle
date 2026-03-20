from flask import Flask, render_template, jsonify, abort
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Configuration
WHATSAPP_NUMBER = "8958595983"  # Replace with your business number

# Get the directory where app.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "products.json")

# Default products data
DEFAULT_PRODUCTS = [
    {
        "id": 1,
        "name": "Radiance Serum",
        "price": 48.00,
        "currency": "USD",
        "description": "A lightweight vitamin C serum that brightens skin tone and reduces dark spots. Formulated with hyaluronic acid for deep hydration and natural glow.",
        "image_url": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&q=80",
        "category": "Skincare",
        "tag": "Bestseller"
    },
    {
        "id": 2,
        "name": "Silk Glow Foundation",
        "price": 62.00,
        "currency": "USD",
        "description": "Medium-coverage foundation with a luminous finish. Infused with skincare ingredients that improve skin texture while providing flawless coverage.",
        "image_url": "https://images.unsplash.com/photo-1631730486784-5456119f69ae?w=800&q=80",
        "category": "Makeup",
        "tag": "New Arrival"
    },
    {
        "id": 3,
        "name": "Midnight Recovery Oil",
        "price": 85.00,
        "currency": "USD",
        "description": "Luxurious overnight facial oil with evening primrose and lavender essential oil. Wake up to replenished, youthful-looking skin.",
        "image_url": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800&q=80",
        "category": "Skincare",
        "tag": None
    },
    {
        "id": 4,
        "name": "Velvet Matte Lipstick",
        "price": 32.00,
        "currency": "USD",
        "description": "Long-lasting matte lipstick in universally flattering shades. Enriched with shea butter to prevent drying while maintaining bold color payoff.",
        "image_url": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800&q=80",
        "category": "Makeup",
        "tag": "Limited Edition"
    },
    {
        "id": 5,
        "name": "Rose Quartz Facial Roller",
        "price": 28.00,
        "currency": "USD",
        "description": "Authentic rose quartz stone roller for facial massage. Reduces puffiness, promotes lymphatic drainage, and enhances product absorption.",
        "image_url": "https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=800&q=80",
        "category": "Tools",
        "tag": None
    },
    {
        "id": 6,
        "name": "Hydrating Mist",
        "price": 24.00,
        "currency": "USD",
        "description": "Refreshing facial spray with rose water and aloe vera. Perfect for setting makeup or midday hydration boost.",
        "image_url": "https://images.unsplash.com/photo-1607006412363-e7b93cc591c9?w=800&q=80",
        "category": "Skincare",
        "tag": "Vegan"
    }
]

def init_data_file():
    """Create products.json if it doesn't exist"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_PRODUCTS, f, indent=2)
        print(f"Created {DATA_FILE}")

def load_products():
    """Load products from JSON file"""
    init_data_file()  # Ensure file exists
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    """Serve homepage with product grid"""
    products = load_products()
    return render_template('index.html', products=products)

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
    """Serve individual product page"""
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        abort(404)
    
    # Generate WhatsApp link with pre-filled message
    message = f"Hi, I want to order {product['name']} from GlowStyle"
    whatsapp_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={message.replace(' ', '%20')}"
    
    return render_template('product.html', product=product, whatsapp_link=whatsapp_link)

@app.route('/products')
def api_products():
    """API endpoint for all products"""
    return jsonify(load_products())

@app.route('/products/<int:product_id>')
def api_product(product_id):
    """API endpoint for single product"""
    products = load_products()
    product = next((p for p in products if p['id'] == product_id), None)
    
    if not product:
        abort(404)
    return jsonify(product)


if __name__ == '__main__':
    app.run(debug=True, port=5000)