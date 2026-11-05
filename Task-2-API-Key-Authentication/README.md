# Task 2 — API Key Generation and Sharing

## Project Description

This project is a Text Processing REST API developed using Python and Flask. It demonstrates how API keys can be generated, shared securely, and used to authenticate different consumers.

The API allows authorized consumers to perform text-processing operations such as uppercase, lowercase, title case, and reverse.

## Technologies Used

- Python
- Flask
- REST API
- JSON
- SHA-256 Hashing
- HTTP Requests

## Features

- Generate three unique API keys using Python's `secrets` module.
- Authenticate requests using the `X-API-Key` header.
- Store SHA-256 hashes instead of plaintext API keys.
- Support three independent consumers.
- Perform text-processing operations.
- Reject missing and invalid API keys.

## API Consumers

1. `tester_alpha`
2. `tester_beta`
3. `tester_gamma`

Each consumer receives a separate API key.

## API Endpoint

**POST /process**

Example JSON request:

```json
{
  "text": "hello world",
  "operation": "upper"
}
```

Example successful response:

```json
{
  "consumer": "tester_alpha",
  "operation": "upper",
  "original": "hello world",
  "result": "HELLO WORLD"
}
```

## Supported Operations

| Operation | Function |
|---|---|
| upper | Converts text to uppercase |
| lower | Converts text to lowercase |
| title | Converts text to title case |
| reverse | Reverses the text |

## How to Run the Project

**Step 1: Install requirements**

```bash
pip install -r requirements.txt
```

**Step 2: Generate API keys**

```bash
python generate_keys.py
```

This creates:

- `api_keys.json` — SHA-256 hashes of the generated keys.
- `keys_to_share.txt` — original API keys for private sharing.

Both generated files should remain local and must not be uploaded to the public repository.

**Step 3: Start the Flask server**

```bash
python app.py
```

Server URL:

`http://127.0.0.1:5001`

**Step 4: Test the API**

Send a POST request to `/process` with a valid API key in the `X-API-Key` header and a JSON body containing the text.

## API Testing Results

| Test | Expected HTTP Status |
|---|---|
| Valid key — tester_alpha | 200 OK |
| Valid key — tester_beta | 200 OK |
| Valid key — tester_gamma | 200 OK |
| Missing API key | 401 Unauthorized |
| Invalid API key | 403 Forbidden |
| Valid key with missing text | 400 Bad Request |

All three consumer authentication tests and the missing/invalid API key tests were completed successfully.

## API Key Security

API keys are generated using Python's `secrets` module.

The application stores SHA-256 hashes and compares them using `hmac.compare_digest`.

Each consumer should receive only their own API key through a private communication channel.

The raw API keys and generated local files are excluded from GitHub using `.gitignore`.

## Demonstration Video

[Watch Task 2 Demonstration](PASTE_YOUR_YOUTUBE_VIDEO_LINK_HERE)

## Conclusion

This project demonstrates API key generation, secure key sharing, authentication, and controlled access to a Flask REST API. It also demonstrates how valid requests are processed while missing or invalid API keys are rejected.
