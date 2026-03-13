# backend/app.py

import os
import json
import dotenv

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

# ─── LOAD ENV ────────────────────────────────────────────────────────────────────
dotenv.load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment")

# ─── INIT CLIENT ─────────────────────────────────────────────────────────────────
client = AsyncOpenAI(api_key=API_KEY)

# ─── MODEL & PROMPTS ─────────────────────────────────────────────────────────────
# Use your fine-tuned emotion classifier here:
CLASSIFIER_MODEL = "ft:gpt-4o-mini-2024-07-18:personal:emotion-classifier:BR2kHLuM"
# Use a faster base model for empathy generation
GEN_MODEL        = "gpt-4o-mini"

SYSTEM_PROMPT = """
You are an emotion classifier. Return a JSON array (lower-case strings)
containing any emotions from this list that apply:
[anger, annoyance, approval, caring, confusion, curiosity, desire,
disappointment, disapproval, disgust, embarrassment, excitement, fear,
gratitude, grief, joy, love, nervousness, optimism, pride, realization,
relief, remorse, sadness, surprise, neutral]
Respond with JSON only.
"""

GEN_PROMPT_TEMPLATE = """
You are an empathetic assistant. A user just said:
\"\"\"{user_text}\"\"\"

From your sentiment classifier, they seem to be feeling: {emotions_list}.

Respond with 1–2 sentences that acknowledge their emotion and offer support or encouragement.
"""

# ─── FASTAPI SETUP ───────────────────────────────────────────────────────────────
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTES ─────────────────────────────────────────────────────────────────────

@app.post("/classify")
async def classify(payload: dict):
    text = payload.get("text")
    if not text:
        raise HTTPException(400, detail="Missing 'text' in request body")

    resp = await client.chat.completions.create(
        model=CLASSIFIER_MODEL,
        messages=[
            {"role": "system",  "content": SYSTEM_PROMPT},
            {"role": "user",    "content": text}
        ],
        temperature=0,
        top_p=0
    )

    content = resp.choices[0].message.content.strip()
    try:
        emotions = json.loads(content)
    except json.JSONDecodeError:
        # fallback parsing
        emotions = [e.strip() for e in content.strip("[]").split(",") if e.strip()]

    return {"emotions": emotions}


# @app.post("/chat")
# async def chat(payload: dict = Body(...)):
#     history = payload.get("history", [])
#     print(f"Received payload: {payload}")
#     text = payload.get("text")
#     if not text:
#         raise HTTPException(400, detail="Missing 'text' in request body")

#     # 1) classify
#     classify_resp = await client.chat.completions.create(
#         model=CLASSIFIER_MODEL,
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user",   "content": text}
#         ],
#         temperature=0,
#         top_p=0,
#     )
#     raw = classify_resp.choices[0].message.content.strip()
#     try:
#         emotions = json.loads(raw)
#     except json.JSONDecodeError:
#         emotions = [e.strip() for e in raw.strip("[]").split(",") if e.strip()]

#     # 2) generate empathetic reply
#     gen_prompt = GEN_PROMPT_TEMPLATE.format(
#         user_text=text.replace('"', '\\"'),
#         emotions_list=", ".join(emotions) or "neutral"
#     )
#     gen_resp = await client.chat.completions.create(
#         model=GEN_MODEL,
#         messages=[{"role": "system", "content": gen_prompt}],
#         temperature=0.7,
#         max_tokens=60,
#     )
#     reply = gen_resp.choices[0].message.content.strip()

#     return {"reply": reply, "emotions": emotions}


@app.post("/chat")
async def chat(payload: dict = Body(...)):
    history = payload.get("history", [])
    if not history:
        raise HTTPException(400, detail="Missing 'history' in request body")

    # Extract the latest user message
    latest_message = history[-1]["content"]

    # Step 1: Classify emotions for the latest user message
    classify_resp = await client.chat.completions.create(
        model=CLASSIFIER_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": latest_message}
        ],
        temperature=0,
        top_p=0,
    )

    raw = classify_resp.choices[0].message.content.strip()
    try:
        emotions = json.loads(raw)
    except json.JSONDecodeError:
        emotions = [e.strip() for e in raw.strip("[]").split(",") if e.strip()]

    # Step 2: Create an empathetic reply
    gen_prompt = GEN_PROMPT_TEMPLATE.format(
        user_text=latest_message.replace('"', '\\"'),
        emotions_list=", ".join(emotions) or "neutral"
    )

    # Optionally, you could use the full history if you want deeper context
    full_messages = [{"role": "system", "content": "You are a supportive assistant."}]
    full_messages += history
    full_messages += [{"role": "assistant", "content": gen_prompt}]

    gen_resp = await client.chat.completions.create(
        model=GEN_MODEL,
        messages=full_messages,
        temperature=0.7,
        max_tokens=100,
    )

    reply = gen_resp.choices[0].message.content.strip()

    return {"reply": reply, "emotions": emotions}
