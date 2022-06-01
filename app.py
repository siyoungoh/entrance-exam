from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("localhost:27017")
# client = MongoClient("내 mongodb url 주소")
db = client.bicycleTouringDB


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/attraction", methods=["POST"])
def save_attraction():
    attraction = request.form["attraction"]
    description = request.form["description"]

    doc = {
        "attraction": attraction,
        "description": description,
    }
    db.attractions.insert_one(doc)
    return jsonify({"status": "saved"})


@app.route("/attractions", methods=["GET"])
def get_attractions():
    attractions = list(db.attractions.find({}, {"_id": False}))
    return jsonify({"attractions": attractions})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
