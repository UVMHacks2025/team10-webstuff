from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import sql
from connect import auth

app = Flask(__name__)

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
        food_type_key = request.form['type']
        restriction_key = request.form['dietary_restriction']
        is_perishable = request.form['perishable']
        location = request.form['location']

        con = auth()
        cur = con.cursor()
        cur.execute(
            'INSERT INTO "INVENTORY" (food_name, quantity, expiration_date, food_type_key, restriction_key, is_perishable, location) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (name, quantity, expiration_date, food_type_key, restriction_key, is_perishable, location)
        )
        con.commit()
        con.close()
        return redirect(url_for('inventory'))
    return render_template('insert.html')

@app.route('/inventory')
def inventory():
    con = auth()
    cur = con.cursor()
    cur.execute('SELECT container_id, quantity, entry_date, expiration_date, food_name, food_type_key, restriction_key, is_active, is_perishable, location FROM "INVENTORY" WHERE is_active = 1')
    inventory = cur.fetchall()
    con.close()
    return render_template('inventory.html', inventory=inventory)

if __name__ == "__main__":
    app.run(debug=True)