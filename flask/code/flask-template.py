from flask import Flask, render_template

app = Flask(__name__)


@app.template_global()  # 全局调用
def add(a, b):
    return a+b


@app.route("/index")
def index():
    my_str = 'Hello Word'
    my_int = 10
    my_array = [3, 4, 2, 1, 7, 9]
    my_dict = {
        'name': 'xiaoming',
        'age': 18
    }
    return render_template('template.html', **locals())


if __name__ == '__main__':
    app.run()
