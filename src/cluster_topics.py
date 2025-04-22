import json
import argparse
from pathlib import Path
from typing import List

from sentence_transformers import SentenceTransformer
import hdbscan

def load_tickets(filepath: Path) -> List[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_text_embeddings(tickets: List[dict], model_name="all-MiniLM-L6-v2") -> List:
    model = SentenceTransformer(model_name)
    texts = [f"{t['subject']} {t['body']}" for t in tickets]
    return model.encode(texts, convert_to_tensor=False), texts

def cluster_embeddings(embeddings, min_cluster_size=5):
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric="euclidean")
    cluster_labels = clusterer.fit_predict(embeddings)
    return cluster_labels

def assign_clusters(tickets: List[dict], cluster_labels: List[int]):
    for t, label in zip(tickets, cluster_labels):
        t["cluster_id"] = int(label) if label != -1 else -1
    return tickets

def save_output(tickets: List[dict], out_path: Path):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)
    print(f"[✓] Saved clustered output to: {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Cluster support tickets by semantic topic")
    parser.add_argument("--file", required=True, help="Path to anonymized .json file")
    args = parser.parse_args()

    in_path = Path(args.file)
    if not in_path.exists():
        print(f"[!] File not found: {in_path}")
        return

    tickets = load_tickets(in_path)
    embeddings, texts = get_text_embeddings(tickets)
    labels = cluster_embeddings(embeddings)
    clustered = assign_clusters(tickets, labels)

    out_path = in_path.with_name(f"{in_path.stem}_clustered.json")
    save_output(clustered, out_path)

    # Summary preview
    label_counts = {label: labels.tolist().count(label) for label in set(labels)}
    print(f"[📊] Cluster distribution: {label_counts}")

if __name__ == "__main__":
    main()
