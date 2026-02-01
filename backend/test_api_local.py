import os
os.environ['API_KEY'] = "sk_test_123456789"
from fastapi.testclient import TestClient
from main import app

API_KEY = "sk_test_123456789"
ALLOWED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
DUMMY_AUDIO = b"FAKE_MP3_DATA"

# Try to load a real sample mp3 from repo root for accurate tests
SAMPLE_AUDIO = None
sample_path = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "sample.mp3"))
if os.path.exists(sample_path):
    with open(sample_path, "rb") as f:
        SAMPLE_AUDIO = f.read()

client = TestClient(app)


def check_response_shape(data):
    required_fields = ["status", "language", "classification", "confidenceScore", "explanation"]
    if not all(field in data for field in required_fields):
        return False, "Missing fields"
    if data["classification"] not in ["HUMAN", "AI_GENERATED"]:
        return False, f"Invalid classification: {data['classification']}"
    return True, ""


def post_json_audio(language, headers=None, audio_bytes=DUMMY_AUDIO):
    import base64 as _b64
    payload = {"language": language, "audioFormat": "mp3", "audioBase64": _b64.b64encode(audio_bytes).decode()}
    return client.post("/api/voice-detection", json=payload, headers=headers or {})


def test_api_key_enforcement():
    print("Test 1: API Key enforcement (no key)...")
    response = post_json_audio("Tamil", headers={})
    try:
        data = response.json()
    except Exception:
        data = {}
    if response.status_code == 401 and data.get("status") == "error":
        print("✅ PASS")
    else:
        print("❌ FAIL", response.status_code, response.text)


def test_language_restriction():
    print("\nTest 2: Language restriction (invalid language)...")
    headers = {"x-api-key": API_KEY}
    response = post_json_audio("French", headers=headers)
    if response.status_code == 400:
        print("✅ PASS")
    else:
        print("❌ FAIL", response.status_code, response.text)


def test_allowed_languages():
    print("\nTest 3: Test all allowed languages...")
    headers = {"x-api-key": API_KEY}
    for lang in ALLOWED_LANGUAGES:
        # Use a real sample mp3 if present; otherwise skip the accurate detection test
        if SAMPLE_AUDIO is None:
            print(f"❌ SKIP: {lang} → missing sample.mp3 (place sample.mp3 at repo root to run this test)")
            continue
        response = post_json_audio(lang, headers=headers, audio_bytes=SAMPLE_AUDIO)
        try:
            data = response.json()
        except Exception:
            print(f"❌ FAIL: {lang} → Invalid JSON")
            continue
        ok, msg = check_response_shape(data)
        if response.status_code == 200 and ok:
            print(f"✅ PASS: {lang}")
        else:
            print(f"❌ FAIL: {lang} → {msg} (status: {response.status_code})")


def test_invalid_base64():
    print("\nTest 4: Invalid base64 payload")
    headers = {"x-api-key": API_KEY}
    payload = {"language":"Tamil","audioFormat":"mp3","audioBase64":"NOT_BASE64"}
    response = client.post("/api/voice-detection", json=payload, headers=headers)
    if response.status_code == 400 and response.json().get("status") == "error":
        print("✅ PASS")
    else:
        print("❌ FAIL", response.status_code, response.text)


def test_confidence_range():
    print("\nTest 5: Confidence score in [0,1]")
    headers = {"x-api-key": API_KEY}
    if SAMPLE_AUDIO is None:
        print("❌ SKIP: missing sample.mp3 (place sample.mp3 at repo root to run this test)")
        return
    response = post_json_audio("Tamil", headers=headers, audio_bytes=SAMPLE_AUDIO)
    data = response.json()
    cs = data.get("confidenceScore")
    if isinstance(cs, (float, int)) and 0 <= cs <= 1:
        print("✅ PASS")
    else:
        print("❌ FAIL", cs)


def test_invalid_mp3_rejected():
    print("\nTest 6: Reject invalid MP3 payloads")
    import base64 as _b64
    payload = {"language": "Tamil", "audioFormat": "mp3", "audioBase64": _b64.b64encode(b"NOT_MP3_DATA").decode()}
    headers = {"x-api-key": API_KEY}
    response = client.post("/api/voice-detection", json=payload, headers=headers)
    try:
        data = response.json()
    except Exception:
        print("❌ FAIL: Invalid JSON response")
        return
    if response.status_code == 400 and data.get("status") == "error":
        print("✅ PASS")
    else:
        print("❌ FAIL", response.status_code, response.text)


def test_json_base64_upload():
    print("\nTest 4: JSON base64 upload path...")
    import base64 as _b64
    if SAMPLE_AUDIO is None:
        print("❌ SKIP: missing sample.mp3 (place sample.mp3 at repo root to run this test)")
        return
    payload = {
        "language": "Tamil",
        "audioFormat": "mp3",
        "audioBase64": _b64.b64encode(SAMPLE_AUDIO).decode()
    }
    headers = {"x-api-key": API_KEY}
    response = client.post("/api/voice-detection", json=payload, headers=headers)
    try:
        data = response.json()
    except Exception:
        print("❌ FAIL: Invalid JSON response")
        return
    ok, msg = check_response_shape(data)
    if response.status_code == 200 and ok:
        print("✅ PASS: JSON path")
    else:
        print("❌ FAIL: JSON path →", response.status_code, data)


if __name__ == "__main__":
    test_api_key_enforcement()
    test_language_restriction()
    test_allowed_languages()
