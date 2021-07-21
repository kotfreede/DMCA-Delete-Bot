# (c) @AbirHasan2005

import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait

from configs import Config


async def DeleteMessages(client: Client, chat_id: int, message_ids: list):
    try:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=message_ids,
            revoke=True
        )
        await client.send_message(
            chat_id=Config.LOGS_CHANNEL,
            text=f"#DMCA_DELETE:\n"
                 f"Deleted {str(len(message_ids))} Messages from {str(chat_id)} !!"
        )
        return 200, None
    except FloodWait as e:
        print(f"Sleeping for {e.x}s ...")
        await asyncio.sleep(e.x)
        await DeleteMessages(client, chat_id, message_ids)
    except Exception as err:
        return 400, err
