
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os

app = Flask(__name__)
# Use an environment variable for the secret key in a real app
app.secret_key = os.urandom(24)

# --- UI Theme Configuration ---
# This dictionary provides styling values for a modern look and feel.
# It can be used within Jinja2 templates to apply consistent colors, fonts, and spacing.
# Example in HTML: <body style="background-color: {{ theme.bg_color }};">
# Or in a <style> block: .my-class { border-radius: {{ theme.border_radius }}; }
ui_theme = {
    'font_family': "'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    'bg_color': '#f8f9fa',
    'card_bg_color': '#ffffff',
    'primary_color': '#0d6efd',
    'secondary_color': '#6c757d',
    'success_color': '#198754',
    'danger_color': '#dc3545',
    'text_color_dark': '#212529',
    'text_color_light': '#f8f9fa',
    'border_color': '#dee2e6',
    'shadow': '0 0.5rem 1rem rgba(0, 0, 0, 0.15)',
    'border_radius': '0.5rem',
    'padding_md': '1.5rem',
    'padding_sm': '1rem',
}

# Sample product data (in a real app, this would come from a database)
products = {
    1: {'name': 'Modern Laptop', 'price': 1200.00, 'description': 'A high-performance laptop for all your needs.', 'image': 'laptop.jpg'},
    2: {'name': 'Wireless Headphones', 'price': 150.00, 'description': 'Noise-cancelling headphones with superior sound quality.', 'image': 'headphones.jpg'},
    3: {'name': 'Smart Watch', 'price': 250.00, 'description': 'Track your fitness and stay connected on the go.', 'image': 'watch.jpg'},
    4: {'name': 'Ergonomic Mouse', 'price': 75.00, 'description': 'A comfortable mouse designed for long hours of use.', 'image': 'mouse.jpg'},
    5: {'name': 'Mechanical Keyboard', 'price': 180.00, 'description': 'A tactile and responsive keyboard for typing enthusiasts.', 'image': 'keyboard.jpg'},
    6: {'name': '4K Monitor', 'price': 450.00, 'description': 'A stunning 27-inch 4K monitor with vibrant colors.', 'image': 'monitor.jpg'}
}

@app.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = {}

@app.route('/')
def index():
    return render_template('index.html', products=products, theme=ui_theme)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = products.get(product_id)
    if not product:
        return "Product not found", 404
    return render_template('product_detail.html', product=product, product_id=product_id, theme=ui_theme)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product_id_str = str(product_id)
    if product_id not in products:
        flash('Invalid product!', 'danger')
        return redirect(url_for('index'))

    cart = session['cart']
    quantity = int(request.form.get('quantity', 1))

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += quantity
    else:
        cart[product_id_str] = {
            'name': products[product_id]['name'],
            'price': products[product_id]['price'],
            'quantity': quantity
        }
    
    session.modified = True
    flash(f'{products[product_id]["name"]} has been added to your cart.', 'success')
    return redirect(request.referrer or url_for('index'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    total_price = 0
    for item in cart.values():
        total_price += item['price'] * item['quantity']
    return render_template('cart.html', cart=cart, total_price=total_price, theme=ui_theme)

@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    product_id_str = str(product_id)
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity'))

    if product_id_str in cart:
        if quantity > 0:
            cart[product_id_str]['quantity'] = quantity
            flash('Cart updated.', 'success')
        else:
            del cart[product_id_str]
            flash('Item removed from cart.', 'info')
    
    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    product_id_str = str(product_id)
    cart = session.get('cart', {})

    if product_id_str in cart:
        del cart[product_id_str]
        flash('Item removed from cart.', 'info')

    session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty. Cannot proceed to checkout.', 'warning')
        return redirect(url_for('index'))
    return render_template('checkout.html', theme=ui_theme)

@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    # Here you would typically process the payment, save the order, etc.
    # For this example, we'll just clear the cart.
    session['cart'] = {}
    session.modified = True
    flash('Thank you for your order! It has been placed successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
