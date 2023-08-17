from ...models import Guild


class Handler:
    def __init__(self, bot) -> None:
        self.bot = bot

    async def handle_ready(self, data: dict):
        guilds = data.get("guilds")
        if guilds:
            for guild in guilds:
                self.bot.user.guilds.append(Guild(guild, self.bot))


            print(len(self.bot.user.guilds))
            for guild in self.bot.user.guilds:
                print(guild.name)
                print(len(guild.emojis))
                print(len(guild.stickers))
                print(len(guild.roles))

    async def handle_ready_supplemental(self, data: dict):
        pass

    async def handle_message_create(self, data: dict):
        pass

    async def handle_message_delete(self, data: dict):
        pass
