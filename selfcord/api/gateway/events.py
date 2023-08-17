from ...models import Guild
class Handler:
    def __init__(self, bot) -> None:
        self.bot = bot

    async def handle_ready(self, data: dict):
        guilds = data.get("guilds")
        if guilds:
            for guild in guilds:
                
                # TODO: We'll actually just make sure guild.py loads this shit correctly
                properties = guild.get("properties")  # TODO: This is where guild attributes are loaded from
                emojis = guild.get("emojis")
                roles = guild.get("roles")
                for role in roles:
                    # TODO: Instantiate Roles for the particular guild
                    pass

    async def handle_ready_supplemental(self, data: dict):
        pass

    async def handle_message_create(self, data: dict):
        pass

    async def handle_message_delete(self, data: dict):
        pass

    

