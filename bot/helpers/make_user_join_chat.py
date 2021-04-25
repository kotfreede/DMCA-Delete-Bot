#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | @AbirHasan2005
#
# This is first coded by Shrimadhav Sir.
# Thanks a lot for the nice script.
#
# This is modified by @AbirHasan2005 for
# DMCA Delete Bot: @DMCA_DelBot 


from pyrogram.errors import (
    InviteHashExpired,
    InviteHashInvalid,
    UserAlreadyParticipant,
    ChatAdminRequired
)
from pyrogram.types import Chat
from bot.bot import Bot


async def make_chat_user_join(
    client: Bot,
    user_id: int,
    chat: Chat
):
    try:
        await client.join_chat(chat.invite_link) #
    except ChatAdminRequired:
        return False, "Sorry Sir, I am not Admin in `{}` !!\n\nPlease add me as Admin in that chat will **Delete Messages** & **Add Admins** rights."
    except UserAlreadyParticipant:
        pass
    _existing_permissions = await chat.get_member(user_id)
    if _existing_permissions.status == "creator":
        return True, None
    if not _existing_permissions.can_delete_messages:
        await chat.promote_member(
            user_id,
            can_change_info=False,
            can_post_messages=False,
            can_edit_messages=False,
            can_delete_messages=True,
            can_restrict_members=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False
        )
    return True, None
