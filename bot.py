# (c) @AbirHasan2005

from configs import Config
from core.database.add_user import AddUserToDatabase
from core.database.access_db import db
from core.forcesub import ForceSub
from core.extract_chat_data import ExtractChatData
from core.delete_messages import DeleteMessages
from core.broadcast import broadcast_handler

from pyrogram import Client, filters, idle
from pyrogram.errors import UserNotParticipant, PeerIdInvalid, ChannelPrivate
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

Bot = Client(
    session_name=Config.TG_BOT_SESSION,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
User = Client(
    session_name=Config.TG_USER_SESSION,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)


@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    await event.reply_text(
        Config.START_TEXT.format(event.chat.first_name, event.chat.id),
        disable_web_page_preview=True,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Help", callback_data="helpMeh"),
                    InlineKeyboardButton("About", callback_data="aboutMeh")
                ],
                [
                    InlineKeyboardButton("Support Group", url="https://t.me/DevsZone"),
                    InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")
                ],
                [
                    InlineKeyboardButton("Developer - @AbirHasan2005", url="https://t.me/AbirHasan2005")
                ]
            ]
        ),
        quote=True
    )


@Bot.on_message(filters.private & filters.command("status") & filters.user(Config.OWNER_ID))
async def status_command_handler(_, event: Message):
    total_users = await db.total_users_count()
    await event.reply_text(text=f"Total users is DB: {total_users}", quote=True)


@Bot.on_message(filters.private & filters.command("broadcast") & filters.reply & filters.user(Config.OWNER_ID))
async def __broadcast(_, event: Message):
    await broadcast_handler(event)


@User.on_message(filters.private & filters.text & filters.user([454000, 844978205]), group=-2)
async def dmca_handler(user: Client, event: Message):
    status, chat_id, message_ids = await ExtractChatData(user=user, bot=Bot, message=event)
    if status == 400:
        return
    del_messages, __err = await DeleteMessages(client=User, chat_id=chat_id, message_ids=message_ids)
    if del_messages == 400:
        print(f"Got Error - {chat_id} - {__err}")
        return


@Bot.on_message(filters.private & filters.forwarded)
async def forward_handler(bot: Client, event: Message):
    await AddUserToDatabase(bot, event)
    FSub = await ForceSub(bot, event)
    if FSub == 400:
        return
    if event.forward_from_chat:
        editable = await event.reply_text("Please Wait ...")
        try:
            userOnChat = await bot.get_chat_member(chat_id=event.forward_from_chat.id, user_id=event.from_user.id)
            if (userOnChat.can_delete_messages is not True) or (userOnChat.can_promote_members is not True) or (userOnChat.can_invite_users is not True):
                await editable.edit(f"Sorry, {event.from_user.mention}.\n"
                                    f"You don't have required rights!\n\n"
                                    f"Make sure you have the following rights:"
                                    f"`- Can Delete Messages`\n"
                                    f"`- Can Promote Members`\n"
                                    f"`- Can Invite Members`",
                                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Support Group", url="https://t.me/DevsZone")]]))
            else:
                try:
                    meOnChat = await bot.get_chat_member(chat_id=event.forward_from_chat.id, user_id=(await bot.get_me()).id)
                    if (meOnChat.can_delete_messages is not True) or (meOnChat.can_invite_users is not True) or (meOnChat.can_promote_members is not True):
                        await editable.edit("I am Not Admin in that Channel!\n"
                                            "Please Add as Admin with **Delete Messages**, **Add Admins** & **Invite Users** Permission.")
                    else:
                        channel = await bot.get_chat(event.forward_from_chat.id)
                        my_channel = await bot.get_chat_member(chat_id=channel.id, user_id=(await bot.get_me()).id)
                        if (my_channel.can_invite_users is not True) or (
                                my_channel.can_delete_messages is not True) or (
                                my_channel.can_promote_members is not True):
                            await editable.edit("I am Not Admin in that Channel!\n"
                                                "Please Add as Admin with **Delete Messages**, **Add Admins** & **Invite Users** Permission.")
                            return
                        try:
                            await bot.get_chat_member(chat_id=channel.id, user_id=(await User.get_me()).id)
                        except UserNotParticipant:
                            await User.join_chat(channel.invite_link)
                            try:
                                await bot.promote_chat_member(
                                    chat_id=channel.id,
                                    user_id=(await User.get_me()).id,
                                    can_change_info=False,
                                    can_post_messages=False,
                                    can_edit_messages=False,
                                    can_delete_messages=True,
                                    can_restrict_members=False,
                                    can_invite_users=True,
                                    can_pin_messages=False,
                                    can_promote_members=False
                                )
                            except:
                                await editable.edit(f"Failed to Promote @{(await User.get_me()).username}!\n"
                                                    f"Please Add him as Admin with **Delete Messages**, **Add Admins** & **Invite Users** Permission.")
                                return
                        await editable.edit("OK, I will Automatically Delete DMCA Messages from that Chat.")
                except:
                    await editable.edit("I am Not Admin in that Channel!\n"
                                        "Please Add as Admin with **Delete Messages**, **Add Admins** & **Invite Users** Permission.")
        except (PeerIdInvalid, ChannelPrivate):
            await editable.edit("I am Not Admin in that Channel!\n"
                                "Please Add as Admin with **Delete Messages**, **Add Admins** & **Invite Users** Permission.")


@Bot.on_callback_query()
async def callback_handlers(_, event: CallbackQuery):
    if "aboutMeh" in event.data:
        await event.message.edit(
            Config.ABOUT_TEXT,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Home", callback_data="takeMehToHome"),
                     InlineKeyboardButton("Help", callback_data="helpMeh")],
                    [InlineKeyboardButton("Support Group", url="https://t.me/DevsZone"),
                     InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")]
                ]
            )
        )
    elif "helpMeh" in event.data:
        await event.message.edit(
            Config.HELP_TEXT,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Home", callback_data="takeMehToHome"),
                     InlineKeyboardButton("About", callback_data="aboutMeh")],
                    [InlineKeyboardButton("Support Group", url="https://t.me/DevsZone"),
                     InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")]
                ]
            )
        )
    elif "takeMehToHome" in event.data:
        await event.message.edit(
            Config.START_TEXT.format(event.from_user.first_name, event.from_user.id),
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Help", callback_data="helpMeh"),
                        InlineKeyboardButton("About", callback_data="aboutMeh")
                    ],
                    [
                        InlineKeyboardButton("Support Group", url="https://t.me/DevsZone"),
                        InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")
                    ],
                    [
                        InlineKeyboardButton("Developer - @AbirHasan2005", url="https://t.me/AbirHasan2005")
                    ]
                ]
            )
        )
    await event.answer()


# Start Both Clients
Bot.start()
print("Bot Started!")
User.start()
print("User Started!")
# Loop
idle()
print("\n")
# Stop Both Clients
Bot.stop()
print("Bot Stopped!")
User.stop()
print("User Stopped!")
