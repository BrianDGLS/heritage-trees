import csv
from flask import Flask, abort, jsonify, request

app = Flask(__name__)

HERITAGE_TREES_CSV_FILEPATH = "./data/HeritageTreesOfIreland.csv"


def get_tree_data():
    data = []
    with open(HERITAGE_TREES_CSV_FILEPATH) as csvfile:
        for row in csv.DictReader(csvfile, delimiter="\t"):
            data.append(row)
    return data


def get_paginated_list(results, url, start, limit):
    # check if page exists
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < int(start):
        abort(404)
    # make response
    obj = {}
    obj["start"] = start
    obj["limit"] = limit
    obj["count"] = count
    # make URLs
    # make previous url
    if start == 1:
        obj["previous"] = ""
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj["previous"] = url + "?start=%d&limit=%d" % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj["next"] = ""
    else:
        start_copy = start + limit
        obj["next"] = url + "?start=%d&limit=%d" % (start_copy, limit)
    # finally extract result according to bounds
    obj["results"] = results[(start - 1) : (start - 1 + limit)]
    return obj


@app.route("/")
def trees():
    return jsonify(
        get_paginated_list(
            get_tree_data(),
            "/",
            start=request.args.get("start", 1),
            limit=request.args.get("limit", 20),
        )
    )
