#!/usr/bin/env python3
# scripts/eval_gpt_emotions.py

import os
import json
import asyncio
import argparse
from dotenv import load_dotenv
from openai import AsyncOpenAI
from sklearn.metrics import f1_score, precision_score, recall_score
from httpx import HTTPStatusError

# ─── CONFIG ────────────────────────────────────────────────────────────────────
load_dotenv(dotenv_path="/Users/akashjaiswal/EmotionChatBot/.env")
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment")

client = AsyncOpenAI(api_key=API_KEY)
MODEL = "gpt-4o-mini-2024-07-18"  # updated base

SYSTEM_PROMPT = """
You are an emotion classifier. I will send you multiple lines of text
(separated by newlines). Respond with exactly one JSON array of length N,
where each element is a list of emotions (from [anger, annoyance, approval,
caring, confusion, curiosity, desire, disappointment, disapproval, disgust,
embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness,
optimism, pride, realization, relief, remorse, sadness, surprise, neutral])
that apply to the corresponding line. Do not output any extra text outside
the JSON.
"""

async def classify_batch(texts, max_retries=3):
    backoff = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            resp = await client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system",  "content": SYSTEM_PROMPT},
                    {"role": "user",    "content": "\n".join(texts)}
                ],
                temperature=0, top_p=0
            )
            content = resp.choices[0].message.content.strip()
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # fallback: one JSON array per line
                return [json.loads(l) for l in content.splitlines() if l.strip()]
        except HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < max_retries:
                await asyncio.sleep(backoff)
                backoff *= 2
                continue
            raise

async def main(split_path, max_samples=1000, batch_size=10, throttle_s=0.2):
    y_true, y_pred = [], []
    with open(split_path, 'r') as f:
        batch, gold = [], []
        for i, line in enumerate(f):
            if i >= max_samples:
                break
            obj = json.loads(line)
            batch.append(obj["text"])
            gold.append(obj["labels"])
            if len(batch) == batch_size:
                preds = await classify_batch(batch)
                y_true.extend(gold)
                y_pred.extend(preds)
                batch, gold = [], []
                await asyncio.sleep(throttle_s)

    # build label list
    all_labels = sorted({lbl for sub in y_true for lbl in sub})

    def binarise(lbls):
        return [int(lbl in lbls) for lbl in all_labels]

    y_true_bin = [binarise(lbls) for lbls in y_true]
    y_pred_bin = [binarise(lbls) for lbls in y_pred]

    print("Micro F1:", f1_score(y_true_bin, y_pred_bin, average="micro"))
    print("Micro Precision:", precision_score(y_true_bin, y_pred_bin, average="micro"))
    print("Micro Recall:", recall_score(y_true_bin, y_pred_bin, average="micro"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--split",
        default="data/processed/test.jsonl",
        help="which split to evaluate (must be .jsonl)"
    )
    parser.add_argument("--max", type=int, default=1000)
    args = parser.parse_args()
    asyncio.run(main(args.split, args.max))
