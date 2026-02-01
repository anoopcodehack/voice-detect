import base64,requests,os
url='http://127.0.0.1:8001/api/voice-detection'
path='sample.mp3'
if not os.path.exists(path):
    print('sample.mp3 missing; skipping POST')
    raise SystemExit(0)

b=open(path,'rb').read()
payload={'language':'Hindi','audioFormat':'mp3','audioBase64':base64.b64encode(b).decode()}
r=requests.post(url, json=payload, headers={'x-api-key':'sk_test_123456789'})
print('STATUS', r.status_code)
print('RESPONSE', r.text)
