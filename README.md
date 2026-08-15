# Max-Speed Wisp Server (Base44 / BallsProxy Optimized)

This is a high-performance Wisp backend designed for:
- Base44 engines
- BallsProxy
- YouTube playback
- High-speed binary tunneling

## Features
- Wisp handshake
- Binary frames
- HTTP tunneling (OP_HTTP)
- Range request support
- Chunked streaming
- uvloop acceleration

## Deploy on Railway
1. Push this repo to GitHub
2. Create a new Railway project
3. Select "Deploy from GitHub"
4. Set start command:
   python wisp_maxspeed.py

Your Wisp endpoint will be:
wss://<your-app>.railway.app
