import argparse
from pathlib import Path
import subprocess

def run(cmd: str):
    print(f"\n[⚙️] {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[❌] Command failed: {cmd}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="End-to-end pipeline for ticket triage")
    parser.add_argument("--file", required=True, help="Path to .json or .csv input file")
    args = parser.parse_args()

    base = Path(args.file).stem
    folder = Path(args.file).parent

    # Step 1 – Anonymize
    anonymized = folder / f"{base}_anonymized.json"
    run(f"python src/anonymize_tickets.py --file {args.file}")

    # Step 2 – Cluster
    clustered = folder / f"{base}_anonymized_clustered.json"
    run(f"python src/cluster_topics.py --file {anonymized}")

    # Step 3 – Score
    scored = folder / f"{base}_anonymized_clustered_scored.json"
    run(f"python src/urgency_score.py --file {clustered}")

    print(f"\n[✅] Full pipeline complete.")
    print(f"[📊] Open with: streamlit run src/dashboard.py")
    print(f"[📂] Final output: {scored}")

if __name__ == "__main__":
    main()
