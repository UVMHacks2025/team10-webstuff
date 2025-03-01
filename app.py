from flask import Flask, render_template
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

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/inventory')
def inventory():
    con = auth()
    cur = con.cursor()
    cur.execute('SELECT * FROM "INVENTORY"')
    inventory = cur.fetchall()
    con.close()
    return render_template('inventory.html', inventory=inventory)

if __name__ == "__main__":
    app.run(debug=True)