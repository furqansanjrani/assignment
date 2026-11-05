"""
Generate three API keys (one per consumer) with Python's `secrets` module.

* Stores only SHA-256 hashes in api_keys.json  -> safe to commit.
* Prints the raw keys ONCE and also writes them to keys_to_share.txt
  (git-ignored) so you can send each tester only their own key privately.

Usage:  python generate_keys.py
"""
import hashlib
import json
import os
import secrets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONSUMERS = ["tester_alpha", "tester_beta", "tester_gamma"]


def main():
    hashes, raw = {}, {}
    for name in CONSUMERS:
        key = "rs_" + secrets.token_urlsafe(32)
        raw[name] = key
        hashes[name] = hashlib.sha256(key.encode("utf-8")).hexdigest()

    with open(os.path.join(BASE_DIR, "api_keys.json"), "w", encoding="utf-8") as fh:
        json.dump(hashes, fh, indent=2)

    share_path = os.path.join(BASE_DIR, "keys_to_share.txt")
    with open(share_path, "w", encoding="utf-8") as fh:
        for name, key in raw.items():
            fh.write(f"{name}: {key}\n")
    try:
        os.chmod(share_path, 0o600)
    except OSError:
        pass

    print("Generated API keys (shown once - send each to its tester privately):\n")
    for name, key in raw.items():
        print(f"  {name:<14} {key}")
    print("\nHashes saved to api_keys.json. Raw keys saved to keys_to_share.txt (do NOT commit).")


if __name__ == "__main__":
    main()
