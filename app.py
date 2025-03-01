from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql
from connect import auth

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)