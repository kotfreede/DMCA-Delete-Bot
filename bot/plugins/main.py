# (c) @AbirHasan2005

import os
import asyncio
import aiofiles
import datetime
import traceback
import random
import string
import time
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, \
	PeerIdInvalid, ChatAdminRequired
from pyrogram.errors.exceptions.forbidden_403 import MessageDeleteForbidden, MessageAuthorRequired, RightForbidden
from bot.database import Database
from bot.helpers.make_user_join_chat import make_chat_user_join
from bot import (
	SESSION_NAME,
	DATABASE_URL,
	UPDATES_CHANNEL,
	LOGS_CHANNEL,
	START_TEXT,
	HELP_TEXT,
	ABOUT_TEXT,
	ADMIN,
        BROADCAST_AS_COPY
)
from bot.bot import Bot

db = Database(DATABASE_URL, SESSION_NAME)
broadcast_ids = {}


async def send_msg(user_id, message):
	try:
		if BROADCAST_AS_COPY is False:
			await message.forward(chat_id=user_id)
		elif BROADCAST_AS_COPY is True:
			await message.copy(chat_id=user_id)
		return 200, None
	except FloodWait as e:
		await asyncio.sleep(e.x)
		return send_msg(user_id, message)
	except InputUserDeactivated:
		return 400, f"{user_id} : deactivated\n"
	except UserIsBlocked:
		return 400, f"{user_id} : blocked the bot\n"
	except PeerIdInvalid:
		return 400, f"{user_id} : user id invalid\n"
	except Exception as e:
		return 500, f"{user_id} : {traceback.format_exc()}\n"


@Bot.on_message(filters.command("start") & filters.private)
async def startbot(bot: Bot, cmd: Message):
	if not await db.is_user_exist(cmd.chat.id):
		await db.add_user(cmd.chat.id)
		await bot.send_message(
			LOGS_CHANNEL,
			f"#NEW_USER: \n\nNew User [{cmd.chat.first_name}](tg://user?id={cmd.chat.id}) started @DMCA_DelBot !!"
		)
	if UPDATES_CHANNEL is not None:
		try:
			user = await bot.get_chat_member(UPDATES_CHANNEL, cmd.chat.id)
			if user.status == "kicked":
				await bot.send_message(
					chat_id=cmd.chat.id,
					text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		except UserNotParticipant:
			await bot.send_message(
				chat_id=cmd.chat.id,
				text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
						]
					]
				),
				parse_mode="markdown"
			)
			return
		except Exception:
			await bot.send_message(
				chat_id=cmd.chat.id,
				text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
				parse_mode="markdown",
				disable_web_page_preview=True)
			return
	await cmd.reply_text(
		START_TEXT.format(cmd.chat.first_name, cmd.chat.id),
		disable_web_page_preview=True,
		parse_mode="Markdown",
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("Help", callback_data="helpmeh"),
					InlineKeyboardButton("About", callback_data="aboutmeh")
				],
				[
					InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
					InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")
				],
				[
					InlineKeyboardButton("Developer - @AbirHasan2005", url="https://t.me/AbirHasan2005")
				]
			]
		),
		quote=True
	)


@Bot.on_message(filters.command("help") & filters.private)
async def helpmsg(bot: Bot, cmd: Message):
	if not await db.is_user_exist(cmd.chat.id):
		await db.add_user(cmd.chat.id)
		await bot.send_message(
			LOGS_CHANNEL,
			f"#NEW_USER: \n\nNew User [{cmd.chat.first_name}](tg://user?id={cmd.chat.id}) started @DMCA_DelBot !!"
		)
	if UPDATES_CHANNEL is not None:
		try:
			user = await bot.get_chat_member(UPDATES_CHANNEL, cmd.chat.id)
			if user.status == "kicked":
				await bot.send_message(
					chat_id=cmd.chat.id,
					text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		except UserNotParticipant:
			await bot.send_message(
				chat_id=cmd.chat.id,
				text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
						]
					]
				),
				parse_mode="markdown"
			)
			return
		except Exception:
			await bot.send_message(
				chat_id=cmd.chat.id,
				text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
				parse_mode="markdown",
				disable_web_page_preview=True)
			return
	await cmd.reply_text(
		HELP_TEXT,
		disable_web_page_preview=True,
		parse_mode="Markdown",
		reply_markup=InlineKeyboardMarkup(
			[
				[
					InlineKeyboardButton("Home", callback_data="gotohome"),
					InlineKeyboardButton("About", callback_data="aboutmeh")
				],
				[
					InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
					InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")
				],
				[
					InlineKeyboardButton("Developer - @AbirHasan2005", url="https://t.me/AbirHasan2005")
				]
			]
		),
		quote=True
	)


