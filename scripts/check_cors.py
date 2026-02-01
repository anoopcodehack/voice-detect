import sys, os
sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..')))
# Ensure tests set the required env vars before importing the app
os.environ.setdefault('API_KEY', 'sk_test_123456789')
os.environ.setdefault('FRONTEND_ORIGIN', 'http://localhost:3000')
from fastapi.testclient import TestClient
from backend.main import app

c = TestClient(app)
r = c.options('/api/voice-detection', headers={
    'Origin': 'http://localhost:3000',
    'Access-Control-Request-Method': 'POST',
    'Access-Control-Request-Headers': 'content-type,x-api-key'
})
print('STATUS', r.status_code)
print('HEADERS')
for k, v in r.headers.items():
    if k.lower().startswith('access-control'):
        print(f'{k}: {v}')
print('BODY:', r.text)
