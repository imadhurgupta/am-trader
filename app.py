from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import get_db, init_db

app = Flask(__name__)
app.secret_key = 'am_trader_secret_key_2024'

# Initialize DB on startup
with app.app_context():
    init_db()


# ─── Home ────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    db = get_db()
    bestsellers = db.execute(
        "SELECT * FROM products WHERE is_bestseller = 1 LIMIT 6"
    ).fetchall()
    db.close()
    return render_template('index.html', bestsellers=bestsellers)


# ─── Products ────────────────────────────────────────────────────────────────

@app.route('/products')
def products():
    category = request.args.get('category', 'all')
    db = get_db()
    if category == 'tea':
        products_list = db.execute(
            "SELECT * FROM products WHERE category = 'Tea' ORDER BY name"
        ).fetchall()
    elif category == 'spice':
        products_list = db.execute(
            "SELECT * FROM products WHERE category = 'Spice' ORDER BY name"
        ).fetchall()
    else:
        products_list = db.execute(
            "SELECT * FROM products ORDER BY category, name"
        ).fetchall()
    db.close()
    return render_template('products.html', products=products_list, active_filter=category)


# ─── About ───────────────────────────────────────────────────────────────────

@app.route('/about')
def about():
    return render_template('about.html')


# ─── Contact ─────────────────────────────────────────────────────────────────

@app.route('/contact')
def contact():
    return render_template('contact.html')


# ─── Submit Enquiry (POST) ────────────────────────────────────────────────────

@app.route('/submit-enquiry', methods=['POST'])
def submit_enquiry():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    product_interest = request.form.get('product_interest', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email:
        flash('Name and email are required.', 'error')
        return redirect(request.referrer or url_for('contact'))

    db = get_db()
    db.execute(
        "INSERT INTO enquiries (name, email, phone, product_interest, message) VALUES (?, ?, ?, ?, ?)",
        (name, email, phone, product_interest, message)
    )
    db.commit()
    db.close()

    flash('Thank you! Your enquiry has been received. We\'ll get back to you within 24 hours.', 'success')
    return redirect(request.referrer or url_for('contact'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
