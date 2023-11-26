from flask import Blueprint, request, jsonify, current_app
from src.use_case.parse_code import parseCode
from src.use_case.compare_trees import compareTrees

import asyncio as aio

bp = Blueprint("main_v1", __name__, url_prefix="/v1.1")

# Route /process that recieves a list of files and returns a processed information
@bp.route("/process", methods=["POST"])
def process():
    # Get the files from the request file storage
    files = [(f.filename, parseCode(f.read().decode("utf-8"))) for f in request.files.values()]

    # Get unique pairs of files and parallelize the comparison to compare the trees of each pair
    # The result is a list of tuples with the similarity of each pair
    pairs = [(files[i], files[j]) for i in range(len(files)) for j in range(i + 1, len(files))]
    similarities = [compareTrees(p[0][1], p[1][1]) for p in pairs]

    # Return a report with the similarities
    return jsonify({
        "report": [
            {
                "file1": files[i][0],
                "file2": files[j][0],
                "similarity": similarities[i * (len(files) - i - 1) + j - i - 1]
            }
            for i in range(len(files)) for j in range(i + 1, len(files))
        ]
    })
