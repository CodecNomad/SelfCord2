from __future__ import annotations
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from ..bot import Bot

class Message:
    def __init__(self, data: dict, bot: Bot):
        self.bot = bot
        self.http = bot.http
        self.update(data)
