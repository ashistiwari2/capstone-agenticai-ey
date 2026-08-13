import json
import re
from config import DATA_DIR, CHUNKS_PATH, CHUNK_SIZE, CHUNK_OVERLAP
from utils.pii_filter import redact_pii

def clean_text(text: str) -> str:
    text = redact_pii(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text: str, chunk_size: int, overlap: int):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks

def main():
    records = []
    for path in sorted(DATA_DIR.glob("*.txt")):
        text = clean_text(path.read_text(encoding="utf-8"))
        for idx, chunk in enumerate(chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP), start=1):
            records.append({
                "chunk_id": f"{path.name}#chunk-{idx}",
                "source": path.name,
                "chunk_number": idx,
                "text": chunk,
            })
    CHUNKS_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")
    print(f"Wrote {len(records)} chunks to {CHUNKS_PATH}")

if __name__ == "__main__":
    main()
