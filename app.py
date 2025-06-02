from flask import Flask,render_template,request,redirect,url_for,flash,session,jsonify
import sqlite3
import hashlib
import logging
import razorpay

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Razorpay client setup
razorpay_client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY", "YOUR_SECRET_KEY"))

def get_db_connection():
    conn = sqlite3.connect('shopmix.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))
        conn.commit()
        conn.close()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = request.json['product_id']
        logging.info(f"Product added to cart: {product_id}")
        return jsonify({'status': 'success'})
    return render_template('cart.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/faq')
def faq():  
    return render_template('faq.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/about')    
def about():
    return render_template('about.html')
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')
@app.route('/order_summary')
def order_summary():
    return render_template('order_summary.html')
@app.route('/order_success')
def order_success():
    return render_template('order_success.html')
@app.route('/order_failed')
def order_failed():
    return render_template('order_failed.html')
@app.route('/profile')
def profile():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)
@app.route('/update_profile', methods=['POST'])

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    amount = data.get('amount') * 100  # in paise
    payment = razorpay_client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": '1'
    })
    return jsonify(payment)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
