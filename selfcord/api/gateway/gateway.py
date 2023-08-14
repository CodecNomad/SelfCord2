from __future__ import annotations
from typing import TYPE_CHECKING
from zlib import decompressobj
import time
import asyncio

import websockets
import ujson

if TYPE_CHECKING:
    from websockets import Request
    from zlib import _Decompress


class gateway:

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE = 3
    VOICE_STATE = 4
    VOICE_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALIDATE_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    GUILD_SYNC = 12

    def __init__(self, token: str) -> None:
        self.token: str = token
        self.url = ("wss://gateway.discord.gg/"
                    "?encoding=json&v=9&compress=zlib-stream")
        self.zlib: _Decompress = decompressobj()
        self.zlib_suffix: bytes = b"\x00\x00\xff\xff"
        self.latency = float("inf")

    async def send_json(self, payload: dict):
        await self.ws.send(ujson.dumps(payload))

    async def recv_json(self):
        item = await self.ws.recv()
        buffer = bytearray()
        buffer.extend(item)
        if len(item) < 4 or item[-4:] != self.zlib_suffix:
            return
        if item:
            op = item['op']
            data = item['d']
            event = item['t']

            if op == self.HELLO:
                interval = data["heartbeat_interval"] / 1000.0
                await self.identify()
                asyncio.create_task(self.heartbeat(interval))

            elif op == self.HEARTBEAT_ACK:
                self.heartbeat_ack()



    async def connect(self):
        self.ws = websockets.connect(self.url,
                                     origin="https://discord.com",
                                     max_size=None)

    async def identify(self):
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "client_state": {
                    "api_code_version": 0,
                    "highest_last_message_id": "0",
                    "initial_guild_id": None,
                    "private_channels_version": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1,
                },
                "compress": False,
                "presence": {
                    "activities": [],
                    "afk": False,
                    "since": 0,
                    "status": "dnd"
                },
                "properties": {
                    "os": "Android",
                    "browser": "Discord Android",
                    "device": "Discord Android",
                    "browser_useragent": ("Mozilla/5.0 (X11; Linux x86_64)"
                                          "AppleWebKit/537.36 "
                                          "(KHTML, like Gecko) "
                                          "discord/0.0.157 "
                                          "Chrome/108.0.5359.215 "
                                          "Electron/22.3.2 "
                                          "Safari/537.36"),
                    "system-locale": "en-GB",
                    "os_arch": "x64"
                },
            },
        }
        await self.send_json(payload)

    async def heartbeat(self, interval: int):
        heartbeatJSON = {"op": 1, "d": time.time()}
        while True:
            await asyncio.sleep(interval)
            await self.send_json(heartbeatJSON)
            self.last_send = time.perf_counter()

    def heartbeat_ack(self):
        self.last_ack = time.perf_counter()
        self.latency = self.last_ack - self.last_send

    async def call(self, channel: str, guild: str | None =None):
        payload = {
            "op": 4,
            "d": {
                "guild_id": guild,
                "channel_id": channel,
                "preferred_region": "rotterdam",
                "self_mute": False,
                "self_deaf": False,
                "self_video": False,
            },
        }
        await self.send_json(payload)

    async def leave_call(self):
        payload = {
            "op": 4,
            "d": {
                "guild_id": None,
                "channel_id": None,
                "self_mute": False,
                "self_deaf": False,
                "self_video": False,
            },
        }
        await self.send_json(payload)
