from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
# A secret key is needed to use sessions
app.secret_key = os.urandom(24)

# Dummy product data (in a real app, this would come from a database)
PRODUCTS = {
    1: {'id': 1, 'name': 'Classic Leather Watch', 'price': 150.00, 'description': 'A timeless piece with a genuine leather strap.', 'image': 'images/watch.jpg'},
    2: {'id': 2, 'name': 'Wireless Bluetooth Headphones', 'price': 75.50, 'description': 'High-fidelity sound with 20 hours of battery life.', 'image': 'images/headphones.jpg'},
    3: {'id': 3, 'name': 'Modern Minimalist Backpack', 'price': 45.00, 'description': 'Sleek, durable, and water-resistant. Perfect for daily commute.', 'image': 'images/backpack.jpg'},
    4: {'id': 4, 'name': 'Stainless Steel Water Bottle', 'price': 25.00, 'description': 'Keeps your drinks cold for 24 hours or hot for 12 hours.', 'image': 'images/bottle.jpg'},
    5: {'id': 5, 'name': 'Ergonomic Office Chair', 'price': 250.00, 'description': 'Supports your posture for a comfortable workday.', 'image': 'images/chair.jpg'},
    6: {'id': 6, 'name': 'Smart Home Hub', 'price': 99.99, 'description': 'Control all your smart devices from one central hub.', 'image': 'images/hub.jpg'}
}
# NOTE: You need to create a 'static/images' folder and add the corresponding images
# (watch.jpg, headphones.jpg, etc.) for the app to display them.

@app.context_processor
def utility_processor():
    def get_cart_count():
        return len(session.get('cart', []))
    def get_cart_items():
        cart_product_ids = session.get('cart', [])
        return [PRODUCTS[pid] for pid in cart_product_ids if pid in PRODUCTS]
    return dict(get_cart_count=get_cart_count, get_cart_items=get_cart_items)

@app.route('/')
def home():
    """Renders the home page with a list of all products."""
    products_list = list(PRODUCTS.values())
    return render_template('index.html', products=products_list)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Renders the detail page for a single product."""
    product = PRODUCTS.get(product_id)
    if product:
        return render_template('product.html', product=product)
    return 'Product not found', 404

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Adds a product to the cart stored in the session."""
    cart = session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
        session['cart'] = cart
        flash(f"{PRODUCTS[product_id]['name']} added to cart!", 'success')
    else:
        flash('Item is already in your cart.', 'info')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/cart')
def view_cart():
    """Displays the contents of the shopping cart."""
    cart_product_ids = session.get('cart', [])
    cart_products = [PRODUCTS[pid] for pid in cart_product_ids if pid in PRODUCTS]
    total_price = sum(product['price'] for product in cart_products)
    return render_template('cart.html', cart_items=cart_products, total_price=total_price)

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    """Removes an item from the cart."""
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        session['cart'] = cart
        flash(f"{PRODUCTS[product_id]['name']} removed from cart.", 'success')
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    """Placeholder for the checkout process."""
    # In a real app, this would lead to a payment gateway
    session.pop('cart', None) # Clear cart after checkout
    flash('Thank you for your purchase!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
