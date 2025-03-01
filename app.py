from flask import Flask, render_template, request, redirect, url_for, flash, session
import psycopg2
from psycopg2 import sql
from connect import auth

app = Flask(__name__)

app.secret_key = 's3cr3t_k3y_12345'

# Mapping for food types
food_type_mapping = {
    'canned': 1,
    'dairy': 2,
    'produce': 3,
    'meat': 4,
    'grains': 5,
    'other': 6,
    'household_product': 7,
    'snacks': 8
}

# Mapping for dietary restrictions
dietary_restriction_mapping = {
    'vegan': 1,
    'vegetarian': 2,
    'hallal': 3,
    'kosher': 4,
    'gluten-free': 5,
    'nut-free': 6,
    'dairy-free': 7,
    'none': 8
}

# Mapping for perishable status
perishable_mapping = {
    'perishable': 1,
    'nonperishable': 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']
        food_type_key = food_type_mapping.get(request.form['type'].lower(), 6)  # Default to 'other' if not found
        restriction_key = dietary_restriction_mapping.get(request.form['dietary_restriction'].lower(), 8)  # Default to 'none' if not found
        is_perishable = perishable_mapping.get(request.form['perishable'].lower(), 0)  # Default to 'nonperishable' if not found
        location = request.form['location']

        con = auth()
        cur = con.cursor()
        
        # Get the next container_id
        cur.execute('SELECT COALESCE(MAX(container_id), 0) + 1 FROM "INVENTORY"')
        container_id = cur.fetchone()[0]

        cur.execute(
            'INSERT INTO "INVENTORY" (container_id, food_name, quantity, expiration_date, food_type_key, restriction_key, is_perishable, location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (container_id, name, quantity, expiration_date, food_type_key, restriction_key, is_perishable, location)
        )
        con.commit()
        con.close()
        return redirect(url_for('inventory'))
    return render_template('insert.html')

@app.route('/inventory')
def inventory():
    con = auth()
    cur = con.cursor()
    cur.execute('SELECT container_id, quantity, entry_date, expiration_date, food_name, food_type_key, restriction_key, is_active, is_perishable, location FROM "INVENTORY"')
    inventory = cur.fetchall()
    con.close()
    return render_template('inventory.html', inventory=inventory)

@app.route('/user', methods=['POST'])
def register():
    # Get form data
    user = 10
    firstName = request.form.get('first-name')
    lastName = request.form.get('last-name')
    email = request.form.get('email')
    password = request.form.get('psw')
    password_repeat = request.form.get('psw-repeat')
    role = request.form.get('role')

    # Form validation
    if not email or not password or password != password_repeat:
        flash('Please fill in all fields and ensure passwords match!')
        return redirect(url_for('user'))

  
    conn = auth()
    if conn is None:
        flash("Database connection failed")
        return redirect(url_for('user'))
    
    cursor = conn.cursor()

    # Insert query (without user_id if it's auto-incrementing)
    cursor.execute('INSERT INTO "USER" (user_id, first_name, last_name, email, password, role) VALUES (%s,%s, %s, %s, %s, %s)', 
                    (user,firstName, lastName, email, password, role))
    conn.commit()  # Commit the transaction

    flash('Registration successful!')
    return redirect(url_for('user'))

# Login route
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('uname')  # Username input field
    password = request.form.get('psw')  # Password input field

    conn = auth()
    if conn is None:
        flash("Database connection failed")
        return redirect(url_for('index'))

    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT * FROM "USER" WHERE email = %s AND password = %s', (email, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session['user'] = email  # Store user session
        flash('Login successful!')
        return redirect(url_for('inventory'))  # Redirect to the next page

    else:
        flash('Invalid email or password!')
        return redirect(url_for('user'))  # Redirect back to login




if __name__ == "__main__":
    app.run(debug=True)