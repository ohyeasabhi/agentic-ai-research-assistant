import faiss
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Files
INDEX_FILE = Path("semantic_index.faiss")
DATA_FILE = Path("semantic_data.json")

# Model (small & fast)
model = SentenceTransformer("all-MiniLM-L6-v2")


def _load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def _save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


def _load_index(dim):
    if INDEX_FILE.exists():
        return faiss.read_index(str(INDEX_FILE))
    return faiss.IndexFlatL2(dim)


def add_to_memory(text: str):
    embedding = model.encode([text])
    dim = embedding.shape[1]

    index = _load_index(dim)
    data = _load_data()

    index.add(embedding)
    data.append(text)

    faiss.write_index(index, str(INDEX_FILE))
    _save_data(data)


def search_memory(query: str, k: int = 3):
    if not INDEX_FILE.exists():
        return []

    data = _load_data()
    index = faiss.read_index(str(INDEX_FILE))

    query_vec = model.encode([query])
    _, indices = index.search(query_vec, k)

    return [data[i] for i in indices[0] if i < len(data)]
