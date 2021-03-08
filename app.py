from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
# import request
import lockon


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index', methods = [ "GET", "POST"])
def index():
    form_data = request.form
    res = lockon.lockon(form_data["id"], form_data["password"])

    return render_template('index.html', data=res)

if __name__ == "__main__":
    # app.run()
    app.run(host='0.0.0.0')