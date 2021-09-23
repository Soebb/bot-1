import re
from uuid import uuid4
from aiogram import types
from colorama import Fore, Back
from colorama import init
from dispatcher import dp, bot
from .functions import checkUser, InlineLog
from youtube_search import YoutubeSearch


init(autoreset=True)


#функции для поиска по ютюбу(в основном инлайн)
def youTube(word="cybeer", max_res=5):
    result = YoutubeSearch(word, max_res).to_dict()
    return result


def inlineYouTube(inline_query):
	query = inline_query.query
	query = re.sub(r'^\W*\w+\W*', '', query)
	cbans = youTube(query)
	if cbans != []:
			return [types.InlineQueryResultArticle(
				id= str(uuid4()), title=cbans[i]['title'],
				input_message_content=types.InputTextMessageContent(f"youtube.com{cbans[0]['url_suffix']}"), thumb_url=cbans[i]['thumbnails'][0]
				) for i in range(len(cbans))]
	else:
		cb = inline_query.from_user
		if cb.last_name:
			user = f"{cb.first_name} {cb.last_name}"
		else:
			user = cb.first_name
		return [types.InlineQueryResultArticle(
				id= str(uuid4()), title="Нет текста для поиска",
				input_message_content=types.InputTextMessageContent(f"Я, {user}, нажимаю бесполезные кнопки."),
				description="Пример запроса:\nyt cats", thumb_url="https://image.flaticon.com/icons/png/512/3572/3572260.png"
				),]

@dp.inline_handler()
async def yt_search(inline_query: types.InlineQuery):
	if await checkUser(inline_query) == True:
		return
	else:
		await bot.answer_inline_query(inline_query.id, inlineYouTube(inline_query), cache_time=20)	
	await InlineLog(inline_query)
		