import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"
INDEX_DIR = "faiss_index"

os.makedirs(INDEX_DIR, exist_ok=True)

# Load embedding model (FAST)
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
filenames = []

for file in os.listdir(DATA_DIR):
    if file.endswith(".txt"):
        path = os.path.join(DATA_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            texts.append(f.read())
            filenames.append(file)

# Create embeddings
embeddings = model.encode(texts, show_progress_bar=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index + metadata
faiss.write_index(index, os.path.join(INDEX_DIR, "index.faiss"))
with open(os.path.join(INDEX_DIR, "metadata.pkl"), "wb") as f:
    pickle.dump(filenames, f)

print("✅ FAISS index built using SentenceTransformers!")
