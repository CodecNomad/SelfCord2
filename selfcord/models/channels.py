from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from .users import User
import random

if TYPE_CHECKING:
    from ..bot import Bot
    from ..api import DiscordHttp


class Channel:
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)

    def _update(self, payload: dict):
        self.id: int = int(payload["id"])
        self.type: int = int(payload["type"])


class Messageable(Channel):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self.id: int
        self.guild_id: int
        self.type: int
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload: dict):
        self.last_message_id: Optional[int] = payload.get("last_message_id")

    @property
    def nonce(self) -> int:
        return random.randint(100000, 99999999)

    async def send(
        self, content: str, files: Optional[list[str]] = None, tts: bool = False
    ):
        if self.type in (1, 3):
            headers = {"referer": f"https://canary.discord.com/channels/@me/{self.id}"}
        else:
            headers = {
                "referer": f"https://canary.discord.com/channels/{self.guild_id}/{self.id}"
            }
        await self.http.request(
            "POST",
            f"/channels/{self.id}/messages",
            headers=headers,
            json={"content": content, "flags": 0, "tts": tts, "nonce": self.nonce},
        )


class DMChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload: dict):
        self.recipient: Optional[User] = self.bot.fetch_user(payload["recipients"][0])

        self.is_spam: Optional[bool] = payload.get("is_spam")


class GroupChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload: dict):
        self.recipient: list[Optional[User]] = [
            self.bot.fetch_user(user) for user in payload["recipients"]
        ]
        self.is_spam: Optional[bool] = payload.get("is_spam")
