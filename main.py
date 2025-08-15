import hmac
import hashlib
import time
import json
import requests

def generate_auth_headers(method: str, path: str, payload: dict = None, fingerprint: str = None) -> dict:
    timestamp = int(time.time() // 60)
    payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=False, ensure_ascii=False) if payload else ""
    print("提交分数数据:",payload_str)
    data = f"{method}|{path}|{timestamp}|{fingerprint}|{payload_str}"
    print(data)
    signature = hmac.new(
        "x".encode('utf-8'),
        data.encode('utf-8'),
        hashlib.md5
    ).hexdigest()
    
    return {
        "x-auth-hash": signature,
        "x-timestamp": str(timestamp),
        "x-fingerprint": fingerprint,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "priority": "u=1, i",
        "accept-encoding": "gzip, deflate, br, zstd",
        "referer": "https://xiaommx.cn/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "content-type": "application/json"
    }

# 1. 获取 token
headers = generate_auth_headers(
    method="POST",
    path="/no-use/library-itch/start-session",
    payload=None,
    fingerprint="1541930801"
)
response = requests.post(
    "https://api.xiaommx.cn/no-use/library-itch/start-session",
    headers=headers,
    json=None  # 明确发送空请求体
)
token = response.json()["token"]
print("Token:", token)

# 2. 提交分数（修正点：使用 json=body 发送实际请求体）

body = {
    "score":80,
    "token": token,
    "clientGameTime": 10
}
headers2 = generate_auth_headers(
    method="POST",
    path="/no-use/library-itch/submit-score",
    payload=body,  # 签名时包含请求体
    fingerprint="1541930801"
    
)
payload_str = json.dumps(body, separators=(',', ':'), sort_keys=False, ensure_ascii=False)
time.sleep(10)
response2 = requests.post(
    "https://api.xiaommx.cn/no-use/library-itch/submit-score",
    headers=headers2,
    data=payload_str,  # 实际发送请求体
)
print("提交分数头:",headers2)

print("提交分数响应:", response2.text)
