from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

SECRET = "X9@kLm!123"

@app.route('/license', methods=['POST'])
def license_api():
    data = request.json
    device_id = data.get("device_id", "")

    payload = device_id + SECRET
    hash_val = hashlib.md5(payload.encode()).hexdigest()

    return jsonify({
        "status": "ok",
        "hash": hash_val
    })

# Render 必须绑定这个端口
import os
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)




