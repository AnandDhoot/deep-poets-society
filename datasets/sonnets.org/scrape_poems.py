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

url = "http://sonnets.org/"

html_page = urllib.request.urlopen(url + 'alpha.htm')
soup_ = BS(html_page, 'html.parser')
for link in soup_.findAll('a'):
	s = link.get('href')
	if str(s) not in ['index.htm', "http://webstats.motigo.com/", "bartlett.htm", "ayres.htm", "bateskl.htm", "bevingtn.htm", "blind.htm", "bruner.htm", "constable.htm", "dobell.htm", "dobson.html", "drummond.htm", "fletcher.htm", "hillyer.htm", "hucks.htm", "jones.htm", "lazarus.htm", "lodge.htm", "logan.htm", "lok.htm", "longmore.htm", "mccall.htm", "nelson.htm", "perry.htm", "polwhele.htm", "prestonm.htm", "seeger.htm", "wwi.htm#shillito", "sotheby.htm", "stewart.htm"]:
		file = str(s).split('.')[0]
		if os.path.isfile(file+'.txt'):
			print(str(s) + ' file exists')
			continue
		print(str(s) + ' file does not exist')

		html = urllib.request.urlopen(url + str(s))
		soup = BS(html, 'html.parser')

		text_file = open(file+'.txt', "w")
		text_file.write( strip_tags( str(soup.find_all('p')[2]) ) )
		text_file.close()
		count += 1


print(str(count) + ' new poems scrapped')
