
class Handler:
    def __init__(self, bot) -> None:
        self.bot = bot

    async def handle_ready(self, data: dict):
        pass

    async def handle_ready_supplemental(self, data: dict):
        pass

    async def handle_message_create(self, data: dict):
        pass

    async def handle_message_delete(self, data: dict):
        pass

    

