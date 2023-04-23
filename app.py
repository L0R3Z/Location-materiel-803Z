from flask import Flask,request,render_template,jsonify,abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

print("hello world!")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
