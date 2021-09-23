import speech_recognition as sr
import os
import subprocess
import asyncio
from pathlib import Path
from aiogram import types
from dispatcher import dp, bot
from .Dbmodule import GetUserVoice, AddUserVoice
from .functions import checkUser, log
#Функции распознавания голоса, проверить работоспособность позже         


# скачивание файла голосового сообщения
async def voiceFile(file: types.File, file_name: str, path: str):
	Path(f"{path}").mkdir(parents=True, exist_ok=True)
	await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")
	return


#перекодировка из огг в вав формат
async def transcibeVoice(message):
	voice = await message.voice.get_file()
	path = "download/voices/"
	await voiceFile(file=voice,
					file_name=f"{voice.file_id}.ogg",
					path=path)
	os.system("ffmpeg -i download/voices/{}.ogg download/voices/{}.wav"
			  .format(voice.file_id,
					  voice.file_id))
	return


#включение автороспознавания голосовых
@dp.message_handler(commands= ["voiceallow"], commands_prefix="/")
async def voiceallow(message:types.Message):
	if await checkUser(message) == True:
		return
	if len(message.get_args()) != 0:
		Ylist = ['1', 'true', 'True', 'Yes', 'yes', 'y', 'Y']
		Nlist = ['0', 'false', 'False', 'No', 'no', 'n', 'N']
		args = message.get_args()
		nowargs = 0
		status = 0
		if args in Ylist:
			status = True
		elif args in Nlist:
			status = False
		try:
			if GetUserVoice(message)[0] == message.from_user.id:
				nowargs = GetUserVoice(message)[1]
				if nowargs == 0 and status == False:
					await message.reply("Уже выключено")
				elif nowargs == 1 and status == True:
					await message.reply("Уже включено")
				elif nowargs == 0 and status == True:
					try:
						AddUserVoice(message, status)
					except Exception as A:
						print(A)
					await message.reply("Автораспознавание голосовых включено")
				elif nowargs == 1 and status == False:
					try:
						AddUserVoice(message, status)
					except Exception as A:
						print(A)
					await message.reply("Автораспознавание голосовых выключено")
			else: AddUserVoice(message, status)

		except IndexError:
			AddUserVoice(message, status)
	else: await message.reply("Введите аргумент")
	await log(message)

#Распознавание всех голосовых сообщений которые будут отправлены
#Если в базе данных стоит false распознавать будет только по команде
@dp.message_handler(content_types = ['voice'])
async def onvoice(message: types.Message):
	if await checkUser(message) == True:
		return
	try:
		nowargs = GetUserVoice(message)[1]
	except IndexError:
		status = True
		AddUserVoice(message, status) 
		nowargs = 1
	if nowargs == 1:
		mes= await message.reply("Начинаю распознавание...")
		try:
			await transcibeVoice(message)
			voice = await message.voice.get_file()
			r = sr.Recognizer()
			with sr.WavFile("download/voices/{}.wav".format(voice.file_id)) as source:
				#r.adjust_for_ambient_noise(source) # Optional
				audio = r.record(source)
			txt = r.recognize_google(audio, language="ru-RU")
			mes = await message.bot.edit_message_text(chat_id=message.chat.id, 
											 text=txt,
											 message_id=mes.message_id,
											 parse_mode="HTML")
			
		except sr.UnknownValueError:
			mes = await message.bot.edit_message_text(chat_id=message.chat.id,
											 text="Ошибка распознавания.",
											 message_id=mes.message_id,
											 parse_mode="HTML")
			#time.sleep(10)
			await message.bot.delete_message(chat_id=message.chat.id, message_id=mes.message_id)
			await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
		except sr.RequestError as e:
			await message.reply('Could not request results from Speech to Text service; {0}'.format(e))
		os.remove('download/voices/{}.ogg'.format(voice.file_id))
		os.remove('download/voices/{}.wav'.format(voice.file_id))
	else:
		 pass
	await log(message)


#Распознавание голоса командой
@dp.message_handler(commands= ["voice"], commands_prefix="/")
async def voice(message:types.Message):
	if await checkUser(message) == True:
		return
	if not message.reply_to_message:
		mes = await message.reply("Нужен реплай на сообщение с войсом.")
		await asyncio.sleep(10)
		await message.bot.delete_message(chat_id=message.chat.id, message_id=mes.message_id)
	else:
		repl = message.reply_to_message
		if not repl.voice:
			mes = await message.reply("Нужно ответить на голосовое сообщение")
			return
		mes = await message.reply("Начинаю распознавание...")
		try:
			await transcibeVoice(repl)
			voice = await repl.voice.get_file()
			r = sr.Recognizer()
			with sr.WavFile("download/voices/{}.wav".format(voice.file_id)) as source:
				#r.adjust_for_ambient_noise(source) # Optional
				audio = r.record(source)
			txt = r.recognize_google(audio, language="ru-RU")
			mes = await message.bot.edit_message_text(chat_id=message.chat.id, text=txt,
											  message_id=mes.message_id, parse_mode="HTML")
			
		except sr.UnknownValueError:
			mes = await message.bot.edit_message_text(chat_id=message.chat.id, text="Ошибка распознавания.",
											  message_id=mes.message_id, parse_mode="HTML")
			await asyncio.sleep(10)
			await message.bot.delete_message(chat_id=message.chat.id, message_id=mes.message_id)
		except sr.RequestError as e:
			await message.reply('Could not request results from Speech to Text service; {0}'.format(e))
		os.remove('download/voices/{}.ogg'.format(voice.file_id))
		os.remove('download/voices/{}.wav'.format(voice.file_id))
		await log(message)