# Util
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    with open('requirements.txt', 'r') as file:
        return file.read()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
