import requests
import base64

API_URL = "https://voice-detect-1-c20t.onrender.com/api/voice-detection"
API_KEY = "sk_test_123456789"
ALLOWED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
DUMMY_AUDIO = base64.b64encode(b"FAKE_MP3_DATA").decode("utf-8")

def check_response_shape(data):
    required_fields = ["status", "language", "classification", "confidenceScore", "explanation"]
    if not all(field in data for field in required_fields):
        return False, "Missing fields"
    if data["classification"] not in ["HUMAN", "AI_GENERATED"]:
        return False, f"Invalid classification: {data['classification']}"
    return True, ""

def test_api_key_enforcement():
    print("Test 1: API Key enforcement (no key)...")
    payload = {"language": "Tamil", "audioFormat": "mp3", "audioBase64": DUMMY_AUDIO}
    response = requests.post(API_URL, json=payload)
    try:
        data = response.json()
    except:
        data = {}
    message = data.get("message") if isinstance(data, dict) else ""
    if response.status_code == 401 or message == "Invalid API key or malformed request":
        print("✅ PASS")
    else:
        print("❌ FAIL", response.text)

def test_language_restriction():
    print("\nTest 2: Language restriction (invalid language)...")
    payload = {"language": "French", "audioFormat": "mp3", "audioBase64": DUMMY_AUDIO}
    headers = {"x-api-key": API_KEY}
    response = requests.post(API_URL, json=payload, headers=headers)
    try:
        data = response.json()
    except:
        data = {}
    message = data.get("message") if isinstance(data, dict) else ""
    if response.status_code == 400 or message == "Unsupported language":
        print("✅ PASS")
    else:
        print("❌ FAIL", response.text)

def test_allowed_languages():
    print("\nTest 3: Test all allowed languages...")
    headers = {"x-api-key": API_KEY}
    for lang in ALLOWED_LANGUAGES:
        payload = {"language": lang, "audioFormat": "mp3", "audioBase64": DUMMY_AUDIO}
        response = requests.post(API_URL, json=payload, headers=headers)
        try:
            data = response.json()
        except:
            print(f"❌ FAIL: {lang} → Invalid JSON")
            continue
        ok, msg = check_response_shape(data)
        if response.status_code == 200 and ok:
            print(f"✅ PASS: {lang}")
        else:
            print(f"❌ FAIL: {lang} → {msg}")

if __name__ == "__main__":
    test_api_key_enforcement()
    test_language_restriction()
    test_allowed_languages()

