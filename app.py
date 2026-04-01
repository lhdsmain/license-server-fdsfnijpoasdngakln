from flask import Flask, request, jsonify
import hashlib
import os
import requests
import time

app = Flask(__name__)

SECRET = os.environ.get("SECRET", "X9@kLm!123")

# 👉 你的 GitHub raw 地址（必须改成你自己的）
GITHUB_URL = "https://raw.githubusercontent.com/lhdsmain/license-server-fdsfnijpoasdngakln/refs/heads/main/devices.json"

# 👉 缓存（避免频繁请求 GitHub）
devices_cache = set()
last_update = 0
CACHE_TIME = 60   # 秒


def load_devices():
    global devices_cache, last_update

    # 1分钟内不重复请求
    if time.time() - last_update < CACHE_TIME:
        return devices_cache

    try:
        resp = requests.get(GITHUB_URL, timeout=60)
        data = resp.json()
        devices_cache = set(data)
        last_update = time.time()
    except Exception as e:
        print("load devices error:", e)

    return devices_cache


@app.route('/')
def home():
    return "server running v2"


@app.route('/license', methods=['GET', 'POST'])
def license_api():

    # 👉 浏览器测试用
    if request.method == 'GET':
        return "use POST"

    data = request.json
    if not data or "device_id" not in data:
        return jsonify({"status": "error"}), 400

    device_id = data.get("device_id")

    devices = load_devices()

    # ❗ 白名单校验
    if device_id not in devices:
        return jsonify({
            "status": "denied",
            "msg": "device not registered"
        }), 403

    # ✔ 合法 → 生成 hash
    payload = device_id + SECRET
    hash_val = hashlib.md5(payload.encode()).hexdigest()

    return jsonify({
        "status": "ok",
        "hash": hash_val
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
