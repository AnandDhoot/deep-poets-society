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

# count = 0

def signal_handler(signal, frame):
	print(str(count) + ' new poems scraped')
	sys.exit(0)

url = "https://www.poets.org/poetsorg/poems"

html_page = urllib.request.urlopen(url)
soup_ = BS(html_page, 'html.parser')

for link in soup_.findAll('a'):
	s = link.get('href')
		print(s)

	file = str(s).split('/')[-1]
	if os.path.isfile(file+'.txt'):
		print(file + ' file exists')
		continue

	print(file + ' file does not exist')
	if len(str(s)) > 15 and str(s)[:15] == '/poetsorg/poem/':
		print(url+s)
		html = urllib.request.urlopen(url+s).read()
		soup = BS(html, 'html.parser')
		text_file = open(file+'.txt', "w")
		text_file.write(strip_tags(str(soup.select('h2')[0]) + '\n'))
		text_file.write(strip_tags(str(soup.select('pre')[0])))
		text_file.close()
		count += 1

os.remove('for_her.txt')
os.remove('for_him.txt')

print(str(count) + ' new poems scrapped')