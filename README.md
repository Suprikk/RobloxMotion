# Roblox Head Motion Controller

Kontrol karakter Roblox pake gerakan kepala — tanpa install apapun, cukup buka browser.

## Demo

Gerakin kepala kiri/kanan/atas/bawah → karakter Roblox ikut bergerak real-time.

## Cara Kerja

```
Browser (controller.html)
    ↓ MediaPipe detect kepala
    ↓ WebSocket kirim aksi
relay.py (jalan di PC lo)
    ↓ HTTP endpoint
Roblox (HttpService poll)
    ↓
Karakter bergerak
```

## File Structure

```
├── controller.html     — Web controller (buka di browser)
├── relay.py            — WebSocket + HTTP relay server
├── roblox/
│   ├── PoseReceiver.lua       — ServerScript (ServerScriptService)
│   └── PoseReceiverLocal.lua  — LocalScript (StarterPlayerScripts)
└── README.md
```

## Setup

### 1. Install dependencies Python

```bash
pip install websockets flask
```

### 2. Jalanin relay server

```bash
python relay.py
```

### 3. Setup Roblox Studio

- Copy `PoseReceiver.lua` ke **ServerScriptService** (sebagai Script)
- Copy `PoseReceiverLocal.lua` ke **StarterPlayer > StarterPlayerScripts** (sebagai LocalScript)
- Aktifin **HttpService**: Game Settings → Security → Allow HTTP Requests → ON
- Bikin **RemoteFunction** bernama `GetPoseData` di ReplicatedStorage (atau biarkan script yang bikin otomatis)

### 4. Buka web controller

```
http://localhost:8080/controller.html
```

Atau hosting ke GitHub Pages dan buka dari sana.

### 5. Pilih kamera dan mulai

- Klik **Refresh** untuk detect kamera
- Pilih kamera yang mau dipake
- Klik **Mulai**
- Konek ke `ws://localhost:8765`
- Playtest di Studio

## Kontrol

| Gerakan Kepala | Aksi Karakter |
|---|---|
| Kepala ke kiri | Geser kiri |
| Kepala ke kanan | Geser kanan |
| Kepala naik | Lompat |
| Kepala turun | Jongkok |
| Diam di tengah | Idle |

## Config

### Web Controller (`controller.html`)
```javascript
const THRESHOLD_X  = 0.06   // sensitivitas kiri/kanan
const THRESHOLD_Y  = 0.05   // sensitivitas atas/bawah
const DEAD_ZONE    = 0.02   // zona tengah = idle
const SEND_RATE_MS = 50     // frekuensi kirim data (ms)
```

### Relay Server (`relay.py`)
```python
WS_PORT   = 8765   // port WebSocket
HTTP_PORT = 5000   // port HTTP untuk Roblox
```

### Roblox LocalScript
```lua
local LERP         = 0.15   -- smoothing gerakan
local MOVE_SPEED   = 0.5    -- kecepatan geser kiri/kanan
local JUMP_COOLDOWN = 1.0   -- cooldown lompat (detik)
```

## Notes

- Web controller butuh HTTPS atau localhost untuk akses kamera
- Kalau pake GitHub Pages, relay server harus punya WSS (WebSocket Secure)
- DroidCam: konek HP ke PC via USB/WiFi dulu baru buka controller.html
