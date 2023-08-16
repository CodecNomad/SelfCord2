import inspect
from typing import Optional
import asyncio
from .utils import Command, CommandCollection, BotException
from .api import DiscordHttp, Gateway
from .models import Capabilities, Client


class Bot:
    def __init__(self, prefixes: list[str], debug: bool = False, userbot: bool = False):
        self.http: DiscordHttp = DiscordHttp()
        self.capabilities: Capabilities = Capabilities.default()
        self.gateway: Gateway = Gateway(self, self.capabilities)
        self.prefixes: list[str] = prefixes
        self.debug: bool = debug
        self.userbot: bool = userbot
        self.commands = CommandCollection()
        self.token: Optional[str] = None
        self.user: Optional[Client] = None

    def cmd(self, description="", aliases=None):
        """Decorator to add commands for the bot

        Args:
            description (str, optional): Description of command. Defaults to "".
            aliases (list, optional): Alternative names for command. Defaults to [].

        Raises:
            RuntimeWarning: If you suck and don't use a coroutine
        """
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
                self.user = Client(data)
                await self.gateway.start(token)
            except KeyboardInterrupt:
                await self.http.close()
                await self.gateway.close()

        asyncio.run(runner())
