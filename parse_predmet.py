# -*- coding: UTF-8 -*-

FILLER = "[^[]/]"
STUD_URL = "https://is.muni.cz/auth/predmety/predmet.pl?id="


import urllib2
import re
from BeautifulSoup import BeautifulSoup
import get_page_c
import auth_muni
import databaze_predmetu

FAKULTY = {'Lékařská fakulta' : 1411 ,
 u'FF' : 1421 ,
 u'PrF' : 1422 ,
 u'FSS' : 1423 ,
 'Přírodovědecká fakulta' : 1431 ,
 'Fakulta informatiky' : 1433,
 'Pedagogická fakulta' : 1441 ,
 u'ESF' : 1456 ,
 u'FSpS' : 1451,
 u'CUS' : 1490}  

class DoParsePredmet:
	def __init__(self, _pid):
		
		self.pid = _pid
		
		page, url = get_page_c.get_page(STUD_URL + str(self.pid), auth_muni.username, auth_muni.password)
		self.page = page
		self.parseFakulta(page)
		#Beautiful Soup nepotřebujeme, uděláme si to regexpem
		#řeší zvrhlé ukončovací tagy
#		self.document = re.sub('(</[^<>\s]*)[^<>]*>', lambda x: x.group(1) + '>', page)
#		
#		soup = BeautifulSoup(self.document)
#		self.aplikace = soup.find('div', id='aplikace')
#	
#		identita_profil = self.aplikace.find('div', id='identita_profil')
#		skola = self.aplikace.find('div', id='skola')
#		vyuka = self.aplikace.find('div', id='vyuka')"""		
	def parseFakulta(self, text):
		try:
			self.fakulta = re.search(u"<B>([^<>/]*fakulta[^<>/]*)</B>", text, re.IGNORECASE).group(1)
		except Exception,e:
			self.fakulta=None
			self.fid=None
			return
		self.fid = FAKULTY[self.fakulta]
		
	def print_info(self):
		print u"ID předmětu:\t\t" + unicode(self.pid) + "\n"
		print "Fakulta:\t\t" + self.fakulta + "\n"
	def storetoDB(self, fajl):
		if self.pid == None or self.fid == None: return False
		a = databaze_predmetu.DB(fajl)
		a.insertInto(self.pid, self.fid)

if __name__ == "__main__":
	s = DoParsePredmet(558000)
	s.print_info()
