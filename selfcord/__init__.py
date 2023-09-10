from .bot import Bot
from .utils import Command, CommandCollection, BotException, CommandException, Context
from .models import User, Client, Member
from .api import gateway, DiscordHttp

import sentry_sdk

sentry_sdk.init(
    dsn="https://c950f70061673a46dccf5127e4fc38e6@o4505725812473856.ingest.sentry.io/4505725836787712",
    traces_sample_rate=1.0,
)
