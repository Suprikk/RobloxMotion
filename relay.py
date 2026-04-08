"""
WebSocket + HTTP Relay Server
Railway: WebSocket dan HTTP jalan di PORT yang sama
"""

import asyncio
import websockets
import json
import os
import threading
from flask import Flask, jsonify, request
from websockets.server import serve

PORT = int(os.environ.get('PORT', 8765))

app = Flask(__name__)

latest_data = {"action": "idle", "x": 0.0, "y": 0.0, "z": 0.0, "ts": 0}
data_lock = threading.Lock()

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/')
def index():
    with data_lock:
        return jsonify({"status": "RobloxMotion relay running", "action": latest_data.get("action", "idle")})

@app.route('/pose')
def get_pose():
    with data_lock:
        return jsonify(latest_data.copy())

connected_clients = set()

async def ws_handler(websocket):
    connected_clients.add(websocket)
    print(f"[WS] Client konek | Total: {len(connected_clients)}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                with data_lock:
                    latest_data.update(data)
            except Exception:
                pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"[WS] Client disconnect | Total: {len(connected_clients)}")

def run_flask():
    # Flask di port terpisah buat local testing
    http_port = PORT + 1 if os.environ.get('RAILWAY_ENVIRONMENT') else 5000
    print(f"[HTTP] Flask di http://0.0.0.0:{http_port}/pose")
    app.run(host='0.0.0.0', port=http_port, debug=False, use_reloader=False)

async def run_ws():
    print(f"[WS] WebSocket di ws://0.0.0.0:{PORT}")
    async with serve(ws_handler, "0.0.0.0", PORT, ping_interval=20, ping_timeout=10):
        await asyncio.Future()

async def main():
    is_railway = bool(os.environ.get('RAILWAY_ENVIRONMENT'))
    print("=" * 45)
    print("  RobloxMotion Relay Server")
    print(f"  PORT     : {PORT}")
    print(f"  Railway  : {is_railway}")
    print("=" * 45)

    if not is_railway:
        # Local: Flask di thread terpisah, WS di main
        threading.Thread(target=run_flask, daemon=True).start()

    await run_ws()

if __name__ == '__main__':
    asyncio.run(main())
