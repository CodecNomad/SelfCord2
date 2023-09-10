from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .assets import Asset
from .guild import Guild, Role
from .channels import DMChannel, Messageable

if TYPE_CHECKING:
    from ..bot import Bot


base = "https://discord.com/api/v9"

# Realise this might be fucked because my subclassism didn't work with channels
# So basically guys my epic OOP magic didn't work this is indeed fucked
# Time to copy and paste everything! Actually methods should be fine, attrs for some reason don't wanna work


class User:
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self.update(payload)

    def update(self, payload: dict):
        self.name: Optional[str] = payload.get("username")
        self.id: str = payload["id"]  # USER ID STAYS STRING
        self.discriminator: Optional[str] = payload.get("discriminator")
        self.avatar: Optional[Asset] = (
            Asset(self.id, payload["avatar"]).from_avatar()
            if payload.get("avatar") is not None
            else None
        )
        self.banner: Optional[Asset] = (
            Asset(self.id, payload["banner"]).from_avatar()
            if payload.get("banner") is not None
            else None
        )
        self.banner_color: Optional[str] = payload.get("banner_color")
        self.accent_color: Optional[str] = payload.get("accent_color")
        self.display_name: Optional[str] = payload.get("global_name")
        self.flags: Optional[int] = payload.get("flags")
        self.avatar_decoration: Optional[str] = payload.get(
            "avatar_decoration")
        self.is_bot = payload["bot"] if payload.get(
            "bot") is not None else False

    async def friend(self):
        await self.http.request(
            "put", base + "/users/@me/relationships/" + self.id, json={}
        )

    async def block(self):
        await self.http.request(
            "put", base + "/users/@me/relationships/" + self.id, json={"type": 2}
        )

    async def reset_relationship(self):
        await self.http.request(
            "delete", base + "/users/@me/relationships/" + self.id, json={}
        )

    async def create_dm(self) -> DMChannel:
        json = await self.http.request(
            "post", base + "/channels", json={"recipients": [self.id]}
        )
        return DMChannel(json, self.bot)


class Client(User):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self.guilds: list[Guild] = []
        self.friends: list[User] = []
        self.blocked: list[User] = []
        self.private_channels: list[Messageable] = []
        self.cached_users: dict[str, User] = {}
        self.cached_channels: dict[str, Messageable] = {}
        self.cached_messages: dict[str, str] = {}
        self.update(payload)
        super().__init__(payload, bot)

    def update(self, payload: dict):
        self.name: Optional[str] = payload.get("username")
        self.id: str = payload["id"]  # USER ID STAYS STRING
        self.discriminator: Optional[str] = payload.get("discriminator")
        self.avatar: Optional[Asset] = (
            Asset(self.id, payload["avatar"]).from_avatar()
            if payload.get("avatar") is not None
            else None
        )
        self.banner: Optional[Asset] = (
            Asset(self.id, payload["banner"]).from_avatar()
            if payload.get("banner") is not None
            else None
        )
        self.banner_color: Optional[str] = payload.get("banner_color")
        self.accent_color: Optional[str] = payload.get("accent_color")
        self.display_name: Optional[str] = payload.get("global_name")
        self.flags: Optional[int] = payload.get("flags")
        self.avatar_decoration: Optional[str] = payload.get(
            "avatar_decoration")
        self.is_bot = payload["bot"] if payload.get(
            "bot") is not None else False
        self.verified = payload.get("verified")
        self.purchased_flags = payload.get("purchased_flags")
        self.pronouns = payload.get("pronouns")
        self.premium_type = payload.get("premium_type")
        self.phone = payload.get("phone")
        self.nsfw = payload.get("nsfw_allowed")
        self.mobile = payload.get("mobile")
        self.desktop = payload.get("desktop")
        self.mfa = payload.get("mfa_enabled")


class Member(User):
    def __init__(self, payload: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self.roles: list[Role] = []
        self.permissions = 0  # TODO: Create Permission class
        super().__init__(payload, bot)
