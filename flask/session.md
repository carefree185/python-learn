# flask session

flask中的session使用方式和django中的差不多。需要导入`session`然后直接添加值即可
```python
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = "*^817##61Ksjflkxkmks"  # 加密使用的key


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":

        return render_template("login.html")
    else:
        session["username"] = "123"  # 添加session

        return redirect("/home")


@app.route("/home")
def home():
    if session.get("username"):
        print(session.get("username"))  # 获取session值
        return render_template("home.html")
    return "请先登录"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
```