from fastapi.testclient import TestClient
from main import app

API_KEY = "sk_test_123456789"
ALLOWED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
DUMMY_AUDIO = b"FAKE_MP3_DATA"

client = TestClient(app)


def check_response_shape(data):
    required_fields = ["status", "language", "classification", "confidenceScore", "explanation"]
    if not all(field in data for field in required_fields):
        return False, "Missing fields"
    if data["classification"] not in ["HUMAN", "AI_GENERATED"]:
        return False, f"Invalid classification: {data['classification']}"
    return True, ""


def post_audio(language, headers=None, audio_bytes=DUMMY_AUDIO):
    files = {"audio": ("test.mp3", audio_bytes, "audio/mpeg")}
    data = {"language": language}
    return client.post("/api/voice-detection", files=files, data=data, headers=headers or {})


def test_api_key_enforcement():
    print("Test 1: API Key enforcement (no key)...")
    response = post_audio("Tamil", headers={})
    if response.status_code == 401:
        print("✅ PASS")
    else:
        print("❌ FAIL", response.status_code, response.text)


def test_language_restriction():
    print("\nTest 2: Language restriction (invalid language)...")
    headers = {"x-api-key": API_KEY}
    response = post_audio("French", headers=headers)
    if response.status_code == 400:
        print("✅ PASS")
    else:
        print("❌ FAIL", response.status_code, response.text)


def test_allowed_languages():
    print("\nTest 3: Test all allowed languages...")
    headers = {"x-api-key": API_KEY}
    for lang in ALLOWED_LANGUAGES:
        response = post_audio(lang, headers=headers)
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


if __name__ == "__main__":
    test_api_key_enforcement()
    test_language_restriction()
    test_allowed_languages()
