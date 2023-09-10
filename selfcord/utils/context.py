from __future__ import annotations
from typing import Optional, Callable, Any, TYPE_CHECKING
import re
import shlex
from traceback import format_exception

if TYPE_CHECKING:
    from ..models import Message, Guild, User, Client, Member, Messageable


# FUCK IT WE SKID (from my own module so it doesn't count!)
class Context:
    """Context related for commands, and invocation"""

    def __init__(self, message, bot) -> None:
        self.message = message
        self.bot = bot

    @property
    def author(self) -> User:
        return self.message.author

    @property
    def guild(self) -> Guild:
        return self.message.guild

    @property
    def channel(self) -> Messageable:
        return self.message.channel

    @property
    def content(self) -> str:
        return self.message.content

    @property
    def command(self) -> Optional[Callable]:
        if self.prefix is None:
            return None
        for command in self.bot.commands:
            for alias in command.aliases:
                if self.content.lower().startswith(self.prefix + alias):
                    return command
        # No extensions yet

        # for extension in self.bot.extensions:
        #     for command in extension.commands:
        #         for alias in command.aliases:
        #             if self.content.lower().split(" ")[0] == self.prefix + alias:
        #                 self.extension = extension.ext
        #                 return command
        return None

    @property
    def alias(self) -> Optional[str]:
        for command in self.bot.commands:
            for alias in command.aliases:
                if self.content.lower().startswith(self.prefix + alias.lower()):
                    return alias

        # No extensions yet

        # for extension in self.bot.extensions:
        #     for command in extension.commands:
        #         for alias in command.aliases:
        #             if self.content.lower().startswith(self.prefix + alias.lower()):
        #                 self.extension = extension.ext
        #                 return alias
        return None

    @property
    def prefix(self) -> Optional[str]:
        for prefix in self.bot.prefixes:
            if self.content.startswith(prefix):
                return prefix

    @property
    def command_content(self) -> Optional[str]:
        """The content minus the prefix and command name, essentially the args

        Returns:
            str: String of content
        """
        if self.alias is None:
            return
        try:
            cut = len(self.prefix + self.alias)
            return self.content[cut:]
        except:
            return None

    def get_converter(self, param) -> Optional[str | Any]:
        if param.annotation is param.empty:
            return str
        if callable(param.annotation):
            return param.annotation

    async def convert(self, param, value) -> Any:
        """Attempts to turn x value in y value, using get_converter func for the values

        Args:
            param (_type_): function parameter
            value (_type_): value in message

        Returns:
            Type[str]: The type of parameter
        """
        from ..models import User

        converter = self.get_converter(param)
        if converter is User:
            # I can probably optimise to not use regex
            id = re.findall(r"[0-9]{18,19}", value)
            if len(id) > 0:
                user = await self.bot.get_user(id[0])
                return user
        return converter(value)

    # Cyclomatic complexity too high - Normdev This is FOR you
    async def get_arguments(self) -> tuple[list, dict]:
        """Get arguments by checking function arguments and comparing to arguments in message.

        Returns:
            _type_: _description_
        """
        args: list[Any] = []
        kwargs: dict[Any, Any] = {}

        if self.command.signature is not None:
            signature = self.command.signature
        if self.command_content == "":
            return args, kwargs
        if self.command_content is None:
            return args, kwargs
        sh = shlex.shlex(self.command_content[1:], posix=False)
        sh.whitespace = " "
        sh.whitespace_split = True
        splitted = list(sh)

        # I used enumerate here, lsp says i dont need it, reminder because idfk what I used it for
        for name, param in signature:
            # Ok because I am so pro coder I somehow passed ctx in without even using ctx
            if name in ["ctx", "self"]:
                continue

            if param.kind is param.POSITIONAL_OR_KEYWORD:
                try:
                    arg: str | Any = await self.convert(param, splitted.pop(0))
                    args.append(arg)
                except Exception as e:
                    print(e)
            if param.kind is param.VAR_KEYWORD:
                for arg in splitted:
                    arg = await self.convert(param, arg)
                    args.append(arg)
            if param.kind is param.VAR_POSITIONAL:
                for arg in splitted:
                    arg = await self.convert(param, arg)
                    args.append(arg)

            if param.kind is param.KEYWORD_ONLY:
                arg = await self.convert(param, " ".join(splitted))
                kwargs[name] = arg

        for key in kwargs.copy():
            if not kwargs[key]:
                kwargs.pop(key)

        return args, kwargs

    async def invoke(self):
        """Used to actually run the command"""
        if self.command is None:
            return
        if not self.bot.userbot:
            if self.message.author.id != self.bot.user.id:
                return
        if self.command_content is not None:
            args, kwargs = await self.get_arguments()
            func = self.command.func
            args.insert(0, self)
            # No extensions yet

            # if func.__code__.co_varnames[0] == "self":
            #     args.insert(0, self.extension)
            #     args.insert(1, self)
            # else:
            #     args.insert(0, self)

        await func(*args, **kwargs)
