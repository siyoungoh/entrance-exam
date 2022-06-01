import pymongo
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

    attractions_list = list(db.attractions.find({}, {'_id': False}))
    previous_id = len(attractions_list)
    if previous_id > 0:
        attraction_id = previous_id + 1
    else:
        attraction_id = 1

    doc = {
        "attractionId": attraction_id,
        "attraction": attraction,
        "description": description,
        "read": False,
    }
    db.attractions.insert_one(doc)
    return jsonify({"status": "saved"})


@app.route("/attractions", methods=["GET"])
def get_attractions():
    attractions = list(db.attractions.find({}, {"_id": False}).sort("read", pymongo.ASCENDING))
    # 참고 문서
    # https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html#pymongo.cursor.Cursor.sort
    # https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.ASCENDING
    return jsonify({"attractions": attractions})


@app.route("/attraction/read", methods=["POST"])
def mark_as_read():
    attraction_id = request.form["attractionId"]
    db.attractions.update_one({"attractionId": int(attraction_id)}, {"$set": {"read": True}})
    return jsonify({"status": "marked as read"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
