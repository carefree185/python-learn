import os

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        print(request.url)  # 完整的url
        print(request.url_root)  # 请求地址，host
        print(request.url_rule)  # 路由
        print(request.url_charset)  # url的编码
        print(request.values)  # 包含了get和post两种请求方式提交的数据
        print(request.args)
        print(request.args.to_dict())
        return render_template("login.html")
    else:
        print(request.form)  # form表单提交的参数，FormData数据。post提交的数据
        print(request.form.to_dict())  # 转为字典
        print(request.files.to_dict())
        # 上传并保存文件
        file = request.files.get("file")
        path = os.path.join("xht", file.filename)
        file.save(path)

        return "200 ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)


