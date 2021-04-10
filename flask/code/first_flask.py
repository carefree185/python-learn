from flask import Flask, send_file, jsonify  # Flask类
from flask import render_template  # 用于返回模板的函数
from flask import redirect

app = Flask(__name__)


@app.route("/")
def index():
    return "首页"


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/to_home")
def to_home():
    return redirect("/home")


@app.route("/get_file")
def get_file():
    return send_file("first_flask.py")


@app.route("/get_json")
def get_json():

    d = {
        "name": "杜宇鹏",
        "age": 25
    }
    return jsonify(d)


if __name__ == '__main__':
    app.run(debug=True)
