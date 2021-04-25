# (c) @AbirHasan2005

from pyrogram import (
    Client,
    __version__
)
from . import (
    API_HASH,
    API_ID,
    TG_USER_SESSION
)


class User(Client):
    def __init__(self):
        super().__init__(
            TG_USER_SESSION,
            api_hash=API_HASH,
            api_id=API_ID,
            workers=4
        )

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.set_parse_mode("markdown")
        print(f"@{usr_bot_me.username} based on Pyrogram v{__version__} ")
        return (self, usr_bot_me.id)

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")
