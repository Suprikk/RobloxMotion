"""
WebSocket Relay Server
Jembatan antara web controller (browser) dan Roblox (HTTP poll)

Cara jalanin:
    pip install websockets flask
    python relay.py

Web controller konek ke: ws://localhost:8765
Roblox poll ke:          http://localhost:5000/pose
"""

import asyncio
import websockets
import json
import threading
from flask import Flask, jsonify

# ===========================
# CONFIG
# ===========================
WS_PORT   = 8765   # port WebSocket (dari browser)
HTTP_PORT = 5000   # port HTTP (dari Roblox)
# ===========================

app = Flask(__name__)

# State terbaru dari web controller
latest_data = {
    "action": "idle",
    "x": 0.0,
    "y": 0.0,
    "z": 0.0,
    "ts": 0
}
data_lock = threading.Lock()

# ===== HTTP endpoint buat Roblox =====
@app.route('/pose', methods=['GET'])
def get_pose():
    with data_lock:
        return jsonify(latest_data.copy())

def run_flask():
    print(f"[HTTP] Flask jalan di http://localhost:{HTTP_PORT}/pose")
    app.run(host='0.0.0.0', port=HTTP_PORT, debug=False, use_reloader=False)

# ===== WebSocket server buat browser =====
async def handle_client(websocket):
    global latest_data
    client_addr = websocket.remote_address
    print(f"[WS] Client konek: {client_addr}")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                with data_lock:
                    latest_data = data
            except json.JSONDecodeError:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        print(f"[WS] Client disconnect: {client_addr}")

async def run_websocket():
    print(f"[WS] WebSocket server jalan di ws://localhost:{WS_PORT}")
    async with websockets.serve(handle_client, "0.0.0.0", WS_PORT):
        await asyncio.Future()  # jalan selamanya

if __name__ == '__main__':
    print("=" * 40)
    print("  Motion Controller Relay Server")
    print("=" * 40)
    print(f"  WebSocket : ws://localhost:{WS_PORT}")
    print(f"  HTTP Poll : http://localhost:{HTTP_PORT}/pose")
    print("=" * 40)

    # Flask di thread terpisah
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # WebSocket di main thread
    asyncio.run(run_websocket())
