import json
import argparse
from pathlib import Path
from typing import List
from collections import Counter, defaultdict

from sentence_transformers import SentenceTransformer
import hdbscan
import spacy

nlp = spacy.load("en_core_web_sm")

def load_tickets(filepath: Path) -> List[dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_text_embeddings(tickets: List[dict], model_name="all-MiniLM-L6-v2") -> List:
    model = SentenceTransformer(model_name)
    texts = [f"{t['subject']} {t['body']}" for t in tickets]
    embeddings = model.encode(texts, convert_to_tensor=False)
    return embeddings, texts

def cluster_embeddings(embeddings, min_cluster_size=2):
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric="euclidean")
    cluster_labels = clusterer.fit_predict(embeddings)
    return cluster_labels

def assign_clusters(tickets: List[dict], cluster_labels: List[int]):
    for t, label in zip(tickets, cluster_labels):
        t["cluster_id"] = int(label) if label != -1 else -1
    return tickets

def extract_keywords_by_cluster(tickets, top_n=5):
    cluster_texts = defaultdict(list)
    for t in tickets:
        if t["cluster_id"] != -1:
            cluster_texts[t["cluster_id"]].append(f"{t['subject']} {t['body']}")

    cluster_keywords = {}
    for cluster_id, texts in cluster_texts.items():
        joined_text = " ".join(texts).lower()
        doc = nlp(joined_text)

        words = [
            token.lemma_
            for token in doc
            if token.is_alpha and not token.is_stop and len(token) > 2
        ]
        top_words = [w for w, _ in Counter(words).most_common(top_n)]
        cluster_keywords[cluster_id] = top_words

    return cluster_keywords

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

    label_counts = {label: labels.tolist().count(label) for label in set(labels)}
    print(f"\n[📊] Cluster distribution: {label_counts}")

    keywords = extract_keywords_by_cluster(clustered)
    print(f"\n[🔎] Cluster keywords:")
    for cid, words in keywords.items():
        print(f"  Cluster {cid}: {', '.join(words)}")

if __name__ == "__main__":
    main()
