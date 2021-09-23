import random
import time
import datetime
import asyncio
from aiogram import types, exceptions
from .Dbmodule import UserGetDatabase, UserAddDatabase
from .functions import *
from dispatcher import dp, bot
from config import MYID, GROUP_ID
import Datapacks
startTime = time.time()


#информация по боту и автору
@dp.message_handler(commands= ["info"], commands_prefix="/")
async def info(message: types.Message):
	info ="""
		"Для разбанов в боте писать @Ваш юзернейм@"
		"Бот умеет распознавать голосовые сообщения, нужно просто отправить гс в ЛС боту"
		"Бот написан на языке Python 3.9.6\n Автор @cybeer"
		"""
	if message.chat.type != 'private':
		return
	else: await message.bot.send_message(chat_id=message.chat.id, text=info, parse_mode="Markdown")
	await log(message)


#информация по командам
@dp.message_handler(commands= ["start","help"], commands_prefix="/")
async def help(message: types.Message):
	if await checkUser(message) == True:
		return
	info="[A]start - Помощь и информация о командах\n[A]help - Помощь и информация о командах\n[A]info - Информация о боте и создателе\n[G]pet - Похвалить участника чата\n[G]status - Статус в супергруппе\n[G]role - Кастомная роль\n[G]joke - Кринжмашина\n[A]reg - Регистрация в БД бота\n[A]ping - Проверка бота\n[A]uptime - Время от запуска бота\n[A]voice - Ручное распознавание голосового сообщения\n[A]voiceallow - Включение автораспознавания голосовых сообщений\n[P]invite - Пригласительная ссылка в группу\n[A] - Команда доступна во всех чатах\n[G] - Команда доступна только в групповых чатах\n[P] - Команда доступна только в личных сообщениях бота"
	await message.bot.send_message(chat_id=message.chat.id, text = info)
	await log(message)


#пригласительная ссылка в чат
@dp.message_handler(commands= ["invite"], commands_prefix="/")
async def invite(message: types.Message):
	if message.from_user.id in Datapacks.idList:
		if message.chat.type == 'private':
			invite_link = await message.bot.export_chat_invite_link(chat_id=GROUP_ID)
			mes = await message.bot.send_message(chat_id=message.chat.id,
							   text=f"Ваша пригласительная ссылка {invite_link}",
							   parse_mode="Markdown") 
		else: 
			mes = await message.reply("Отправь это сообщение в лс")
	else:	
		mes = await message.reply("Эта команда тебе недоступна")
	await delete_message(message, mes, 120)
	await log(message)


#показывает статус в чате
@dp.message_handler(commands= ["status"], commands_prefix="/")
async def rights(message: types.Message):
	if await checkUser(message) == True:
		return
	if message.chat.type == 'private':
		return
	status = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
	mes = await message.bot.send_message(chat_id=message.chat.id, text = status.status)
	await delete_message(message, mes, 60)
	await log(message)


#функции бота и команды
@dp.message_handler(commands= ["ping"], commands_prefix="/")
async def ping(message: types.Message):
	if await checkUser(message) == True:
		return
	mes = await message.bot.send_message(chat_id=message.chat.id, text = "I`m here!!!")
	await delete_message(message, mes, 60)
	await log(message)


#Время прошедшее со времени запуска бота
@dp.message_handler(commands= ["uptime"], commands_prefix="/")
async def uptime(message:types.Message):
	if await checkUser(message) == True:
		return
	uptime = time.time() - startTime
	mes = await message.bot.send_message(chat_id=message.chat.id, text=time.strftime("%H:%M:%S", time.gmtime(uptime)))
	await delete_message(message, mes, 60)
	await log(message)


