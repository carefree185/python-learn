from flask import Flask
from time import sleep

app = Flask(__name__)


@app.route('/index')
def index():
    sleep(2)
    return 'hello'


@app.route('/index1')
def index1():
    sleep(2)
    return 'hello1'


if __name__ == '__main__':
    app.run()
