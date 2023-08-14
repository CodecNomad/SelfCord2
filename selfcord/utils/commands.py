import inspect
from typing import Callable, Any, Optional
from ..errors import CommandException

class Command:
    """Command Object pretty much"""

    def __init__(self, **kwargs):
        self.name: Optional[str] = kwargs.get("name")
        self.aliases: Optional[list[str]] = [self.name] + kwargs.get("aliases", [])
        self.description: Optional[str] = kwargs.get("description")
        self.func: Callable = kwargs['func']
        self.check: Any = inspect.signature(self.func).return_annotation
        self.signature: Any = inspect.signature(self.func).parameters.items()


class CommandCollection:
    """Commands collection, where commands are stored into. Utilised for help commands and general command invocation."""

    def __init__(self, **kwargs):
        self.commands: dict[Command, Callable] = {}
        self.recent_commands: dict[Command, Callable] = {}

    def __len__(self):
        return len(self.commands)

    def __iter__(self):
        yield from self.commands.values()

    def _is_already_registered(self, cmd: Command) -> bool:
        """Whether the specified Command is already registered

        Args:
            cmd (Command): Command to check

        Returns:
            bool: True or False
        """
        for command in self.commands.values():
            for alias in cmd.aliases:
                return alias in command.aliases
        return False

    def append(self, collection):
        """Append to commands, and recent_commands

        Args:
            collection (CommandCollection): Collection instance

        Raises:
            ValueError: Collection must be subclass of CommandCollection
        """
        if not isinstance(collection, CommandCollection):
            raise RuntimeError(
                "Collection is not a subclass of CommandCollection"
            )
        for item in collection:
            self.commands[item.name] = item
            self.recent_commands[item.name] = item

    def add(self, cmd: Command):
        """Add a Command to the collection

        Args:
            cmd (Command): Command to be added

        Raises:
            ValueError: cmd must be a subclass of Command
            ValueError: Name or Alias is already registered
        """
        if not isinstance(cmd, Command):
            raise CommandException("cmd is not a subclass of Command")
        if self._is_already_registered(cmd):
            raise CommandException(
                "Command Name or Alias is already registered"
            )
        self.commands[cmd.name] = cmd
        self.recent_commands[cmd.name] = cmd

    def recents(self):
        """View commands recently acquired

        Yields:
            Generator: [Command]
        """
        yield from self.recent_commands.values()

    def copy(self):
        """Copy commands from recents to main collection"""
        self.commands.update(self.recent_commands)
        self.clear()

    def clear(self):
        """Clear recents"""
        self.recent_commands.clear()

    def get(self, alias) -> Optional[Command]:
        """Get a specific command from the collection

        Args:
            alias (str): Name of the command

        Returns:
            Command: Command obtained
        """
        for command in self.commands:
            if alias in command.aliases:
                return command
