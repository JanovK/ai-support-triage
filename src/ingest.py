import json
import csv
import argparse
from pathlib import Path
from typing import List, Dict
from langdetect import detect

REQUIRED_FIELDS = {"ticket_id", "subject", "body"}

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except:
        return "unknown"

def normalize_ticket(ticket: dict) -> dict:
    # Ensure required fields
    for field in REQUIRED_FIELDS:
        ticket.setdefault(field, "")
    # Fallbacks
    ticket["lang"] = ticket.get("lang") or detect_language(ticket["body"])
    ticket["channel"] = ticket.get("channel", "unknown")
    ticket["timestamp"] = ticket.get("timestamp", "1970-01-01")
    return ticket

def load_json(filepath: Path) -> List[Dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [normalize_ticket(t) for t in data]

def load_csv(filepath: Path) -> List[Dict]:
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [normalize_ticket(row) for row in reader]

def main():
    parser = argparse.ArgumentParser(description="Ticket ingestion tool")
    parser.add_argument("--file", type=str, required=True, help="Path to input .json or .csv")
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"[!] File not found: {filepath}")
        return

    ext = filepath.suffix.lower()
    if ext == ".json":
        tickets = load_json(filepath)
    elif ext == ".csv":
        tickets = load_csv(filepath)
    else:
        print("[!] Unsupported file type. Use .json or .csv")
        return

    print(f"[✓] Loaded {len(tickets)} tickets.")
    print(json.dumps(tickets[:2], indent=2, ensure_ascii=False))  # Preview 2 tickets

if __name__ == "__main__":
    main()
