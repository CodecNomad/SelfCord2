from __future__ import annotations
import inspect
from typing import TYPE_CHECKING, Optional
import asyncio
from .utils import Command, CommandCollection, BotException
from .api import DiscordHttp, Gateway
from .models import Capabilities, Client, User, Messageable


class Bot:
    def __init__(self, prefixes: list[str], debug: bool = False, userbot: bool = False):
        self.http: DiscordHttp = DiscordHttp(self)
        self.capabilities: Capabilities = Capabilities.default()
        self.gateway: Gateway = Gateway(self)
        self.prefixes: list[str] = prefixes
        self.debug: bool = debug
        self.userbot: bool = userbot
        self.commands = CommandCollection()
        self.token: Optional[str] = None
        self.user: Optional[Client] = None

    def cmd(self, description: str = "", aliases: Optional[list[str]] = None):
        if aliases is None:
            aliases = []
        if isinstance(aliases, str):
            aliases = [aliases]

        def decorator(coro):
            name = coro.__name__
            if not inspect.iscoroutinefunction(coro):
                raise BotException("Not a coroutine")
            cmd = Command(
                name=name, description=description, aliases=aliases, func=coro
            )
            self.commands.add(cmd)
            return cmd

        return decorator

    def run(self, token: str):
        async def runner():
            try:
                data = await self.http.static_login(token)
                self.user = Client(data, self)
                await self.gateway.start(token)
            except KeyboardInterrupt:
                await self.logout()

        asyncio.run(runner())

    async def logout(self):
        await self.http.close()
        await self.gateway.close()

    def fetch_user(self, user_id: str) -> Optional[User]:
        if self.user:
            return self.user.cached_users.get(user_id)
        return None

    def fetch_channel(self, channel_id: str) -> Optional[Messageable]:
        if self.user:
            return self.user.cached_channels.get(channel_id)
        return None
