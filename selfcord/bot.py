import inspect
from .errors import BotException
from .utils import Command, CommandCollection


class Bot:
    def __init__(self, prefixes: list[str], debug: bool = False, userbot: bool = False):
        self.prefixes = prefixes
        self.debug = debug
        self.userbot = userbot
        self.commands = CommandCollection

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
