from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .assets import Asset

if TYPE_CHECKING:
    from ..bot import Bot


class User:
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self._update(payload)

    def _update(self, payload: dict):
        self.name: Optional[str] = payload.get("username")
        self.id: int = payload['id']
        self.discriminator: Optional[str] = payload.get("discriminator")
        self.avatar: Optional[Asset] = (
            Asset(self.id, payload['avatar'])
            if payload.get("avatar") is not None
            else None
        )
        self.banner: Optional[Asset] = (
            Asset(self.id, payload['banner'])
            if payload.get("banner") is not None
            else None
        )
        self.banner_color: Optional[str] = payload.get("banner_color")
        self.accent_color: Optional[str] = payload.get("accent_color")
        self.display_name: Optional[str] = payload.get("global_name")
        self.avatar_decoration: Optional[str] = payload.get("avatar_decoration")
        self.is_bot = (
            payload['bot']
            if payload.get('bot') is not None
            else False
        )

    # TODO: when http is correctly made I will add methods


class Client(User):
    def __init__(self, payload: dict, bot: Bot):
        super().__init__(payload, bot)


class Member(User):
    def __init__(self, payload: dict, bot: Bot):
        super().__init__(payload, bot)
