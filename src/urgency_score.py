import argparse
import json
import re
from pathlib import Path
from transformers import pipeline

# Loads the sentiment model locally (can be overridden)
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Business rules: trigger words by theme
KEYWORDS = {
    "high": ["urgent", "immediately", "asap", "not working", "security", "blocked", "crash", "error", "hacked"],
    "medium": ["refund", "delay", "issue", "problem", "unavailable", "login", "password"],
    "low": ["question", "how", "help", "support", "info", "change"]
}

def rule_based_score(text: str) -> float:
    score = 0
    text_lower = text.lower()
    for word in KEYWORDS["high"]:
        if re.search(rf"\b{word}\b", text_lower):
            score += 1.0
    for word in KEYWORDS["medium"]:
        if re.search(rf"\b{word}\b", text_lower):
            score += 0.5
    for word in KEYWORDS["low"]:
        if re.search(rf"\b{word}\b", text_lower):
            score += 0.2
    return min(score / 3.0, 1.0)  # Normalisé

def hybrid_urgency_score(ticket: dict) -> dict:
    full_text = f"{ticket['subject']} {ticket['body']}"
    
    # Sentiment analysis
    sentiment = sentiment_model(full_text[:512])[0]
    sentiment_score = 1.0 if sentiment["label"] == "NEGATIVE" else 0.0

    # Score by keywords
    rules_score = rule_based_score(full_text)

    # Hybrid weighting: 70% rules, 30% tone
    final_score = round((rules_score * 0.7 + sentiment_score * 0.3), 3)

    ticket["urgency_score"] = final_score
    ticket["urgency_reason"] = {
        "sentiment": sentiment["label"],
        "confidence": sentiment["score"],
        "rules_score": rules_score
    }
    return ticket

def main():
    parser = argparse.ArgumentParser(description="Urgency scoring tool for support tickets")
    parser.add_argument("--file", required=True, help="Path to clustered ticket .json")
    args = parser.parse_args()

    in_path = Path(args.file)
    if not in_path.exists():
        print(f"[!] File not found: {in_path}")
        return

    with open(in_path, "r", encoding="utf-8") as f:
        tickets = json.load(f)

    scored = [hybrid_urgency_score(t) for t in tickets]

    out_path = in_path.with_name(f"{in_path.stem}_scored.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(scored, f, indent=2, ensure_ascii=False)

    print(f"[✓] Scored tickets saved to: {out_path}")
    print("\n[🔥] Sample scores:")
    for t in scored[:3]:
        print(f"  {t['ticket_id']} → urgency_score={t['urgency_score']} ({t['urgency_reason']['sentiment']})")

if __name__ == "__main__":
    main()
