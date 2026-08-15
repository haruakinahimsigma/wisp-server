import os
import asyncio
import aiohttp
import websockets
import uvloop

uvloop.install()

OP_HANDSHAKE = 0x01
OP_DATA = 0x02
OP_PING = 0x03
OP_PONG = 0x04
OP_HTTP = 0x05

async def fetch_upstream(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            async for chunk in resp.content.iter_chunked(16384):
                yield chunk

async def handle_wisp(ws):
    await ws.send(bytes([OP_HANDSHAKE]) + b"WISP/1.0")

    while True:
        frame = await ws.recv()
        if isinstance(frame, str):
            frame = frame.encode()

        opcode = frame[0]
        payload = frame[1:]

        if opcode == OP_PING:
            await ws.send(bytes([OP_PONG]) + payload)
            continue

        if opcode == OP_HTTP:
            try:
                url, headers_raw = payload.split(b"\0", 1)
                url = url.decode()
                headers = {}

                if headers_raw:
                    import json
                    headers = json.loads(headers_raw.decode())

                async for chunk in fetch_upstream(url, headers):
                    await ws.send(bytes([OP_DATA]) + chunk)

            except Exception:
                await ws.send(bytes([OP_DATA]) + b"")
            continue

        if opcode == OP_DATA:
            await ws.send(bytes([OP_DATA]) + payload)

async def main():
    port = int(os.environ.get("PORT", 8000))
    async with websockets.serve(handle_wisp, "0.0.0.0", port, max_size=None):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
