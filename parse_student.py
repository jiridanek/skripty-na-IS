# -*- coding: UTF-8 -*-

FILLER = "[^[]/]"
#nebo "https://is.muni.cz/auth/osoba/"
STUD_URL = "https://is.muni.cz/auth/lide/?uco="


import urllib2
import re
from BeautifulSoup import BeautifulSoup
import get_page_c
import auth_muni

class DoParseStudentInfo:
	def __init__(self, _uco):
		
		self.uco = _uco
		
		page, url = get_page_c.get_page(STUD_URL + str(self.uco), auth_muni.username, auth_muni.password)
		
		#řeší zvrhlé ukončovací tagy
		self.document = re.sub('(</[^<>\s]*)[^<>]*>', lambda x: x.group(1) + '>', page)
		
		soup = BeautifulSoup(self.document)
		self.aplikace = soup.find('div', id='aplikace')
		
		
		identita_profil = self.aplikace.find('div', id='identita_profil')
		skola = self.aplikace.find('div', id='skola')
		vyuka = self.aplikace.find('div', id='vyuka')
		
		self.parseIdentitaProfil(identita_profil)
		self.parseSkola(skola)
		self.parseVyuka(vyuka)
	
	def parseIdentitaProfil(self, _i_p):
		
		self.name = _i_p.find('h2').string.strip()
		try:
			self.status = _i_p.find('div', id='status').string.strip()
		except:
			self.status = None
		
		try:
			self.web = _i_p.find('div', id='web').a.string.strip()
		except:
			self.web = None
		
		#více e-mailů, taky nemusí být žádný
		try:
			self.email = [i.a.strip() for i in _i_p.findAll('div', id='email')]
		except:
			self.email=[]
		#;-)
		
		fotourl = "https://is.muni.cz/auth/lide/foto.pl?uco=" + str(self.uco)
		self.fotourl = get_page_c.dump_url(fotourl, auth_muni.username, auth_muni.password)
		self.logotitle = _i_p.find('div', id='os_logo').img["alt"].strip()
		
		logourl = "https://is.muni.cz" + _i_p.find('div', id='os_logo').img["src"].strip()
		self.logourl = get_page_c.dump_url(logourl, auth_muni.username, auth_muni.password)
	
	#vezmeme si jen názvy oborů a akt. semestr
	def parseSkola(self, _s):
		self.studia=[]
		
		#Tohle se stane u Decka. Mel bych se mrknout, o co tady de....
		if _s == None:
			return
		
		studium_text = _s.findAll('div', 'studium_text')
		if studium_text == None:
			return
		for studium in studium_text:
			s = {}
			s["obor"] = studium.find(text=re.compile("Obor:", re.I)).next.string.strip()
			#Semestr: , Ročník/Blok/Cyklus
			try:
				s["srbc"] = studium.find(text=re.compile("Semestr:", re.I)).string.strip()
				s["semestr"] = re.search("([0-9]+).*", s["srbc"], re.I).group(1)
			except:
				s["srbc"] = None
				s["semestr"] = None
			
			self.studia.append(s)
		
	def parseVyuka(self, _v):
		self.vyuka = []
		if _v == None or len(_v) <= 0:
			 return
		odkazy = _v.findAll('a')
		if odkazy == None or len(odkazy) <= 0:
			 return
		odk = "https://is.muni.cz/" + "/".join(odkazy[0]['href'].split("/")[1:])
		odk_text = odkazy[0].string + " <b>(&#8734;)</b>"
		self.vyuka.append((odk, odk_text))
		for o in odkazy[1:]:
			odk = "http://is.muni.cz/" + "/".join(o['href'].split("/")[2:])
			odk_text = o.string
			self.vyuka.append((odk, odk_text))
	
		
	def print_info(self):
		print u"Jméno:\t\t" + unicode(self.name) + "\n"
		print u"Status:\t\t" + self.status + "\n"
		#print u"Web:\t\t" + self.web + "\n"
		#print u"E-mail:\t\t" + self.email + "\n"
		print u"Foto:\t\t" + self.fotourl + "\n"
		print u"Fakulta:\t\t" + self.logotitle
		self.logourl
if __name__ == "__main__":
	s = DoParseStudentInfo(151353)
	s.print_info()
