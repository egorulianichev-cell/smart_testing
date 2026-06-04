from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "OK", 200

@app.route("/feature"
def new_feature():
    return "New Feature", 200
           )
@app.route("/about")
def about():
    return "about", 200


@app.route("/health")
def health():
    return jsonify(status="healthy"), 200
