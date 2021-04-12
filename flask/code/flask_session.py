from flask import Flask, render_template, request, session, redirect
from functools import wraps

app = Flask(__name__)
app.secret_key = "*^817##61Ksjflkxkmks"  # 加密使用的key


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":

        return render_template("login.html")
    else:
        session["username"] = "123"  # 添加session

        return redirect("/home")


# 登录认证装饰器
def login_decorator(func):
    @wraps(func)  # inner.__name__ = func.__name__
    def inner(*args, **kwargs):
        if session.get("username"):
            ret = func(*args, **kwargs)
            return ret
        else:
            return "请先登录"

    # inner.__name__ = func.__name__
    return inner


@app.route("/home")
@login_decorator
def home():
    return render_template("home.html")


@app.route("/index/<int:age>", defaults={"name": "dyp"})
@login_decorator
def index(name, age):
    return f"index {name}:{age}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


