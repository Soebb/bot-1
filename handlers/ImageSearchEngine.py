import re
import requests
#import base64 пока что не надо
from bs4 import BeautifulSoup
from urllib import parse
from pathlib import Path


session = requests.session()
"Работает некорректно"

__all__=["saucenao",
		 "iqdb",
		 #"ascii2d"
		 #"anime"
		 ]


async def saucenao(photo_url, message):
	try:
		url="https://saucenao.com/search.php"
		#url = "https://saucenao.com"
		Header = {
			'Host': 'saucenao.com',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
			 'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, * / *;q = 0.8',
			'Accept - Language': 'zh - CN, zh;q = 0.8, zh - TW;q = 0.7, zh - HK;q = 0.5, en - US;q = 0.3, en;q = 0.2',
			 'Accept - Encoding': 'gzip, deflate, br',
			'Connection': 'keep - alive',
		}  
		payloaddata = {
			'frame': 1,
			'hide': 0,
			'database': 999,
		}
		#files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
		photo_file=requests.get(photo_url)
		files = {"file": (
		"saucenao.jpg", photo_file.content, "image/png")}
		mes = await message.reply("Поиск на saucenao")
		r = session.post(url=url, headers=Header, data=payloaddata,files=files)
		#r = session .get(url=url,headers=Header)
		soup = BeautifulSoup(r.text, 'html.parser')
		#print(soup.prettify())
		result=0
		choice=0
		for img in soup.find_all('div', attrs={'class': 'result'}):  # 找到class="wrap"的div里面的所有<img>标签
			#print(img)
			if('hidden' in str(img['class']))==False:
				try:
					name=img.find("div",attrs={'class': 'resulttitle'}).get_text()
					img_url=str(img.img['src'])
					describe_list=img.find("div",attrs={'class': 'resultcontentcolumn'})
					url_list = img.find("div", attrs={'class': 'resultcontentcolumn'}).find_all("a",  attrs={'class': 'linkify'})
					similarity = str(img.find("div", attrs={'class': 'resultsimilarityinfo'}).get_text())
					#print(name)
				except:
					continue
				try:
					describe = str(url_list[0].previous_sibling.string)
					describe_id = str(url_list[0].string)
					describe_url = str(url_list[0]['href'])
					author_url = str(url_list[1]['href'])
					author = str(url_list[1].previous_sibling.string)
					author_id = str(url_list[1].string)
					'''print(name)
					print(img_url)
					print(describe)
					print(describe_id)
					print(similarity)
					print(auther)
					print(auther_id)
					print(describe_url)'''
					text = f"{name}\n{describe}[{describe_id}]({describe_url})\n{author}:[{author_id}]({author_url})\nсходство{similarity}"
				except:
					'''print(describe_list.get_text())
					print(describe_list.strong.string)
					print(describe_list.strong.next_sibling.string)
					print(describe_list.small.string)
					print(describe_list.small.next_sibling.next_sibling.string)'''
					author = str(describe_list.strong.string)
					author_id = str(describe_list.strong.next_sibling.string)
					describe = str(describe_list.small.string) + "\n" + str(describe_list.small.next_sibling.next_sibling.string)
					text = f"{name}\n{author}:{author_id}\n{describe}\nсходство{similarity}"
				photo_file = session.get(img_url)
				await message.bot.send_photo(chat_id=message.chat.id,photo=photo_file.content,parse_mode='Markdown',caption=text)
				result=1
		if result==0:
			await message.reply("saucenao не нашел")
	except:
		print("saucenao")


async def iqdb(photo_url, message):
	try:
		await message.bot.send_message(chat_id=message.chat.id, text="Поиск на iqdb", parse_mode="MarkdownV2")
		url = "http://iqdb.org/"
		# url = "https://saucenao.com"
		photo_file = requests.get(photo_url)
		files = {"file": ("iqdb.jpg", photo_file.content, "image/png")}
		# files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}

		r = requests.post(url=url, files=files)
		#print(r.text)
		soup = BeautifulSoup(r.text, 'html.parser')
		a=1
		for img in soup.find_all('td', attrs={'class': 'image'}):  # 找到class="wrap"的div里面的所有<img>标签
			#print(img)
			if a==7:
				break
			try:
				#print(img.a.get('href'))
				img_html=img.a.get('href')
				if "http:" not in img_html and "https:" not in img_html:

					img_html="https:"+img_html

				img_url="http://iqdb.org"+img.img.get('src')

				text=f"[Детали изображения]({img_html})"
				photo_file = session.get(img_url)
				await message.bot.send_photo(chat_id=message.chat.id, photo=photo_file.content, parse_mode='Markdown', caption=text)
				a=a+1
			except:
				None
	except:
		None

