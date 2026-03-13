import json
import os
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv

# ─── CONFIG ─────────────────────────────────────────────────────────────────────
load_dotenv(dotenv_path="/Users/akashjaiswal/EmotionChatBot/.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL_ID = "ft:gpt-4o-mini-2024-07-18:personal:emotion-classifier:BR2kHLuM"  # <-- CHANGE this to your model
INPUT_FILE = "data/processed/val_prepared.jsonl"
OUTPUT_FILE = "evaluation.json"

# ─── LOAD VALIDATION DATA ────────────────────────────────────────────────────────
def load_validation_data(filepath):
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            messages = item.get("messages", [])
            user_input = next((m["content"] for m in messages if m["role"] == "user"), None)
            expected_output_raw = next((m["content"] for m in messages if m["role"] == "assistant"), None)
            if user_input and expected_output_raw:
                try:
                    expected_output = json.loads(expected_output_raw)
                except json.JSONDecodeError:
                    expected_output = [expected_output_raw]
                data.append({
                    "input": user_input,
                    "output": expected_output
                })
    return data

# ─── EVALUATE MODEL ───────────────────────────────────────────────────────────────
def evaluate_model(validation_data):
    results = []
    for item in tqdm(validation_data, desc="Evaluating"):
        input_text = item["input"]
        expected_output = item["output"]

        try:
            print(f"\n---\nInput: {input_text}")

            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=[
                    {"role": "system", "content": "You are an emotion classifier. Respond with a JSON array of emotions."},
                    {"role": "user", "content": input_text}
                ],
                temperature=0,
                top_p=0,
            )

            model_output_raw = response.choices[0].message.content.strip()
            print(f"Model raw output: {model_output_raw}")

            try:
                model_output = json.loads(model_output_raw)
            except json.JSONDecodeError:
                model_output = [e.strip() for e in model_output_raw.strip("[]").split(",") if e.strip()]

            correct = all(label in model_output for label in expected_output)

            results.append({
                "input": input_text,
                "expected_output": expected_output,
                "model_output": model_output,
                "correct": correct
            })

        except Exception as e:
            print(f"❌ Error evaluating input: {input_text}")
            print(e)

    return results

# ─── SAVE RESULTS ────────────────────────────────────────────────────────────────
def save_results(results, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Saved evaluation results to {filepath}")

# ─── MAIN ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    validation_data = load_validation_data(INPUT_FILE)
    print(f"Loaded {len(validation_data)} validation examples.")
    evaluation_results = evaluate_model(validation_data)
    save_results(evaluation_results, OUTPUT_FILE)
