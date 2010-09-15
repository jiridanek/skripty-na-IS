# -*- coding: UTF-8 -*-

FILLER = "[^[]/]"
FIND_URL = "https://is.muni.cz/auth/lide/?searchid="

import urllib2
import re
from BeautifulSoup import BeautifulSoup
import urllib
import get_page_c
import auth_muni


# Projde jen první stránku výsledků
class DoFindStudent:
	def __init__(self, _query):
		page, url = get_page_c.get_page(FIND_URL + urllib.quote_plus(_query) + '&Hledat=Hledat', auth_muni.username, auth_muni.password)

		#řeší zvrhlé ukončovací tagy
		self.document = re.sub('(</[^<>\s]*)[^<>]*>', lambda x: x.group(1) + '>', page)
		
		soup = BeautifulSoup(self.document)
		self.aplikace = soup.find('div', id='aplikace')
		
		
		
		if self.aplikace.find('div', id='identita_profil') != None:
			uco = re.search("/osoba/(\w+)", url).group(1)
			self.lidi=[{'uco':uco}]
			return 
		
		lista = self.aplikace.find('div', id='lista')
		
		if self.aplikace.ul == None:
			self.lidi = None
			return None
		self.lidi = []
		for li in self.aplikace.ul('li'):
			clovek = {}
			clovek['name'] = li.a.string.strip()
			#není to bezpečný
			a = li.find(text=re.compile(u'učo'))
			try:
				clovek['uco'] = re.search("(\w{6})", a).group(1)
			except:
				clovek['uco'] = None
			try:
				clovek['zarazeni'] = li.span['class'].strip()
			except:
				clovek['zarazeni'] = None
			self.lidi.append(clovek)
if __name__ == "__main__":
	s = DoFindStudent('Michal Zlatkovský')
	print s.lidi