'''
async def ascii2d(photo_url, message):
	try:
		url = "https://ascii2d.net/"
		# url = "https://saucenao.com"
		Header = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
		}
		html = session.get(url, headers=Header)
		print(html)
		authenticity_token = re.findall("<input type=\"hidden\" name=\"authenticity_token\" value=\"(.*?)\" />", html.text, re.S)[0]
		payloaddata = {

			'authenticity_token': authenticity_token,
			'utf8': "✓",
		}
		# files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
		await message.reply("Поиск на ascii2d")
		photo_file = requests.get(photo_url)
		files = {"file": (
			"saucenao.jpg", photo_file.content, "image/png")}
		url = "https://ascii2d.net/search/multi"
		r = session.post(url=url, headers=Header, data=payloaddata, files=files)
		soup = BeautifulSoup(r.text, 'html.parser')
		# print(soup.prettify())
		pan = 0
		for img in soup.find_all('div', attrs={'class': 'row item-box'}):  # 找到class="wrap"的div里面的所有<img>标签
			# print(img)
			if pan != 0:
				img_url = "https://ascii2d.net" + str(img.img['src'])
				the_list = img.find_all('a')
				title = str(the_list[0].get_text())
				title_url = str(the_list[0]["href"])
				auther = str(the_list[1].get_text())
				auther_url = str(the_list[1]["href"])

				photo_file = session.get(img_url)
				text=f"titile:[{title}]({title_url})\nauther:[{auther}]({auther_url})"
				message.bot.send_photo(chat_id=message.chat.id, caption=text, parse_mode='Markdown',photo=photo_file.content)
			pan = pan + 1
			if pan == 3:
				break
	except:
		print("ascii2d faild")
'''


'''Не работает потом перепишу полностью
async def anime(photo_url, message):
	try:
		url = "https://trace.moe/api/search"
		# url = "https://saucenao.com"
		photo_file = requests.get(photo_url)
		print()
		ls_f = base64.b64encode(photo_file.content)

		data = {
			"image": ls_f,
		}
		# files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}

		r = session.post(url=url, data=data)
		print(r)

		# r = session .get(url=url,headers=Header)
		await message.bot.send_message(chat_id=message.chat.id,text="Поиск на trace.moe")
		information = r.json()
		print(information)
		anilist_id = information['docs'][0]["anilist_id"]
		filename = information['docs'][0]['filename']
		tokenthumb = information['docs'][0]['tokenthumb']
		at = information['docs'][0]['at']
		limit = information['limit']
		limit_ttl = information['limit_ttl']
		title = information['docs'][0]['title_chinese']
		episode = information['docs'][0]['episode']
		quota = information['quota']
		quota_ttl = information['quota_ttl']
		similarity=information['docs'][0]['Сходство']
		similarity_num="%.2f%%" % (similarity * 100)
		img_url = f"https://trace.moe/thumbnail.php?anilist_id={anilist_id}&file={parse.quote(filename)}&t={at}&token={tokenthumb}"
		print(img_url)
		video_url = f"https://trace.moe/preview.php?anilist_id={anilist_id}&file={parse.quote(filename)}&t={at}&token={tokenthumb}"
		print(video_url)
		video = f"https://media.trace.moe/video/{anilist_id}/{parse.quote(filename)}?t={at}&token={tokenthumb}"
		print(video)
		more_url = f"https://anilist.co/anime/{anilist_id}"
		text = f"""{similarity_num}
		Title:{title}\nЭпизод:{episode}
		Время：{datetime.timedelta(seconds=int(at))}\nИсточник：{filename}
		[Больше информации]({more_url})
		Осталось поисков в минутах:{limit}
		Оставшееся время сброса в минутах:{limit_ttl}s
		24 Осталось поисков через час:{quota}
		24 Оставшееся время сброса в часах:{datetime.timedelta(seconds=int(quota_ttl))}"""
		print(text)
		photo_file = session.get(img_url)
		await message.bot.send_photo(chat_id=message.chat.id, photo=photo_file.content, parse_mode='Markdown', caption=text)
		photo_file = session.get(video)
		await message.bot.send_video(chat_id=message.chat.id,data=photo_file.content)
	except:
		print("anime failed")'''