
class User:
    def __init__(self, payload: dict):

        self.name = payload['name']
        self.id = payload['id']
        self.discriminator = payload['discriminator']
        self.avatar = payload['avatar']
        self.banner = payload['banner']
        self.banner_color = payload['banner_color']
        self.accent_color = payload['accent_color']
        self.display_name = payload['global_name']
        self.avatar_decoration = payload['avatar_decoration']
        self.is_bot = payload['bot']


    # TODO: when http is correctly made I will add methods