@Bot.on_message(filters.private & filters.command("status") & filters.user(ADMIN))
async def sts(c: Bot, m: Message):
	total_users = await db.total_users_count()
	await m.reply_text(text=f"Total users is DB: {total_users}", quote=True)


@Bot.on_message(filters.private & filters.command("broadcast") & filters.user(ADMIN) & filters.reply)
async def broadcast_(c: Bot, m: Message):
	all_users = await db.get_all_users()
	broadcast_msg = m.reply_to_message
	while True:
		broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
		if not broadcast_ids.get(broadcast_id):
			break
	out = await m.reply_text(
		text=f"Broadcast initiated! You will be notified with log file when all the users are notified."
	)
	start_time = time.time()
	total_users = await db.total_users_count()
	done = 0
	failed = 0
	success = 0
	broadcast_ids[broadcast_id] = dict(
		total=total_users,
		current=done,
		failed=failed,
		success=success
	)
	async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
		async for user in all_users:
			sts, msg = await send_msg(
				user_id=int(user['id']),
				message=broadcast_msg
			)
			if msg is not None:
				await broadcast_log_file.write(msg)
			if sts == 200:
				success += 1
			else:
				failed += 1
			if sts == 400:
				await db.delete_user(user['id'])
			done += 1
			if broadcast_ids.get(broadcast_id) is None:
				break
			else:
				broadcast_ids[broadcast_id].update(
					dict(
						current=done,
						failed=failed,
						success=success
					)
				)
	if broadcast_ids.get(broadcast_id):
		broadcast_ids.pop(broadcast_id)
	completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
	await asyncio.sleep(3)
	await out.delete()
	if failed == 0:
		await m.reply_text(
			text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
			quote=True
		)
	else:
		await m.reply_document(
			document='broadcast.txt',
			caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
			quote=True
		)
	os.remove('broadcast.txt')


