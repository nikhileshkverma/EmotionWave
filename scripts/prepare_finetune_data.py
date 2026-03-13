#!/usr/bin/env python3
"""
prepare_finetune_data.py

Convert raw split files into chat-based JSONL for fine-tuning GPT chat models.
Each line will have a "messages" array with system, user, and assistant roles.
Usage:
    python scripts/prepare_finetune_data.py
Outputs:
    data/processed/train_prepared.jsonl
    data/processed/val_prepared.jsonl
"""
import json
from pathlib import Path

# Define your system prompt guiding the model
SYSTEM_PROMPT = """
You are an emotion classifier. Respond with a JSON array of emotions from
[anger, annoyance, approval, caring, confusion, curiosity, desire,
disappointment, disapproval, disgust, embarrassment, excitement, fear,
gratitude, grief, joy, love, nervousness, optimism, pride, realization,
relief, remorse, sadness, surprise, neutral].
"""

def prepare(input_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open('r') as fin, output_path.open('w') as fout:
        for line in fin:
            ex = json.loads(line)
            user_content = ex['text']
            labels = ex.get('labels', [])
            assistant_content = json.dumps(labels)
            record = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": assistant_content}
                ]
            }
            fout.write(json.dumps(record) + "\n")


def main():
    base = Path("data/processed")
    prepare(base / "train.jsonl", base / "train_prepared.jsonl")
    prepare(base / "val.jsonl",   base / "val_prepared.jsonl")
    print("Prepared chat-based JSONL for train and val splits.")


if __name__ == '__main__':
    main()
