import inspect
from typing import Optional
import asyncio
from .utils import Command, CommandCollection, BotException
from .api import discord_http, gateway
from .models import Client

class Bot:
    def __init__(self, prefixes: list[str], debug: bool = False, userbot: bool = False):
        self.http: discord_http = discord_http()
        self.gateway: Gateway = Gateway(self)
        self.prefixes: list[str] = prefixes
        self.debug: bool = debug
        self.userbot: bool = userbot
        self.commands = CommandCollection()
        self.token: Optional[str] = None
        self.user: Optional[Client] = None

    def cmd(self, description="", aliases=[]):
        """Decorator to add commands for the bot

        Args:
            description (str, optional): Description of command. Defaults to "".
            aliases (list, optional): Alternative names for command. Defaults to [].

        Raises:
            RuntimeWarning: If you suck and don't use a coroutine
        """
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
            data = await self.http.static_login(token)
            self.user = Client(data)
            await self.gateway.start(token)

        asyncio.run(runner())



