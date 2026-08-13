from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data" / "banking"
OUTPUT_DIR = ROOT_DIR / "outputs"
CHUNKS_PATH = OUTPUT_DIR / "chunks.json"
INDEX_PATH = OUTPUT_DIR / "index.json"

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "650"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
TOP_K = int(os.getenv("TOP_K", "5"))

OUTPUT_DIR.mkdir(exist_ok=True)
