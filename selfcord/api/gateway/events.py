import itertools
from ...models import Guild, Convert, User


class Handler:
    def __init__(self, bot) -> None:
        self.bot = bot

    async def handle_ready(self, data: dict):
        guilds = data.get("guilds")
        private_channels = data.get("private_channels")
        users = data.get("users")
        relationships = data.get("relationship")

        # LOOK AT ALL THIS OPTIMISATION
        for guild, channel, user, relation in itertools.zip_longest(
            guilds if guilds is not None else [],
            private_channels if private_channels is not None else [],
            users if users is not None else [],
            relationships if relationships is not None else [],
        ):
            if guild is not None:
                self.bot.user.guilds.append(Guild(guild, self.bot))
            if channel is not None:
                chan = Convert(channel, self.bot)
                self.bot.user.private_channels.append(chan)
                self.bot.user.cached_channels.append(chan)
            if user is not None:
                check_user = self.bot.fetch_user(user['id'])
                if check_user is None:
                    self.bot.user.cached_users.append(User(user, self.bot))
                else:
                    check_user._update(user)
            if relation is not None:
                check_user = self.bot.fetch_user(relation['id'])
                if check_user is None:
                    relation = User(relation, self.bot)
                    self.bot.user.cached_users.append(relation)
                    if relation['type'] == 1:
                        self.bot.user.friends.append(relation)
                        
                else:
                    check_user._update(user)


    async def handle_ready_supplemental(self, data: dict):
        pass

    async def handle_message_create(self, data: dict):
        pass

    async def handle_message_delete(self, data: dict):
        pass
