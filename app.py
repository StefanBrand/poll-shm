# Util
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<a href="static/endtimestamps.csv">Download <code>endtimestamps.csv</code></a>'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
