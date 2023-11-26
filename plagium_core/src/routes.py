from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, request, jsonify
from src.use_case.parse_code import parseCode
from src.use_case.compare_trees import compareTreesUseCase
from src.entities.file import File

bp = Blueprint("main_v1", __name__, url_prefix="/v1.1")

async def async_compare_trees(pair):
    return await compareTreesUseCase(pair[0].tree, pair[1].tree)

@bp.route("/process", methods=["POST"])
def process():
    # Parsea el código de cada archivo y calcula su hash
    files = []
    for file in request.files.values():
        code = file.read().decode("utf-8")
        files.append(File(file.filename, parseCode(code), hash(code)))

    files = list(set(files))

    pairs = [(files[i], files[j]) for i in range(len(files)) for j in range(i + 1, len(files))]

    # Create a ThreadPoolExecutor
    with ThreadPoolExecutor(4) as executor:
        # Use the executor to run compareTreesUseCase for each pair in pairs
        similarities = list(executor.map(lambda p: compareTreesUseCase(p[0].tree, p[1].tree), pairs))

    # Prepara y devuelve el informe de similitudes
    report = [
        {
            "file1": pair[0].name,
            "file2": pair[1].name,
            "similarity": similarity
        }
        for pair, similarity in zip(pairs, similarities)
    ]

    return jsonify({"report": report})
