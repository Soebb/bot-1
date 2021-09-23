import asyncio
from colorama import Fore, Back
from colorama import init
import Datapacks
import random
import sqlite3
import datetime
import re
from .Dbmodule import getUserBlackList, addUserBlackList, UserAddDatabase, logs, inlineLogs
from config import MYID
__all__=["delete_message",
		 "checkUser",
		 "generate",
		 "anekgen",
		 "log",
		 "InlineLog",]
init(autoreset=True)

#удаление сообщений
async def delete_message(message, mes=None, time=None):
	await asyncio.sleep(time)
	if mes is not None:
		await message.bot.delete_message(chat_id=message.chat.id, message_id=mes.message_id)
	await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


#проверка на черный список
async def checkUser(message):
	try:
		if message.from_user.id == getUserBlackList(message)[0] and getUserBlackList(message)[1] == True:
			return True
	except IndexError:
		status = 0
		addUserBlackList(message, status)
		if message.from_user.id == getUserBlackList(message)[0] and getUserBlackList(message)[1] == False:
			return False


#рандом генератор шуток и прочего
def generate(message, mes):
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
	return Datapacks.list[random.randint(1, len(Datapacks.list))].format(user, reply_user)


def anekgen():
	finaltext = '{} приходит {} и говорит:\n- {}\nА {}:\n- {}\n{}'.format(
		Datapacks.who[random.randint(1, len(Datapacks.who))], Datapacks.come[random.randint(1, len(Datapacks.come))],
		Datapacks.say[random.randint(1, len(Datapacks.say))], Datapacks.but[random.randint(1, len(Datapacks.but))],
		Datapacks.phrase[random.randint(1, len(Datapacks.phrase))],
		Datapacks.last[random.randint(1, len(Datapacks.last))])
	return finaltext




#логирование всего что существует
async def log(message):
	text = ""
	username = message.from_user.username
	if username is not None:
		if message.chat.type == 'private':
			text = '[{}] {} отправил команду [{}] в чате {}. ID - {}'.format(
				datetime.datetime.now().strftime("%d.%m.%y, %H:%M"), username,
				message.text, message.chat.type, message.from_user.id)
			print(Fore.BLACK + Back.YELLOW + text)
		elif message.chat.type == 'supergroup' or 'group':
			text = '[{}] {} отправил команду [{}] в чате {}. ID - {}'.format(
				datetime.datetime.now().strftime("%d.%m.%y, %H:%M"), username,
				message.text, message.chat.title, message.from_user.id)
			print(Fore.BLUE + text)
		try:
			await message.bot.send_message(chat_id=MYID, text=text)
			logs(message)
		except Exception as exc:
			print(exc)
		UserAddDatabase(message)
	else:
		first_name = message.from_user.first_name
		if message.chat.type == 'private':
			text = '[{}] {} отправил команду [{}] в чате {}. ID - {}'.format(
				datetime.datetime.now().strftime("%d.%m.%y, %H:%M"), first_name,
				message.text, message.chat.type, message.from_user.id)
			print(Fore.BLACK + Back.YELLOW + text)
		elif message.chat.type == 'supergroup' or 'group':
			text = '{} {} отправил команду [{}] в чате {}. ID - {}'.format(
				datetime.datetime.now().strftime("%d.%m.%y, %H:%M"), first_name,
				message.text, message.chat.title, message.from_user.id)
			print(Fore.BLUE + text)
		try:
			await message.bot.send_message(chat_id=MYID, text=text)
			logs(message)
		except Exception as exc:
			print(exc)
		UserAddDatabase(message)


async def InlineLog(inline_query):
	text = ""
	username = inline_query.from_user.username
	query = inline_query.query
	if username is not None:
		print(Fore.BLUE + "Inline YT запрос - {}".format(query))
		inlineLogs(inline_query)
	else:
		first_name = inline_query.from_user.first_name
		print(Fore.BLUE + "Inline YT запрос - {}".format(query))
		inlineLogs(inline_query)