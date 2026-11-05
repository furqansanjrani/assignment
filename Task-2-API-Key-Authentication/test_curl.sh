#!/usr/bin/env bash
# Demonstrates: each valid key works, invalid key rejected, missing key rejected.
# Reads the three keys from keys_to_share.txt (created by generate_keys.py).
# Each tester can instead run a single command with their own key, e.g.:
#   curl -X POST http://127.0.0.1:5001/process \
#        -H "Content-Type: application/json" -H "X-API-Key: <YOUR_KEY>" \
#        -d '{"text":"hello rootsoftware"}'
BASE="${BASE:-http://127.0.0.1:5001}"
HERE="$(cd "$(dirname "$0")" && pwd)"
KEYFILE="$HERE/keys_to_share.txt"

[ -f "$KEYFILE" ] || { echo "Run python generate_keys.py first."; exit 1; }

i=0
while IFS=': ' read -r name key; do
  i=$((i+1))
  echo "== Consumer $i ($name) - valid key"
  curl -s -w ' [HTTP %{http_code}]\n' -X POST "$BASE/process" \
       -H "Content-Type: application/json" -H "X-API-Key: $key" \
       -d "{\"text\":\"hello from $name\"}"
done < "$KEYFILE"

echo "== Invalid key (expect 403)"
curl -s -w ' [HTTP %{http_code}]\n' -X POST "$BASE/process" \
     -H "Content-Type: application/json" -H "X-API-Key: not-a-real-key" \
     -d '{"text":"hello"}'

echo "== Missing key (expect 401)"
curl -s -w ' [HTTP %{http_code}]\n' -X POST "$BASE/process" \
     -H "Content-Type: application/json" -d '{"text":"hello"}'

echo "== Valid key, bad body (expect 400)"
FIRSTKEY="$(head -n1 "$KEYFILE" | cut -d' ' -f2)"
curl -s -w ' [HTTP %{http_code}]\n' -X POST "$BASE/process" \
     -H "Content-Type: application/json" -H "X-API-Key: $FIRSTKEY" -d '{"wrong":1}'

echo "== Optional operation: reverse"
curl -s -w ' [HTTP %{http_code}]\n' -X POST "$BASE/process" \
     -H "Content-Type: application/json" -H "X-API-Key: $FIRSTKEY" \
     -d '{"text":"RootSoftware","operation":"reverse"}'
