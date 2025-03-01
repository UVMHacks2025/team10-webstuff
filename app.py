from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True)