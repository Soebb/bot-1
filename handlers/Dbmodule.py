import sqlite3
import sys
import datetime
from pathlib import Path
sys.path.insert(0, 'C:/Users/Legion/Desktop/bot/')
from config import DBNAME, LOGDBNAME, MYID


__all__=["sqlite_connect",
		 "UserAddDatabase",
		 "UserGetDatabase",
		 "AddUserVoice",
		 "GetUserVoice",
		 "addUserBlackList",
		 "getUserBlackList",
		 "logs",
		 "inlineLogs",]


def sqlite_connect():
	connect = sqlite3.connect(DBNAME, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
	connect.execute("pragma journal_mode=wal;")
	#print(f"{DBNAME} connected") отладка подключения к БД
	return connect

def sqlite_connectlogs():
	connect = sqlite3.connect(LOGDBNAME, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
	connect.execute("pragma journal_mode=wal;")
	#print(f"{DBNAME} connected") отладка подключения к БД
	return connect

#Черный список бота
def addUserBlackList(message, status):
	connect = sqlite_connect()
	cursor = connect.cursor()
	try:   
		cursor.executemany("INSERT INTO BlackList VALUES (?,?)", 
					 [(message.from_user.id, status)])
	except Exception as A:
		cursor.executemany("UPDATE users SET status=? WHERE user_id=?",
						   [(status, message.from_user.id)])
		print(f"{message.from_user.username} пользователь добавлен в БД {DBNAME} таблицу BlackList",)
	connect.commit()
	connect.close()


def getUserBlackList(message):
	connect = sqlite_connect()
	cursor = connect.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS 
	BlackList(
	user_id INTEGER UNIQUE
	NOT NULL,
	status BOOLEAN)""")
	cursor.execute("SELECT * FROM BlackList WHERE user_id=?",
				[(message.from_user.id)])
	results = cursor.fetchall()
	connect.close()
	return results[0]


#Добавлению в таблицу пользователей
def UserAddDatabase(message, stat=None):
	connect = sqlite_connect()
	cursor = connect.cursor()
	try:   
		cursor.executemany("INSERT INTO users VALUES (?,?,?,?,?)", 
					 [(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, stat)])
	except Exception as A:
		cursor.executemany("UPDATE users SET username=? WHERE user_id=?", 
						   [(message.from_user.username, message.from_user.id)])
		cursor.executemany("UPDATE users SET user_first_name=? WHERE user_id=?",
						   [(message.from_user.first_name, message.from_user.id)])
		cursor.executemany("UPDATE users SET user_last_name=? WHERE user_id=?",
						   [(message.from_user.last_name, message.from_user.id)])
		if stat is not None:
			cursor.executemany("UPDATE users SET Chat_status=? WHERE user_id=?",
							   [(stat, message.from_user.id)])
		if message.from_user.username is not None:
			print(f"{message.from_user.username} пользователь добавлен в БД {DBNAME}",)
		else: print(f"{message.from_user.first_name} пользователь добавлен в БД {DBNAME}",)
	connect.commit()
	connect.close()


def UserGetDatabase(message):
	connect = sqlite_connect()
	cursor = connect.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS 
		users(
		user_id INTEGER UNIQUE 
		NOT NULL,
		username TEXT UNIQUE, 
		user_first_name TEXT NOT NULL, 
		user_last_Name TEXT, 
		Chat_status STRING NOT NULL)""")
	cursor.execute("SELECT * FROM users WHERE user_id=?", 
				   [(message.from_user.id)])
	results = cursor.fetchall()
	connect.close()
	return results[0]


#Автораспознавание голосовых
def AddUserVoice(message, status):
	connect = sqlite_connect()
	cursor = connect.cursor()
	try:
		cursor.executemany("INSERT INTO voiceallow VALUES (?,?)", 
					   [(message.from_user.id, status)])
		print('DATABASE: USER {} ADDED [voiceallow]'
			  .format(message.from_user.username))
		connect.commit()

	except Exception as A:
		cursor.executemany("UPDATE voiceallow SET status=? WHERE user_id=?", 
						   [(status, message.from_user.id)])
	connect.commit()
	connect.close()


def GetUserVoice(message):
	connect = sqlite_connect()
	cursor = connect.cursor()
	cursor.execute("""CREATE TABLE IF NOT EXISTS voiceallow(
	user_id INTEGER UNIQUE 
	NOT NULL, 
	status BOOLEAN NOT NULL)""")
	cursor.execute("SELECT * FROM voiceallow WHERE user_id=?", 
				   [(message.from_user.id)])
	results = cursor.fetchall()
	connect.close()
	return results[0]

def logs(message):
	connect = sqlite_connectlogs()
	cursor = connect.cursor()
	semi = [(str(datetime.datetime.now().strftime("%d.%m.%y %H:%M")), str(message.from_user.username),
		  str(message.text), str(message.chat.type))]
	cursor.execute("""CREATE TABLE IF NOT EXISTS 
	logs(
	time STRING,
	nickname STRING,
	command STRING,
	chat STRING)""")
	cursor.executemany("INSERT INTO logs(time, nickname, command, chat) VALUES (?, ?, ?, ?)", semi)
	connect.commit()
	connect.close()


def inlineLogs(inline_query):
	connect = sqlite_connectlogs()
	cursor = connect.cursor()
	semi = [(str(datetime.datetime.now().strftime("%d.%m.%y %H:%M")), str(inline_query.from_user.username),
		  str(inline_query.query), str(inline_query.chat_type))]
	cursor.execute("""CREATE TABLE IF NOT EXISTS 
	logs(
	time STRING,
	nickname STRING,
	command STRING,
	chat STRING)""")
	cursor.executemany("INSERT INTO logs(time, nickname, command, chat) VALUES (?, ?, ?, ?)", semi)
	connect.commit()
	connect.close()


#Пробуем подключить БД, если не существует создаем 
db = Path("./Database/database.db")
try:
	db.resolve(strict=True)
except FileNotFoundError:
	print("Database not found, trying to create a new one.")
try:
	sqlite_connect()
except Exception as e:
	print("Error when creating database : ", e.__repr__(), e.args)
	pass
else:
	print("Success.")