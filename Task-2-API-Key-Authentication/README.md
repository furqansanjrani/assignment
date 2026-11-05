# Task 2 — API Key Generation and Sharing (RootSoftware Text API)

`POST /process` takes `{"text": "..."}` and returns the processed (upper-cased) text. Access requires a valid key in the `X-API-Key` header.

## Run

```bash
pip install -r requirements.txt
python generate_keys.py     # creates 3 keys (secrets module)
python app.py               # API on http://127.0.0.1:5001
```

`generate_keys.py` produces:

* `api_keys.json` — only **SHA-256 hashes** of the keys (safe to commit)
* `keys_to_share.txt` — the raw keys, one per consumer (**git-ignored, never commit**)

| Consumer | Key |
|---|---|
| tester_alpha | sent privately to tester 1 |
| tester_beta | sent privately to tester 2 |
| tester_gamma | sent privately to tester 3 |

## How the key check works

1. Read `X-API-Key`. Missing → **401**.
2. Hash it with SHA-256 and compare with each stored hash using `hmac.compare_digest` (constant-time).
3. No match → **403**. Match → process the text and return the result (**200**).

## Testing with cURL (what each tester runs)

```bash
curl -X POST http://127.0.0.1:5001/process \
     -H "Content-Type: application/json" \
     -H "X-API-Key: <YOUR_KEY>" \
     -d '{"text":"hello rootsoftware"}'
```

```json
{"consumer":"tester_alpha","operation":"upper","original":"hello rootsoftware","result":"HELLO ROOTSOFTWARE"}
```

Optional `"operation"`: `upper` (default), `lower`, `title`, `reverse`.

| Request | Result |
|---|---|
| valid key (each of the 3) | 200 + processed text |
| wrong key | 403 `{"error":"Invalid API key."}` |
| no `X-API-Key` header | 401 `{"error":"Missing API key. ..."}` |
| valid key, no `text` field | 400 |

`./test_curl.sh` runs all of the above automatically.

## Sharing keys securely

Send each tester **only their own key**, on a private channel (direct message or a password manager share), not in the repo, a group chat, or a public screenshot. If a key leaks, re-run `generate_keys.py` (this invalidates all old keys) and re-issue.
