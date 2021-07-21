# (c) @AbirHasan2005

from configs import Config
from core.database.database import Database

db = Database(Config.MONGO_DB_URI, Config.TG_BOT_SESSION)
