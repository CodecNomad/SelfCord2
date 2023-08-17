from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from .users import User
import random

if TYPE_CHECKING:
    from ..bot import Bot
    from ..api import DiscordHttp


class Messageable:
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.http: DiscordHttp = bot.http
        self.id: int
        self.guild_id: int
        self.type: int

    @property
    def nonce(self) -> int:
        return random.randint(100000, 99999999)

    async def send(
        self, content: str, files: Optional[list[str]] = None, tts: bool = False
    ):
        if self.type == 1 or self.type == 3:
            headers = {
                "referer": f"https://canary.discord.com/channels/@me/{self.id}"}
        else:
            headers = {
                "referer": f"https://canary.discord.com/channels/{self.guild_id}/{self.id}"
            }
        await self.http.request(
            "POST",
            f"/channels/{self.id}/messages",
            headers=headers,
            json={"content": content, "flags": 0,
                  "tts": tts, "nonce": self.nonce},
        )


class DMChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(bot)

    def _update(self, payload: dict):
        self.type: int = 1
        self.recipient: Optional[User] = self.bot.fetch_user(
            payload["recipients"][0])
        self.last_message_id: Optional[int] = payload.get("last_message_id")
        self.is_spam: Optional[bool] = payload.get("is_spam")
        self.id: int = int(payload["id"])


class GroupChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(bot)

    def _update(self, payload: dict):
        self.type: int = 1
        self.recipient: list[Optional[User]] = [
            self.bot.fetch_user(user) for user in payload["recipients"]
        ]
        self.last_message_id: Optional[int] = payload.get("last_message_id")
        self.is_spam: Optional[bool] = payload.get("is_spam")
        self.id: int = int(payload["id"])