@Bot.on_message((filters.text | filters.forwarded) & filters.private & ~filters.edited)
async def main(bot: Bot, message: Message):
	if not await db.is_user_exist(message.chat.id):
		await db.add_user(message.chat.id)
		await bot.send_message(
			LOGS_CHANNEL,
			f"#NEW_USER: \n\nNew User [{message.chat.first_name}](tg://user?id={message.chat.id}) started @DMCA_DelBot !!"
		)
	if UPDATES_CHANNEL is not None:
		try:
			user = await bot.get_chat_member(UPDATES_CHANNEL, message.chat.id)
			if user.status == "kicked":
				await bot.send_message(
					chat_id=message.chat.id,
					text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/linux_repo).",
					parse_mode="markdown",
					disable_web_page_preview=True
				)
				return
		except UserNotParticipant:
			await bot.send_message(
				chat_id=message.chat.id,
				text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
				reply_markup=InlineKeyboardMarkup(
					[
						[
							InlineKeyboardButton("🤖 Join Updates Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
						]
					]
				),
				parse_mode="markdown"
			)
			return
		except Exception:
			await bot.send_message(
				chat_id=message.chat.id,
				text="Something went Wrong. Contact my [Support Group](https://t.me/linux_repo).",
				parse_mode="markdown",
				disable_web_page_preview=True)
			return
	is_private = False
	username = None
	messageIDs = []

	if not "https://t.me" in message.text:
		await message.reply_text("What I will do with this? 😂", quote=True)
		return
	links = list(filter(lambda s: s.startswith("https://t.me"), message.text.split()))
	links = list(links)
	for link in links:
		dev = link.split("/")
		IDs = dev[-1]
		username = dev[-2]
		messageIDs.append(int(IDs))
		test = dev[-3]
		if test == "c":
			is_private = True
			username = "-100" + username
			username = int(username)
	print(f"Channel Address: {username}")
	send = None
	channel = None
	## --- Making Route Clear --- ##
	try:
		channel = await bot.get_chat(username)
	except:
		await message.reply_text(f"Chat `{username}` Not Found!")
		return
	print(channel)
	try:
		user = await bot.get_chat_member(chat_id=channel.id, user_id=message.from_user.id)
		if not (user.status == "creator"
				or user.status == "administrator"):
			await message.reply_text(
				f"Oye Saale, this is not your Chat, you are not an Admin in `{username}` !!\n\nLet that task done by any Admin or Owner 😂",
				disable_web_page_preview=True, parse_mode="Markdown", quote=True)
			return
		if not user.can_delete_messages == True:
			await message.reply_text(f"Sorry {message.from_user.first_name},\nYou don't have Delete Messages Right!")
			return
	except UserNotParticipant:
		await message.reply_text(
			f"Oye Saale, this is not your Chat, you are not an Admin in `{username}` !!\n\nLet that task done by any Admin or Owner 😂",
			disable_web_page_preview=True, parse_mode="Markdown", quote=True)
		return
	except Exception as err:
		await message.reply_text(f"**Error:** `{err}`")
		return
	## --- Route Clear Now --- ##
	try:
		if message.forward_from:
			if int(message.forward_from.id) == 454000:
				send = await message.reply_text("Got [Telegram DMCA](tg://user?id=454000) Notice Message ...",
												parse_mode="Markdown", quote=True)
				await asyncio.sleep(2)
			else:
				send = await message.reply_text("Trying to Delete **Listed** Messages ...", parse_mode="Markdown",
												quote=True)
		else:
			send = await message.reply_text("Trying to Delete **Listed** Messages ...", parse_mode="Markdown",
											quote=True)
		## --- Thanks to Shrimadhav Sir --- ##
		s__, nop = await make_chat_user_join(
			bot.USER,
			bot.USER_ID,
			channel
		)
		if not s__:
			await send.edit(nop.format(username), disable_web_page_preview=True)
			return
		## --- Thanks to Shrimadhav Sir --- ##
		await send.edit("Forwarding the Messages which are being Deleted!")
		await bot.forward_messages(chat_id=message.chat.id, from_chat_id=username, message_ids=messageIDs)
		await bot.USER.delete_messages(
			chat_id=username,
			message_ids=messageIDs,
			revoke=True
		)
		await send.delete()
		await message.reply_text("Deleted Successfully!")
		# await bot.USER.leave_chat(username)
		await bot.send_message(chat_id=LOGS_CHANNEL,
							   text=f"#DMCA_DELETE:\n\nDeleted `{len(messageIDs)}` Messages From {channel.title} which has `{channel.members_count}` Members !!")
	except FloodWait as e:
		await send.delete()
		await message.reply_text(f"Sorry, I got FloodWait Error!\n\nTry Again after `{e.x}s` ...",
								 parse_mode="Markdown")
	except Exception as e:
		if channel.username == "None":
			one_msg = messageIDs[0]
			await send.edit(
				f"Unable to Delete Message in [{channel.title}](https://t.me/c/{channel.id}/{one_msg}) !\n\n**Error:** `{e}`",
				reply_markup=InlineKeyboardMarkup(
					[[InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")]]),
				disable_web_page_preview=True, parse_mode="Markdown")
		else:
			await send.edit(f"Unable to Delete Message in @{channel.username} !\n\n**Error:** `{e}`",
							reply_markup=InlineKeyboardMarkup(
								[[InlineKeyboardButton("Support Group", url="https://t.me/linux_repo")]]),
							disable_web_page_preview=True, parse_mode="Markdown")


@Bot.on_callback_query()
async def button(bot: Bot, cmd: CallbackQuery):
	cb_data = cmd.data
	if "aboutmeh" in cb_data:
		await cmd.message.edit(
			ABOUT_TEXT,
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[InlineKeyboardButton("Home", callback_data="gotohome"),
					 InlineKeyboardButton("Help", callback_data="helpmeh")],
					[InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
					 InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")],
					[InlineKeyboardButton("Donate Now (PayPal)", url="https://www.paypal.me/AbirHasan2005")]
				]
			)
		)
	elif "helpmeh" in cb_data:
		await cmd.message.edit(
			HELP_TEXT,
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[InlineKeyboardButton("Home", callback_data="gotohome"),
					 InlineKeyboardButton("About", callback_data="aboutmeh")],
					[InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
					 InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")]
				]
			)
		)
	elif "gotohome" in cb_data:
		await cmd.message.edit(
			START_TEXT.format(cmd.from_user.first_name, cmd.from_user.id),
			parse_mode="Markdown",
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Help", callback_data="helpmeh"),
						InlineKeyboardButton("About", callback_data="aboutmeh")
					],
					[
						InlineKeyboardButton("Support Group", url="https://t.me/linux_repo"),
						InlineKeyboardButton("Bots Channel", url="https://t.me/Discovery_Updates")
					],
					[
						InlineKeyboardButton("Developer - @AbirHasan2005", url="https://t.me/AbirHasan2005")
					]
				]
			)
		)
