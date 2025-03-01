from flask import Flask, render_template
import psycopg2
from psycopg2 import sql
from connect import auth

app = Flask(__name__)

@app.route('/')
def index():
    con = auth()
    
    cur = con.cursor()

    cur.execute('SELECT * FROM "INVENTORY"')
    inventory = cur.fetchall()
    for i in inventory:
        print(i[4])
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/insert')
def insert():
    return render_template('insert.html')

if __name__ == "__main__":
    app.run(debug=True)
    