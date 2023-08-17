from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Self
from .users import User
from .assets import Asset
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
        self.flags = payload.get("flags")


    


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
        self.icon: Optional[Asset] = (
            Asset(self.id, payload['icon']).from_icon()
            if payload.get("icon") is not None
            else None
        )
        self.name: Optional[str] = payload.get("name")
        self.last_pin_timestamp: Optional[int] = payload.get("last_pin_timestamp")


class TextChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.category_id = payload.get("parent_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class VoiceChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.category_id = payload.get("category_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class Category(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class Announcement(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class AnnouncementThread(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class PublicThread(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class PrivateThread(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class StageChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class Directory(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class ForumChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")


class MediaChannel(Messageable):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)
        super().__init__(payload, bot)

    def _update(self, payload):
        self.guild_id = payload.get("guild_id")
        self.position = payload.get("position")
        self.permission_overwrites = payload.get("permission_overwrites")
