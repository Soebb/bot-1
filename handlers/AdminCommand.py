from aiogram import types, exceptions
from dispatcher import dp
from .Dbmodule import clearGay, clearPisun
from .functions import delete_message, log
from config import MYID


@dp.message_handler(commands= ["admin"], commands_prefix="/")
async def setAdmin(message: types.Message):
	if message.reply_to_message and message.from_user.id == MYID:
		reply = message.reply_to_message
		roletext = message.get_args()
		try:
			if message.chat.type != 'private':
				if len(roletext) != 0:
					if len(roletext) <= 16:
						await message.bot.promote_chat_member(chat_id=message.chat.id,
											user_id=reply.from_user.id,
											is_anonymous=False,
											can_manage_chat=False,
											can_change_info=True,
											can_delete_messages=False,
											can_manage_voice_chats=True,
											can_invite_users=True,
											can_restrict_members=True,
											can_pin_messages=True,
											can_promote_members=False)
						await message.bot.set_chat_administrator_custom_title(chat_id=message.chat.id,
																		user_id=reply.from_user.id,
																		custom_title = roletext)
						mes = await message.reply("Успешно!\nРоль и права появятся в течение минуты.")
					elif len(roletext) > 16:
						Error = await message.reply("Не могу поставить роль. Роль должна быть длинной 16 символов и менее.")
						await delete_message(message, Error, 60)
				else:
					await message.bot.promote_chat_member(chat_id=message.chat.id,
										   user_id=reply.from_user.id,
											is_anonymous=False,
											can_manage_chat=False,
											can_change_info=True,
											can_delete_messages=False,
											can_manage_voice_chats=True,
											can_invite_users=True,
											can_restrict_members=True,
											can_pin_messages=True,
											can_promote_members=False)
					mes = await message.reply_to_message.reply("Ты теперь админ :)")

			else:
				await message.bot.send_message(chat_id=message.chat.id,
										 text="Напиши это в группе")
		except exceptions.CantRestrictChatOwner:
			mes = await message.reply("Ты здесь главный, тебя трогать не могу")
		await delete_message(message, mes, 60)
	elif not message.reply_to_message:
		mes = await message.reply("Нужен реплай на сообщение")
		delete_message(message, mes, 60)
	elif message.from_user.id != MYID:
		mes = await message.reply("Эта команда не для вас написана")
		delete_message(message, mes, 60)
	await log(message)


@dp.message_handler(commands= ["noadmin"], commands_prefix="/")
async def setAdmin(message: types.Message):
	if message.reply_to_message and message.from_user.id == MYID:
		reply = message.reply_to_message
		try:
			if message.chat.type != 'private':
				await message.bot.promote_chat_member(chat_id=message.chat.id,
										  user_id=reply.from_user.id,
										  is_anonymous=False,
										  can_manage_chat=False,
										  can_change_info=False,
										  can_delete_messages=False,
										  can_manage_voice_chats=False,
										  can_invite_users=False,
										  can_restrict_members=False,
										  can_pin_messages=False,
										  can_promote_members=False)
				mes = await message.reply("Успешно!\nПрава исчезнут в течении минуты.")
			else:
				await message.bot.send_message(chat_id=message.chat.id, text="Напиши это в группе")
		except exceptions.CantRestrictChatOwner:
			mes = await message.reply("Ты здесь главный, тебя трогать не могу")
		await delete_message(message, mes, 60)
	elif not message.reply_to_message:
		mes = await message.reply("Нужен реплай на сообщение")
		delete_message(message, mes, 60)
	elif message.from_user.id != MYID:
		mes = await message.reply("Эта команда не для вас написана")
		delete_message(message, mes, 60)
	await log(message)