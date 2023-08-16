from __future__ import annotations

class Asset:
    def __init__(self, id: int, hash: str) -> None:
        self._update(id, hash)

    def _update(self, id: int, hash: str):
        self.id = id
        self.hash = hash
        self.url: str = f"https://cdn.discordapp.com/avatars/{self.id}/{self.hash}.png?size=4096"
        if self.hash.startswith("a_"):
            self.url: str = f"https://cdn.discordapp.com/avatars/{self.id}/{self.hash}.gif?size=4096"

    def __str__(self) -> str:
        return self.url

    @property
    def is_animated(self):
        if self.hash.startswith("a_"):
            return True
        return False

