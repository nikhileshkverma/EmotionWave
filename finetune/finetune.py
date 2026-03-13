# finetune_and_evaluate.py

from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from sklearn.metrics import classification_report
from sklearn.preprocessing import MultiLabelBinarizer

# ─── LOAD ENV ──────────────────────────────────────────────────────────────────
# adjust the path if needed
load_dotenv(dotenv_path="/Users/akashjaiswal/EmotionChatBot/.env")
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Missing OPENAI_API_KEY in environment")

client = OpenAI(api_key=api_key)

# ─── CONFIG ────────────────────────────────────────────────────────────────────
# your newly fine-tuned model name
FINE_TUNED_MODEL = "ft:gpt-4o-mini-2024-07-18:personal:emotion-classifier:BR2kHLuM"
TEST_PATH        = "data/processed/test.jsonl"

ALL_EMOTIONS = [
    "anger","annoyance","approval","caring","confusion","curiosity","desire",
    "disappointment","disapproval","disgust","embarrassment","excitement",
    "fear","gratitude","grief","joy","love","nervousness","optimism","pride",
    "realization","relief","remorse","sadness","surprise","neutral"
]


def evaluate(model_name: str):
    print(f"Evaluating with model {model_name!r} on {TEST_PATH} …")
    # load test examples
    with open(TEST_PATH) as f:
        examples = [json.loads(line) for line in f]

    y_true, y_pred = [], []
    for ex in examples:
        prompt = f"Text: {ex['text']}\nEmotion(s):"
        resp = client.completions.create(
            model=model_name,
            prompt=prompt,
            max_tokens=10,
            temperature=0,
        )
        # parse comma-separated labels
        pred_txt = resp.choices[0].text.strip()
        preds = [p.strip() for p in pred_txt.split(",") if p.strip()]

        y_true.append(ex.get("labels", []))
        y_pred.append(preds)

    # binarize and report
    mlb = MultiLabelBinarizer(classes=ALL_EMOTIONS)
    y_true_bin = mlb.fit_transform(y_true)
    y_pred_bin = mlb.transform(y_pred)

    report = classification_report(
        y_true_bin,
        y_pred_bin,
        target_names=mlb.classes_,
        output_dict=True,
        zero_division=0
    )

    # save to file
    out_path = "evaluation.json"
    with open(out_path, "w") as out:
        json.dump(report, out, indent=2)
    print(f"Saved evaluation report to {out_path}")


if __name__ == "__main__":
    evaluate(FINE_TUNED_MODEL)
