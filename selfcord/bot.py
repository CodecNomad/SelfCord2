from __future__ import annotations
import inspect
from typing import TYPE_CHECKING, Optional
import asyncio
from .utils import Command, CommandCollection, BotException
from .api import DiscordHttp, Gateway
from .models import Capabilities, Client, User


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

    def fetch_user(self, user_id: int) -> Optional[User]:
        if self.user:
            for user in self.user.cached_users:
                if user.id == user_id:
                    return user
        return None
