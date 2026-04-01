from flask import Flask, request, jsonify
import hashlib
import os
import json

app = Flask(__name__)

SECRET = os.environ.get("SECRET", "X9@kLm!123")

# 👉 白名单文件
DB_FILE = "devices.json"


def load_devices():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return set(json.load(f))
    return set()


devices = load_devices()


@app.route('/')
def home():
    return "server running"


@app.route('/license', methods=['POST'])
def license_api():
    data = request.json
    device_id = data.get("device_id", "")

    if not device_id:
        return jsonify({"status": "error"}), 400

    # ❗ 关键：必须在白名单
    if device_id not in devices:
        return jsonify({
            "status": "denied",
            "msg": "device not registered"
        }), 403

    # ✔ 合法设备 → 返回授权
    payload = device_id + SECRET
    hash_val = hashlib.md5(payload.encode()).hexdigest()

    return jsonify({
        "status": "ok",
        "hash": hash_val
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
