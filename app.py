import pymongo
from bson import ObjectId
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("localhost:27017")
# client = MongoClient("내 mongodb url 주소")
db = client.bicycleTouringDB


@app.route("/")
def home():
    return render_template("index2.html")


@app.route("/attraction", methods=["POST"])
def save_attraction():
    attraction = request.form["attraction"]
    description = request.form["description"]

    doc = {
        "attraction": attraction,
        "description": description,
        "read": False,
    }
    db.attractions.insert_one(doc)
    return jsonify({"status": "saved"})


@app.route("/attractions", methods=["GET"])
def get_attractions():
    attractions = list(db.attractions.find({}, {}).sort("read", pymongo.ASCENDING))
    # 참고 : https://stackoverflow.com/questions/4291236/edit-the-values-in-a-list-of-dictionaries
    for attraction in attractions:
        attraction.update((k, str(v)) for k, v in attraction.items())
    return jsonify({"attractions": attractions})


@app.route("/attraction/read", methods=["POST"])
def mark_as_read():
    attraction_id = request.form["attractionId"]
    db.attractions.update_one({"_id": ObjectId(attraction_id)}, {"$set": {"read": True}})
    return jsonify({"status": "marked as read"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