#регистрация в боте и добавление в БД надо доделать заявки
@dp.message_handler(commands= ["reg"], commands_prefix="/")
async def register(message: types.Message):
	if await checkUser(message) == True:
		return
	member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
	stat = str(member.status)
	text = message.get_args()
	#if message.chat.type == 'private':
		#if len(text) != 0:
			#mes = 'Поступила анкета на регистрацию от {} [@{}].\n\nСодержание анкеты:\n{}'.format(
			#message.from_user.first_name, message.from_user.username, message.text.replace("/reg", ""))
	try:
		if UserGetDatabase(message)[0] != message.from_user.id:
			if message.from_user.username is None:
				mes=f"{message.from_user.first_name}, зарегестрирован в Базе Данных"
			else:
				mes=f"{message.from_user.username}, зарегестрирован в Базе Данных"
			await message.bot.send_message(chat_id=MYID, text=mes)
			await message.bot.send_message(chat_id=message.chat.id,
								  parse_mode="Markdown",
								  text="Вы успешно зарегестрированы.")
			UserAddDatabase(message, stat)
		else: 
			await message.bot.send_message(chat_id=message.chat.id,
								  parse_mode="Markdown",
								  text="Вы уже зарегестрированы.")
			UserAddDatabase(message, stat)
	except IndexError:
		if not message.from_user.username:
			mes=f"{message.from_user.first_name}, зарегестрирован в Базе Данных"
		else:
			mes=f"{message.from_user.username}, зарегестрирован в Базе Данных"
		await message.bot.send_message(chat_id=MYID, text=mes)
		await message.bot.send_message(chat_id=message.chat.id,
								 parse_mode="Markdown",
								 text="Вы успешно зарегестрированы.")
		UserAddDatabase(message, stat)
	await log(message)
		#else:
			#mes = 'Допишите команду в формате `/reg <args>`.\nВ аргументе желательно описать по какой причине вы хотите в чат.'
			#await message.bot.send_message(chat_id=message.chat.id, parse_mode="Markdown", text=mes)
	#else:
		#await message.reply("Напиши это в лс мудила")


@dp.message_handler(commands= ["pet"], commands_prefix="/")
async def pet(message: types.Message):
	if message.reply_to_message:
		mes = message.reply_to_message	
		if message.from_user.username is not None:
			user = message.from_user.username
			if mes.from_user.username is not None: 
				reply_user = mes.from_user.username
			else: 
				reply_user = mes.from_user.first_name
		else:
			user = message.from_user.first_name
		if mes.from_user.username is not None:
			reply_user = mes.from_user.first_name
		else: 
				reply_user = mes.from_user.first_name
		text = Datapacks.petlist[random.randint(1, len(Datapacks.petlist))].format(user, reply_user)
		if message.from_user.id == mes.from_user.id:
			await message.bot.send_message(chat_id=message.chat.id,
									 reply_to_message_id=message.message_id,
									 text="Ну вот давай без этого вот.")
		elif message.reply_to_message:
			await message.bot.send_message(chat_id=message.chat.id, disable_web_page_preview=True,
									 reply_to_message_id=mes.message_id, parse_mode='html',
									 text=text)
			await delete_message(message=message, time=60)
		elif "@" in " ".join(message.get_args()):
			mes1 = await message.reply("Никакого этого, МНЕ НУЖЕН РЕПЛАЙ.")
			await delete_message(message, mes1, 60)
	else:
		mes1 = await message.reply("Нужен реплай. Ответь на чье то сообщение этой командой.")
		time.sleep(10)
		await delete_message(message, mes1, 60)
	await log(message)


@dp.message_handler(commands= ["joke"], commands_prefix="/")
async def joke(message: types.Message):
	if message.get_args():
		await message.bot.send_message(chat_id=message.chat.id, parse_mode="HTML",
								 reply_to_message_id=message.message_id,
								 text="Аргумент <b>arg</b> не нужен.")
	else:
	   await message.bot.send_message(chat_id=message.chat.id, parse_mode="HTML",
								 reply_to_message_id=message.message_id,
								 text=anekgen())
	await delete_message(message=message, time=30)
	await log(message)


#работает
@dp.message_handler(commands= ["role"], commands_prefix="/")
async def role(message: types.Message):
	if await checkUser(message) == True:
		return
	roletext = message.get_args()
	try:
		if message.chat.type != 'private':
			if len(roletext) != 0:
				if roletext == 'clear':
					await message.bot.promote_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, can_pin_messages = False)
					mes = await message.reply("Успешно, роль снята!")

				elif len(roletext) <= 16 and roletext != 'clear':
					await message.bot.promote_chat_member(chat_id=message.chat.id, user_id=message.from_user.id,
													can_pin_messages=True)
					await message.bot.set_chat_administrator_custom_title(chat_id=message.chat.id,
																	user_id=message.from_user.id,
																	custom_title = roletext)
					mes = await message.reply("Успешно!\nРоль появится в течение минуты.")
				elif len(roletext) > 16:
					Error = await message.reply("Не могу поставить роль. Роль должна быть длинной 16 символов и менее.")
					await delete_message(message, Error, 60)
			else:
				 mes = await message.reply("Нет аргумента, для снятия роли пропиши /role clear , для присвоения роли пропиши /role arg")

		else:
			await message.bot.send_message(chat_id=message.chat.id,
									 text="Напиши это в группе")
	except exceptions.CantRestrictChatOwner:
		mes = await message.reply("Ты здесь главный, тебе роль поставить не могу")
	await delete_message(message, mes, 60)
	await log(message)