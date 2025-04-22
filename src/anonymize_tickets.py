import argparse
import json
import csv
from pathlib import Path
from ingest import load_json, load_csv
from mask_pii import mask_text

def anonymize_ticket(ticket: dict) -> dict:
    ticket["subject"] = mask_text(ticket["subject"], lang=ticket.get("lang", "en"))
    ticket["body"] = mask_text(ticket["body"], lang=ticket.get("lang", "en"))
    return ticket

def save_json(tickets, out_path: Path):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)

def save_csv(tickets, out_path: Path):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tickets[0].keys())
        writer.writeheader()
        writer.writerows(tickets)

def main():
    parser = argparse.ArgumentParser(description="Batch anonymizer for support tickets")
    parser.add_argument("--file", required=True, help="Path to .json or .csv file")
    args = parser.parse_args()

    in_path = Path(args.file)
    if not in_path.exists():
        print(f"[!] File not found: {in_path}")
        return

    ext = in_path.suffix.lower()
    if ext == ".json":
        tickets = load_json(in_path)
    elif ext == ".csv":
        tickets = load_csv(in_path)
    else:
        print("[!] Unsupported file type. Use .json or .csv")
        return

    anonymized = [anonymize_ticket(t) for t in tickets]

    out_path = in_path.with_name(f"{in_path.stem}_anonymized{in_path.suffix}")
    if ext == ".json":
        save_json(anonymized, out_path)
    else:
        save_csv(anonymized, out_path)

    print(f"[✓] Saved anonymized file to: {out_path}")
    print(json.dumps(anonymized[:1], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
