"""
Task 2 - RootSoftware Text-Processing API protected by API keys.

POST /process   (header: X-API-Key: <key>)
    body: {"text": "hello world", "operation": "upper"}   # operation is optional

Keys are NEVER stored in plain text. generate_keys.py creates three keys,
prints them once (to be shared privately) and stores only their SHA-256 hashes
in api_keys.json. The API hashes the submitted key and compares it with the
stored hashes using a constant-time comparison.
"""
import hashlib
import hmac
import json
import os
from functools import wraps

from flask import Flask, jsonify, request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_FILE = os.environ.get("API_KEYS_FILE", os.path.join(BASE_DIR, "api_keys.json"))

app = Flask(__name__)


def load_consumers():
    """Return {consumer_name: sha256_hash_of_key}."""
    try:
        with open(KEYS_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


def find_consumer(presented_key):
    """Return the consumer name for a valid key, else None (constant-time compare)."""
    presented_hash = hashlib.sha256(presented_key.encode("utf-8")).hexdigest()
    match = None
    for name, stored_hash in load_consumers().items():
        if hmac.compare_digest(presented_hash, stored_hash):
            match = name
    return match


def require_api_key(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key:
            return jsonify({"error": "Missing API key. Send it in the X-API-Key header."}), 401
        consumer = find_consumer(key.strip())
        if consumer is None:
            return jsonify({"error": "Invalid API key."}), 403
        request.consumer = consumer
        return view(*args, **kwargs)

    return wrapper


OPERATIONS = {
    "upper": str.upper,
    "lower": str.lower,
    "title": str.title,
    "reverse": lambda s: s[::-1],
}


@app.post("/process")
@require_api_key
def process():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        return jsonify({"error": "JSON body with a string field 'text' is required"}), 400
    op = data.get("operation", "upper")
    if op not in OPERATIONS:
        return jsonify({"error": f"Unknown operation. Choose one of: {', '.join(OPERATIONS)}"}), 400
    return jsonify(
        {
            "consumer": request.consumer,
            "operation": op,
            "original": data["text"],
            "result": OPERATIONS[op](data["text"]),
        }
    ), 200


@app.get("/")
def index():
    return jsonify({"service": "RootSoftware Text API", "endpoint": "POST /process", "auth": "X-API-Key header"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
