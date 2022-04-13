import csv
from flask import Flask, jsonify, request

from app.pagination import Paginate

app = Flask(__name__)

HERITAGE_TREES_CSV_FILEPATH = "./data/HeritageTreesOfIreland.csv"


def get_tree_data():
    data = []
    with open(HERITAGE_TREES_CSV_FILEPATH) as csvfile:
        for row in csv.DictReader(csvfile, delimiter="\t"):
            data.append(row)
    return data


@app.route("/")
def trees():
    results = get_tree_data()
    start = int(request.args.get("start", 1))
    limit = int(request.args.get("limit", 20))
    paginated_results = Paginate(results, request.base_url, limit)
    return jsonify(paginated_results.get_results(start))
