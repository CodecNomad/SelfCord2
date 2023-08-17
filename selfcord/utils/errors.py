from __future__ import annotations
from typing import Any, Optional


class SelfcordException(Exception):
    """Base Exception Class"""


class BotException(SelfcordException):
    def __init__(self, message: Optional[str] = None, *args: Any) -> None:
        if message is not None:
            message = message.replace("@everyone", "@\u200beveryone").replace(
                "@here", "@\u200bhere"
            )
        super().__init__(message, args)


class CommandException(SelfcordException):
    def __init__(self, message: Optional[str] = None, *args: Any) -> None:
        if message is not None:
            message = message.replace("@everyone", "@\u200beveryone").replace(
                "@here", "@\u200bhere"
            )
        super().__init__(message, args)
