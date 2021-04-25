# (c) @AbirHasan2005

import datetime
from pyrogram import (
    Client,
    __version__
)
from . import (
    API_HASH,
    API_ID,
    SESSION_NAME,
    BOT_TOKEN
)
from bot.user import User

class Bot(Client):
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            SESSION_NAME,
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={
                "root": "bot/plugins"
            },
            workers=4,
            bot_token=BOT_TOKEN
        )

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.set_parse_mode("markdown")
        print(f"@{usr_bot_me.username} based on Pyrogram v{__version__} ")
        self.USER, self.USER_ID = await User().start()
        await self.USER.send_message(usr_bot_me.username, f"@{SESSION_NAME} Restarted!")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")
