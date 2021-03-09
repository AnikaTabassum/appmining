
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import os
from appmining import app

class appdownloader(object):
	def __init__(self, *args, **kwargs):
		print("initiating service")

	def whoamI(self):
		print("i am useless")

	def search(self,query):
		print("here comes search")
		res = requests.get('https://apkpure.com/search?q={}&region='.format(quote_plus(query)), headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
						  'Version/9.1.2 Safari/601.7.5 '
		}).text
		soup = BeautifulSoup(res, "html.parser")
		search_result = soup.find('div', {'id': 'search-res'}).find('dl', {'class': 'search-dl'})
		app_tag = search_result.find('p', {'class': 'search-title'}).find('a')
		print("download details ", search_result)
		print("app details ", app_tag['href'], "tayra ", app_tag['title'])
		download_link = 'https://apkpure.com' + app_tag['href']
		return download_link,  app_tag['title']

	def download(self,link):
		res = requests.get(link + '/download?from=details', headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
						  'Version/9.1.2 Safari/601.7.5 '
		}).text
		soup = BeautifulSoup(res, "html.parser").find('a', {'id': 'download_link'})
		if soup['href']:
			r = requests.get(soup['href'], stream=True, headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
							  'Version/9.1.2 Safari/601.7.5 '
			})
			with open(link.split('/')[-1] + '.apk', 'wb') as file:
				for chunk in r.iter_content(chunk_size=1024):
					if chunk:
						file.write(chunk)

	def download_apk(self,download_link):
		# download_link = appdownloader().search(app_id)
		print("download_link ", download_link)
		result=""
		if download_link is not None:

			print('Downloading {}.apk ...'.format(download_link))
			appdownloader().download(download_link)
			result='Download completed!'
			print(result)
		else:
			result='No results'
			print(result)
		print("download_apk ", result)
		return result



	# Test it
# appdownloader().download_apk('branl')