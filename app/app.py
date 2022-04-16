import csv
from flask import Flask, jsonify, request, abort

from app.pagination import Paginate

app = Flask(__name__)

HERITAGE_TREES_CSV_FILEPATH = "./data/HeritageTreesOfIreland.csv"


def get_tree_data():
    with open(HERITAGE_TREES_CSV_FILEPATH) as csvfile:
        return [row for row in csv.DictReader(csvfile, delimiter="\t")]


@app.route("/")
def trees():
    results = get_tree_data()
    start = int(request.args.get("start", 1))
    limit = int(request.args.get("limit", 20))
    paginated_results = Paginate(results, request.base_url, limit)
    return jsonify(paginated_results.get_results(start))


@app.route("/<record_key>")
def tree(record_key):
    results = get_tree_data()
    try:
        [tree] = [tree for tree in results if tree["RecordKey"] == record_key]
        return jsonify(tree)
    except:
        abort(404)
