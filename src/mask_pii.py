import re
import spacy
import argparse
from pathlib import Path

# Load English NLP pipeline (customize per language later)
nlp = spacy.load("en_core_web_sm")

# Regex patterns for PII
PATTERNS = {
    "EMAIL": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "PHONE": re.compile(r"\b(?:\+?\d{1,3})?[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "IP": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "DATE": re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"),
}

# NER labels to mask
ENTITY_LABELS = {"PERSON", "ORG", "GPE", "LOC", "DATE"}

def mask_text(text: str, lang: str = "en") -> str:
    # Regex masking
    for label, pattern in PATTERNS.items():
        text = pattern.sub(f"[{label}_REDACTED]", text)

    # NER masking
    doc = nlp(text)
    spans = [(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents if ent.label_ in ENTITY_LABELS]

    redacted = text
    offset = 0
    for start, end, label in spans:
        redacted = redacted[:start + offset] + f"[{label}_REDACTED]" + redacted[end + offset:]
        offset += len(f"[{label}_REDACTED]") - (end - start)

    return redacted

def main():
    parser = argparse.ArgumentParser(description="PII Masking Tool")
    parser.add_argument("--file", type=str, required=True, help="Path to input .txt file")
    parser.add_argument("--lang", type=str, default="en", help="Language code (default: en)")
    args = parser.parse_args()

    input_path = Path(args.file)
    if not input_path.exists():
        print(f"[!] File not found: {args.file}")
        return

    text = input_path.read_text(encoding="utf-8")
    masked = mask_text(text, args.lang)

    output_path = input_path.with_name(f"{input_path.stem}_masked.txt")
    output_path.write_text(masked, encoding="utf-8")
    print(f"[✓] Masked output saved to: {output_path}")

if __name__ == "__main__":
    main()
