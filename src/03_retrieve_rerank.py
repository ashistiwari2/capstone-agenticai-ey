import json
import math
import re
import sys
from collections import Counter
from config import INDEX_PATH, TOP_K

TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")

def tokenize(text: str):
    return [t.lower() for t in TOKEN_RE.findall(text)]

def dot(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(value * b.get(term, 0.0) for term, value in a.items())

def query_vector(tokens, idf):
    tf = Counter(tokens)
    vec = {term: count * idf.get(term, 0.0) for term, count in tf.items() if term in idf}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return {term: value / norm for term, value in vec.items()}

def bm25_score(tokens, doc_terms, idf, avgdl, k1=1.5, b=0.75):
    score = 0.0
    tf = doc_terms["tf"]
    dl = doc_terms["length"]
    for token in tokens:
        if token not in tf:
            continue
        freq = tf[token]
        denom = freq + k1 * (1 - b + b * dl / max(avgdl, 1))
        score += idf.get(token, 0.0) * (freq * (k1 + 1)) / denom
    return score

def ranks_from_scores(scores):
    return {idx: rank + 1 for rank, (idx, _) in enumerate(sorted(scores.items(), key=lambda x: x[1], reverse=True))}

def retrieve(query: str, top_k: int = TOP_K):
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    tokens = tokenize(query)
    qv = query_vector(tokens, index["idf"])

    vector_scores = {i: dot(qv, vec) for i, vec in enumerate(index["vectors"])}
    bm25_scores = {i: bm25_score(tokens, terms, index["idf"], index["avgdl"]) for i, terms in enumerate(index["bm25_terms"])}

    vranks = ranks_from_scores(vector_scores)
    branks = ranks_from_scores(bm25_scores)
    fused = {}
    for i in range(len(index["chunks"])):
        fused[i] = 1 / (60 + vranks.get(i, 999)) + 1 / (60 + branks.get(i, 999))

    results = []
    for i, score in sorted(fused.items(), key=lambda x: x[1], reverse=True)[:top_k]:
        chunk = index["chunks"][i]
        results.append({
            "rank": len(results) + 1,
            "score": round(score, 6),
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "text": chunk["text"],
            "vector_score": round(vector_scores[i], 6),
            "bm25_score": round(bm25_scores[i], 6),
        })
    return results

def main():
    query = " ".join(sys.argv[1:]) or "What documents are needed for a home loan?"
    for result in retrieve(query):
        print(f"#{result['rank']} {result['chunk_id']} score={result['score']}")
        print(result["text"][:350] + "\n")

if __name__ == "__main__":
    main()
