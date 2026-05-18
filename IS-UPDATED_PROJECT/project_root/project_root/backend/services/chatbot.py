# services/chatbot.py

import os
import pickle
import requests
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ===================== CONFIG =====================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"          # Recommended for CPU speed + quality

INDEX_DIR = "faiss_index"
DATA_DIR = "data"

TOP_K = 1
MAX_CONTEXT_CHARS = 300       # smaller = faster
NUM_PREDICT = 150             # max tokens to predict

# ===================== LOAD ONCE =====================
index = faiss.read_index(os.path.join(INDEX_DIR, "index.faiss"))

with open(os.path.join(INDEX_DIR, "metadata.pkl"), "rb") as f:
    filenames = pickle.load(f)

documents = {
    file: open(os.path.join(DATA_DIR, file), encoding="utf-8").read()
    for file in filenames
}

embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ===================== FUNCTIONS =====================

def retrieve_context(query: str) -> str:
    """Retrieve most relevant document chunk from FAISS"""
    embedding = embedder.encode([query], normalize_embeddings=True).astype("float32")
    _, indices = index.search(embedding, TOP_K)
    doc_name = filenames[indices[0][0]]
    return documents[doc_name][:MAX_CONTEXT_CHARS]

def build_prompt(user_message: str, short_answer=False) -> str:
    """Build prompt with optional short/detailed mode"""
    context = retrieve_context(user_message)
    if short_answer:
        prompt = f"""
You are a cybersecurity expert.
Answer the question in 2 lines max.
Use clear and simple language.
Do not add unnecessary details.

Context:
{context}

Question:
{user_message}
"""
    else:
        prompt = f"""
You are a cybersecurity expert.
Answer clearly and professionally.
Use Markdown:
- Headings
- Bullet points
- Numbered lists
Keep it concise but informative (max 150 words).

Context:
{context}

Question:
{user_message}
"""
    return prompt

def get_reply(user_message: str, short_answer=False, stream=False):
    """
    Main chatbot function.
    short_answer=True → 2-line answer
    stream=True → streaming output (token by token)
    """
    prompt = build_prompt(user_message, short_answer)

    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "num_ctx": 1024,
                "num_predict": NUM_PREDICT
            }
        }

        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        if response.status_code != 200:
            return "⚠️ LLM server error. Please try again."

        return response.json().get("response", "No response generated.")

    except requests.exceptions.ConnectionError:
        return "❌ Ollama is not running. Start it using: ollama run phi3"

    except Exception as e:
        return f"⚠️ Internal error: {str(e)}"

# ===================== Multi-turn chat memory (Optional) =====================
conversation_history = []

def chat(user_message: str, short_answer=False, stream=False):
    """
    Chat with memory of previous conversation.
    """
    global conversation_history

    # Combine previous conversation into context
    if conversation_history:
        combined_context = "\n".join(conversation_history[-5:])  # last 5 turns
        user_message_full = f"{combined_context}\nUser: {user_message}"
    else:
        user_message_full = user_message

    reply = get_reply(user_message_full, short_answer=short_answer, stream=stream)
    conversation_history.append(f"User: {user_message}")
    conversation_history.append(f"Bot: {reply}")
    return reply
