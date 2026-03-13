# scripts/convert_to_jsonl.py
import csv
import json
import pathlib
import random

random.seed(42)

INPUT = pathlib.Path("data/raw/goemotions_1.csv")
OUT = pathlib.Path("data/processed/goemotions.jsonl")
OUT.parent.mkdir(parents=True, exist_ok=True)

# these columns aren’t labels
drop_cols = {
    "id","author","subreddit","link_id","parent_id",
    "created_utc","rater_id","example_very_unclear"
}

with INPUT.open(newline="") as f:
    reader = csv.DictReader(f)
    # infer which columns are emotions
    emotion_cols = [c for c in reader.fieldnames if c not in drop_cols and c != "text"]
    f.seek(0)
    reader = csv.DictReader(f)

    with OUT.open("w") as out:
        for row in reader:
            text = row["text"]
            # pick every emotion column with a '1'
            labels = [e for e in emotion_cols if row[e] == "1"]
            out.write(json.dumps({"text": text, "labels": labels}) + "\n")
