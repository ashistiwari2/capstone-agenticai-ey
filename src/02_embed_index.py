import json
import math
import re
from collections import Counter, defaultdict
from config import CHUNKS_PATH, INDEX_PATH

TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")

def tokenize(text: str):
    return [t.lower() for t in TOKEN_RE.findall(text)]

def build_index(chunks):
    docs = [tokenize(c["text"]) for c in chunks]
    doc_count = len(docs)
    df = defaultdict(int)
    for tokens in docs:
        for token in set(tokens):
            df[token] += 1
    idf = {token: math.log((doc_count + 1) / (freq + 0.5)) + 1 for token, freq in df.items()}
    avgdl = sum(len(d) for d in docs) / max(doc_count, 1)
    vectors = []
    bm25_terms = []
    for tokens in docs:
        tf = Counter(tokens)
        length = len(tokens)
        vec = {term: count * idf.get(term, 0.0) for term, count in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vec = {term: value / norm for term, value in vec.items()}
        vectors.append(vec)
        bm25_terms.append({"tf": dict(tf), "length": length})
    return {
        "chunks": chunks,
        "idf": idf,
        "avgdl": avgdl,
        "vectors": vectors,
        "bm25_terms": bm25_terms,
    }

def main():
    chunks = json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))
    index = build_index(chunks)
    INDEX_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(f"Wrote index for {len(chunks)} chunks to {INDEX_PATH}")

if __name__ == "__main__":
    main()
