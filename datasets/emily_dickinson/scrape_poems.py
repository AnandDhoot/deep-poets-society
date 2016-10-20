from bs4 import BeautifulSoup as BS
import urllib.request
import re
from html.parser import HTMLParser
import sys, os

class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

count = 0

def signal_handler(signal, frame):
	print(str(count) + ' new poems scraped')
	sys.exit(0)

url = "http://www.poemhunter.com"

for i in range(1,32) :
	html_page = urllib.request.urlopen(url+ '/emily-dickinson/poems/page-'+str(i))
	soup_ = BS(html_page, 'html.parser')
	for link in soup_.findAll('a'):
		s = link.get('href')
		if len(str(s)) > 6 and str(s)[:6] == '/poem/':
			file = str(s).split('/')[-2]
			if os.path.isfile(file+'.txt'):
				print(file + ' file exists')
				continue
			print(file + ' file does not exist')
			html = urllib.request.urlopen(url+s).read()
			soup = BS(html, 'html.parser')
			text_file = open(file+'.txt', "w")
			text_file.write(strip_tags(str(soup.find_all('p')[1].prettify())))
			text_file.close()
			count += 1

print(str(count) + ' new poems scrapped')
