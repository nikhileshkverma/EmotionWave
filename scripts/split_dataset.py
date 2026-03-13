# scripts/split_dataset.py
import json
import random
import pathlib

random.seed(42)

SRC = pathlib.Path("data/processed/goemotions.jsonl")
data = [json.loads(line) for line in SRC.open()]
random.shuffle(data)

n = len(data)
splits = {"train": 0.8, "val": 0.1, "test": 0.1}
start = 0

for name, frac in splits.items():
    end = start + int(frac * n)
    out_path = pathlib.Path(f"data/processed/{name}.jsonl")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        for item in data[start:end]:
            f.write(json.dumps(item) + "\n")
    start = end
