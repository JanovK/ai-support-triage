import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer
import hdbscan
import numpy as np
import json

# 1. Load all tickets (anonymized) from disk
DATA_PATH = Path("data/all_tickets_anonymized.json")
CACHE_DIR = Path("cache")
MODEL_NAME = "all-MiniLM-L6-v2"

def load_tickets():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_centroids(clusterer, embeddings):
    labels = clusterer.labels_
    centroids = []
    for cid in set(labels):
        if cid == -1: continue
        points = embeddings[labels == cid]
        centroids.append(points.mean(axis=0))
    return np.vstack(centroids), [cid for cid in set(labels) if cid != -1]

def main():
    tickets = load_tickets()
    texts = [t["subject"] + " " + t["body"] for t in tickets]

    # 2. Compute embeddings
    model = SentenceTransformer(MODEL_NAME)
    embeddings = np.array(model.encode(texts, convert_to_tensor=False))

    # 3. Run HDBSCAN
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, metric="euclidean")
    clusterer.fit(embeddings)

    # 4. Build centroids & id mapping
    centroids, cluster_ids = compute_centroids(clusterer, embeddings)

    # 5. Cache the clusterer, centroids, and id list
    CACHE_DIR.mkdir(exist_ok=True)
    with open(CACHE_DIR / "cluster_cache.pkl", "wb") as f:
        pickle.dump({
            "centroids": centroids,
            "cluster_ids": cluster_ids
        }, f)

    print(f"[✓] Cached {len(cluster_ids)} clusters to {CACHE_DIR/'cluster_cache.pkl'}")

if __name__ == "__main__":
    main()