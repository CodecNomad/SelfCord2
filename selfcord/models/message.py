from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .users import User, Member

if TYPE_CHECKING:
    from ..bot import Bot

class Message:
    def __init__(self, data: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self.update(data)

    def update(self, payload: dict):
        self.id: str = payload.get("id")
        self.content: str = payload.get("content")
        self.type = payload.get("type", 0)
        self.tts = payload.get("tts")
        self.timestamp = payload.get("timestamp")
        self.replied_message = payload.get("referenced_message")
        self.pinned = payload.get("pinned")
        self.nonce = payload.get("nonce")
        self.mentions = payload.get("mentions")
        self.channel_id = payload.get("channel_id", "")
        self.channel = self.bot.fetch_channel(self.channel_id)
        self.guild_id = payload.get("guild_id", "")
        self.guild = self.bot.fetch_guild(self.guild_id)
        self.author = User(payload.get("author"), self.bot)
        # we will fix later 
        # self.member = Member(payload.get("member"), self.bot)
        self.flags = payload.get("flags", 0)
        # Create associated classes with these
        self.embeds = payload.get("embeds")
        self.components = payload.get("components")
        self.attachments = payload.get("attachments")
