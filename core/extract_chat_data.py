# (c) @AbirHasan2005

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant


async def ExtractChatData(user: Client, bot: Client, message: Message):
    message_ids = list()
    if "https://t.me" not in message.text:
        return
    links = list(filter(lambda s: s.startswith("https://t.me"), message.text.split()))
    chat_id = None
    for link in links:
        message_id = link.split("/")[-1]
        chat_id = link.split("/")[-2]
        message_ids.append(int(message_id))
        if link.split("/")[-3] == "c":
            chat_id = int(f"-100{chat_id}")
    try:
        channel = await bot.get_chat(chat_id)
        my_channel = await bot.get_chat_member(chat_id=channel.id, user_id=(await bot.get_me()).id)
        if (my_channel.can_invite_users is not True) or (my_channel.can_delete_messages is not True) or (my_channel.can_promote_members is not True):
            return 400, None, None
        try:
            await bot.get_chat_member(chat_id=channel.id, user_id=(await user.get_me()).id)
        except UserNotParticipant:
            await user.join_chat(channel.invite_link)
            await bot.promote_chat_member(
                chat_id=channel.id,
                user_id=(await user.get_me()).id,
                can_change_info=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=True,
                can_restrict_members=False,
                can_invite_users=True,
                can_pin_messages=False,
                can_promote_members=False
            )
        return 200, channel.id, message_ids
    except:
        return 400, None, None
