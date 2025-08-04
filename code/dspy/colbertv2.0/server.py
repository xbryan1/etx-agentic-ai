from flask import Flask, render_template, request
from functools import lru_cache
import math
import os
from dotenv import load_dotenv
from rich import print

INDEX_NAME = os.getenv("INDEX_NAME")
INDEX_ROOT = os.getenv("INDEX_ROOT")

print("Importing RAGPretrainedModel from ragatouille (this might take a while)...")
from ragatouille import RAGPretrainedModel
print("RAGPretrainedModel imported successfully.")

app = Flask(__name__)

counter = {"api" : 0}

def init_engine():
    print("Initializing the engine...")
    index_path = os.path.join(INDEX_ROOT, INDEX_NAME)
    engine = RAGPretrainedModel.from_index(index_path)
    print("Engine initialized successfully.")
    return engine

engine = init_engine()

@lru_cache(maxsize=1000000)
def api_search_query(query, k):
    print(f"Query={query}")
    if k == None: k = 10
    k = min(int(k), 100)
    results = engine.search(query, k=k)
    topk = []
    for r in results:
        d = {'text': r['content'], 'pid': r['passage_id'], 'rank': r['rank'], 'score': r['score'], 'prob': 1}
        topk.append(d)
    topk = list(sorted(topk, key=lambda p: (-1 * p['score'], p['pid'])))
    return {"query" : query, "topk": topk}

@app.route("/api/search", methods=["GET"])
def api_search():
    if request.method == "GET":
        counter["api"] += 1
        print("API request count:", counter["api"])
        return api_search_query(request.args.get("query"), request.args.get("k"))
    else:
        return ('', 405)

if __name__ == "__main__":
    app.run("0.0.0.0", int(os.getenv("PORT")))

