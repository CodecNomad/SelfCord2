import websockets
import ujson


class gateway:
    def __init__(self) -> None:
        # YOU WANTED ME TO FOLLOW BEST PRACTICE (E501)
        self.url = ("wss://gateway.discord.gg/"
                    "?encoding=json&v=9&compress=zlib-stream")

    async def connect(self):
        self.ws = websockets.connect(self.url,
                                     origin="https://discord.com")


