import play_scraper
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import bs4
# result= play_scraper.collection(
#         collection='TRENDING',
#         category='BOOKS_AND_REFERENCE',
#         results=20,
#         page=2)

# print(result)
# print(play_scraper.categories())
# 'url': 'https://play.google.com/store/apps/category/GAME_ADVENTURE
# res = requests.get('https://play.google.com/store/apps/category/GAME_ADVENTURE').text
# soup = BeautifulSoup(res, "html.parser")
# # search_result = soup.find('div', {'class': 'wSaTQd'}).find('dl', {'class': 'search-dl'})
# print(soup)
# print(search_result)
# print(play_store.search('google chrome'))
company_name="airbnb"
r = requests.get("https://play.google.com/store/apps/category/GAME_ADVENTURE")
soup = bs4.BeautifulSoup(r.text, "html.parser")
subtitles = soup.findAll("a")
idp=0
dev_urls = []

for title in subtitles:
	idp+=1
	# print("lisa ", title['href'])
	hrefs=title['href']
	title=str(title)
	stt="/store/apps/details?id="

	idx=hrefs.find(stt)
	index=idx+len(stt)
	# print("index ", index, hrefs)
	# print("asa ", hrefs[index:len(hrefs)])
	appid=hrefs[index:len(hrefs)]
	# print("apps ", appid)
	tempdict={idp:appid}
	dev_urls.append(appid)

finalVal=[]
for vals in dev_urls:
	if vals.startswith('com'):
		# print(vals)
		if vals in finalVal:
			temp="nothing imort"
		else:
			finalVal.append(vals)

# print(finalVal)
# print(dev_urls[130])
# print(play_scraper.details('com.android.chrome')['description_html'])
print(play_scraper.details('com.bl.critical.strike')['description_html'])
# for val in finalVal:
# 	print(play_scraper.details(val)['description_html'])