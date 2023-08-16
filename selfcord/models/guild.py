from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..bot import Bot
    from .users import User


class Guild:
    def __init__(self, bot: Bot, payload: dict):
        self.bot = Bot
        self.http = bot.http

    def _update(self, payload: dict):
        self.id = payload.get("id")
        self.name = payload.get("name")
        self.icon = payload.get("icon")
        self.description = payload.get("description")
        self.owner = User(self.bot.fetch_user(payload.get("owner_id")))
        self.roles = [] #TODO: create role class
        self.vanity = payload.get("vanity_url_code")
        self.max_members = payload.get("max_members")
        self.filter = payload.get("explicit_content_filter")
        self.nsfw = payload.get("nsfw")
        self.nsfw_level = payload.get("nsfw_level")
        self.stickers = [] #TODO: create sticker class
        self.updates_channel = Channel(payload.get("public_updates_channel")) #TODO: create channel class
        self.region = payload.get("region") #maybe should we have a region class?