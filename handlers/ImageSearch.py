import re
import sys
from bs4 import BeautifulSoup
from urllib import parse
from aiogram import types
sys.path.insert(0, 'C:/Users/Legion/Desktop/bot/')
from dispatcher import dp, bot
from .functions import delete_message, checkUser
from config import TOKEN, BOTID
from .Dbmodule import addUserBlackList, getUserBlackList
from .ImageSearchEngine import *


#Функции распознавания изображений, проверить работоспособность позже   
@dp.message_handler(content_types = ['photo'])
async def sauce(message: types.Message):
	if await checkUser(message) == True:
		return
	if message.from_user.id != BOTID:
		if message.chat.type == 'private':
			file_info = await message.bot.get_file(message.photo[0].file_id)
			file_url = "https://api.telegram.org/file/bot"+TOKEN+"/"+file_info.file_path
			await saucenao(file_url, message)
			#await ascii2d(file_url, message) не работает
			#await anime(file_url, message) не работает
			await iqdb(file_url, message)
			await message.bot.send_message(chat_id=message.chat.id, text="Поиск завершен", parse_mode="MarkdownV2")
	else:
		return
	await log(message)

@dp.message_handler(commands=['all'], commands_prefix="/")
async def allSearch(message):
	if await checkUser(message) == True:
		return
	if not message.reply_to_message:
		mes = await message.reply("Нужен реплай на сообщение")
		await delete_message(message, mes, 60)
	else:
		mes = message.reply_to_message
		if not mes.photo:
			await message.reply("Нужен реплай на фото")
			return
		file_info = await message.bot.get_file(mes.photo[0].file_id)
		file_url = "https://api.telegram.org/file/bot"+TOKEN+"/"+file_info.file_path
		await saucenao(file_url, message)
		#await ascii2d(file_url, message.chat.id) не работает
		#anime(file_url, message.chat.id) не работает
		await iqdb(file_url, message)
		await message.bot.send_message(chat_id=message.chat.id, text="Поиск завершен", parse_mode="MarkdownV2")
	await log(message)

'''@dp.message_handler(commands=['ascii2'], commands_prefix="/")
async def ascii2Search(message):
	if await checkUser(message) == True:
		return
	if not message.reply_to_message:
		mes = await message.reply("Нужен реплай на сообщение")
		await delete_message(message, mes, 60)
	else:
		mes = message.reply_to_message
		file_info = await message.bot.get_file(mes.photo[0].file_id)
		file_url = "https://api.telegram.org/file/bot"+TOKEN+"/"+file_info.file_path
		await ascii2d(file_url, message.chat.id)
		await message.bot.send_message(chat_id=message.chat.id, text="Поиск завершен", parse_mode="MarkdownV2")
'''

@dp.message_handler(commands=["saucenao"], commands_prefix="/")
async def sauce(message: types.Message):
	if await checkUser(message) == True:
		return
	if not message.reply_to_message:
		mes = await message.reply("Нужен реплай на сообщение")
		await delete_message(message, mes, 60)
	else:
		mes = message.reply_to_message
		if not mes.photo:
			await message.reply("Нужен реплай на фото")
			return
		file_info = await message.bot.get_file(mes.photo[0].file_id)
		file_url = "https://api.telegram.org/file/bot"+TOKEN+"/"+file_info.file_path
		print(file_url)
		await saucenao(file_url, message)
	await log(message)

@dp.message_handler(commands=["iqdb"], commands_prefix="/")
async def iqdbSearch(message: types.Message):
	if await checkUser(message) == True:
		return
	if message.chat.type == 'private':
		mes = message.reply_to_message
		if not mes.photo:
			await message.reply("Нужен реплай на фото")
			return
		file_info = await message.bot.get_file(mes.photo[0].file_id)
		file_url = "https://api.telegram.org/file/bot"+TOKEN+"/"+file_info.file_path
		print(file_url)
		await iqdb(file_url, message)
	else:
		await message.reply("Это доступно только в личных сообщениях бота")
	await log(message)

"""
Не работает потом перепишу полностью
@dp.message_handler(commands=["anime"], commands_prefix="/")
async def animeSearch(message: types.Message):
	if await checkUser(message) == True:
		return
	if not message.reply_to_message:
		mes = await message.reply("Нужен реплай сообщения")
		await delete_message(message, mes, 30)
	else:
		mes = message.reply_to_message
		file_info = await message.bot.get_file(mes.photo[0].file_id)
		file_url = "https://api.telegram.org/file/bot"+TOKEN+"/"+file_info.file_path
		file_url="https://raw.githubusercontent.com/soruly/trace.moe/master/demo.jpg"
		print(file_url)

		await anime(file_url, message)
"""