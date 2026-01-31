import requests
import base64
import json

# =========================
# CONFIG
# =========================
API_URL = "https://voice-detect-1-d9gm.onrender.com/api/voice-detection"  # your deployed endpoint
API_KEY = "sk_test_123456789"  # your API key
ALLOWED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# Sample audio (small dummy MP3)
DUMMY_AUDIO = base64.b64encode(b"FAKE_MP3_DATA").decode("utf-8")

# =========================
# HELPER FUNCTION
# =========================
def check_response_shape(data):
    required_fields = ["status", "language", "classification", "confidenceScore", "explanation"]
    if not all(field in data for field in required_fields):
        return False, "Missing fields"
    if data["classification"] not in ["HUMAN", "AI_GENERATED"]:
        return False, f"Invalid classification: {data['classification']}"
    return True, ""

# =========================
# TEST FUNCTIONS
# =========================
def test_api_key_enforcement():
    print("Test 1: API Key enforcement (no key)...")
    payload = {"language": "Tamil", "audioFormat": "mp3", "audioBase64": DUMMY_AUDIO}
    response = requests.post(API_URL, json=payload)  # No API key
    try:
        data = response.json()
    except ValueError:
        data = {}

    message = ""
    if isinstance(data, dict):
        message = data.get("message") or data.get("detail", {}).get("message", "")

    if response.status_code == 401 or message == "Invalid API key or malformed request":
        print("✅ PASS")
    else:
        print("❌ FAIL")
        print("Response:", response.text)

def test_language_restriction():
    print("\nTest 2: Language restriction (invalid language)...")
    payload = {"language": "French", "audioFormat": "mp3", "audioBase64": DUMMY_AUDIO}
    headers = {"x-api-key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers)
    try:
        data = response.json()
    except ValueError:
        data = {}

    message = ""
    if isinstance(data, dict):
        message = data.get("message") or data.get("detail", {}).get("message", "")

    if response.status_code == 400 or message == "Unsupported language":
        print("✅ PASS")
    else:
        print("❌ FAIL")
        print("Response:", response.text)

def test_allowed_languages():
    print("\nTest 3: Test all allowed languages...")
    headers = {"x-api-key": API_KEY}
    for lang in ALLOWED_LANGUAGES:
        payload = {"language": lang, "audioFormat": "mp3", "audioBase64": DUMMY_AUDIO}
        response = requests.post(API_URL, json=payload, headers=headers)
        try:
            data = response.json()
        except ValueError:
            print(f"❌ FAIL: {lang} → Invalid JSON")
            continue

        ok, msg = check_response_shape(data)
        if response.status_code == 200 and ok:
            print(f"✅ PASS: {lang}")
        else:
            print(f"❌ FAIL: {lang} → {msg}")
            print("Response:", data)

# =========================
# RUN ALL TESTS
# =========================
if __name__ == "__main__":
    test_api_key_enforcement()
    test_language_restriction()
    test_allowed_languages()
