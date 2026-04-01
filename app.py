from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

# 建议在 Render 里设置环境变量 SECRET
SECRET = os.environ.get("SECRET", "X9@kLm!123")


# 首页（用于测试服务是否正常）
@app.route('/')
def home():
    return "server running"


# 授权接口
@app.route('/license', methods=['GET', 'POST'])
def license_api():
    # 👉 浏览器访问用（方便排查）
    if request.method == 'GET':
        return "license endpoint: use POST"

    # 👉 正式逻辑
    data = request.json
    if not data or "device_id" not in data:
        return jsonify({
            "status": "error",
            "msg": "device_id missing"
        }), 400

    device_id = data.get("device_id", "")

    # 生成 hash（授权核心）
    payload = device_id + SECRET
    hash_val = hashlib.md5(payload.encode()).hexdigest()

    return jsonify({
        "status": "ok",
        "hash": hash_val
    })


# Render 需要绑定这个端口
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
