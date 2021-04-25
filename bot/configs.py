# (c) @AbirHasan2005

import os


class Config(object):
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	TG_USER_SESSION = os.environ.get("TG_USER_SESSION")
	ADMIN = int(os.environ.get("ADMIN", 1445283714))
	API_ID = int(os.environ.get("API_ID"))
	API_HASH = os.environ.get("API_HASH")
	DATABASE_URL = os.environ.get("DATABASE_URL")
	LOGS_CHANNEL = int(os.environ.get("LOGS_CHANNEL"))
	UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL")
	START_TEXT = """
Hi [{}](tg://user?id={})
This is Telegram DMCA Messages Delete Bot.

Forward me DMCA Notice Message which has Links of your Telegram Channel Messages, I will try to delete those Files from your Channel.

**Note:** __Don't Forget to first add me to your channel as Admin with Messages Delete Right!__
"""
	HELP_TEXT = """
**How to Use Me?**

> Add me to Channel as Admin with Delete Messages Right.
> Make sure you are Admin in Channel & have Delete Messages Right.
> Forward me DMCA Notice Message.
> Wait Till I Delete Messages 😂

**Tip:** Also you can send a list which has links of messages.

**Note:** __In some case, if your channel is or was private before adding me than I can't delete those broadcasted messages. If need any help ask in [Support Group](https://t.me/linux_repo)!__
"""
	ABOUT_TEXT = """
This is Telegram DMCA Messages Delete Bot.

Forward me DMCA Notice Message which has Links of your Telegram Channel Messages, I will try to delete those Files from your Channel.

🤖 **My Name:** [DMCA Delete Bot](https://t.me/DMCA_DelBot)

📝 **Language:** [Python3](https://www.python.org)

📚 **Library:** [Pyrogram](https://docs.pyrogram.org)

📡 **Hosted on:** [Heroku](https://heroku.com)

🧑🏻‍💻 **Developer:** @AbirHasan2005

💸 **Donate:** [PayPal](https://www.paypal.me/AbirHasan2005)

👥 **Support Group:** [Linux Repositories](https://t.me/linux_repo)

📢 **Updates Channel:** [Discovery Projects](https://t.me/Discovery_Updates)
"""