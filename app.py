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
    return render_template("index3.html")


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
    pipelines = [{'$project': {'attractionId': {"$toString": "$_id"}, 'attraction': "$attraction",
                               "description": "$description", "read": "$read", '_id': False}},
                 {"$sort": {"read": pymongo.ASCENDING}}]
    attractions = list(db.attractions.aggregate(pipelines))
    # 참고 문서
    # https://pymongo.readthedocs.io/en/stable/examples/aggregation.html
    # https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/
    # https://www.mongodb.com/docs/manual/reference/operator/aggregation/toString/#definition
    # https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/#definition

    return jsonify({"attractions": attractions})


@app.route("/attraction/read", methods=["POST"])
def mark_as_read():
    attraction_id = request.form["attractionId"]
    db.attractions.update_one({"_id": ObjectId(attraction_id)}, {"$set": {"read": True}})
    return jsonify({"status": "marked as read"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
