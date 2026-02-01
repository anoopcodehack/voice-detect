import time,base64,requests,os,sys
url='http://127.0.0.1:8000/api/voice-detection'
# Wait for server to be up
for i in range(20):
    try:
        r=requests.options(url, headers={'Origin':'http://localhost:3000','Access-Control-Request-Method':'POST','Access-Control-Request-Headers':'content-type,x-api-key'}, timeout=1)
        print('OPTIONS status', r.status_code)
        print('CORS allow-origin:', r.headers.get('access-control-allow-origin'))
        break
    except Exception as e:
        print('Waiting for server...', i, str(e))
        time.sleep(0.5)
else:
    print('Server did not respond to OPTIONS; aborting')
    sys.exit(2)

# Check sample.mp3 exists
path='sample.mp3'
if not os.path.exists(path):
    print('sample.mp3 missing; skipping POST test')
    sys.exit(0)

b=open(path,'rb').read()
payload={'language':'Hindi','audioFormat':'mp3','audioBase64':base64.b64encode(b).decode()}
for i in range(6):
    try:
        r=requests.post(url, json=payload, headers={'x-api-key':'sk_test_123456789'}, timeout=10)
        print('POST status', r.status_code)
        print('Response:', r.text)
        break
    except Exception as e:
        print('POST attempt', i, 'error', e)
        time.sleep(1)
else:
    print('POST failed after retries')
