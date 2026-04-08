import asyncio, json, os
from aiohttp import web
import aiohttp

PORT = int(os.environ.get('PORT', 8765))
latest_data = {"action": "idle", "x": 0.0, "y": 0.0, "z": 0.0, "ts": 0}
connected = set()

async def handle_root(request):
    return web.json_response({"status": "ok", "action": latest_data.get("action")})

async def handle_pose(request):
    return web.json_response(latest_data)

async def handle_ws(request):
    ws = web.WebSocketResponse(heartbeat=20)
    await ws.prepare(request)
    connected.add(ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            try: latest_data.update(json.loads(msg.data))
            except: pass
    connected.discard(ws)
    return ws

async def main():
    app = web.Application()
    app.router.add_get('/', handle_root)
    app.router.add_get('/pose', handle_pose)
    app.router.add_get('/ws', handle_ws)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', PORT).start()
    print(f"Relay jalan di PORT {PORT}")
    await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
