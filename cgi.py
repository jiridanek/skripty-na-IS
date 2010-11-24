#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import xml.dom.minidom
import databaze_predmetu
import parse_predmet

import re
#cgitb.enable()

OBDOBI = "podzim2010"
DBFILE = 'predmety.db'
STUDIJNI_MATERIALY="https://is.muni.cz/auth/student/studijni_materialy.pl"

class Predmet:
	def __init__(self, jmeno="", kod="", pid=0, ucebna=[("",0)], od="", do="", den=""):
		self.jmeno = jmeno
		self.kod = kod
		self.ucebna = ucebna
		self.od = od
		self.do = do
		self.den = den
		self.pid = pid

		self.base_predmet_url = "https://is.muni.cz/auth/predmety/predmet.pl?id="
		self.base_ucebna_url="https://is.muni.cz/auth/kontakty/mistnost.pl?id="
		self.template_materialy_url = "https://is.muni.cz/auth/dok/rfmgr.pl?furl=/el/{fakulta}/{obdobi}/" + self.jmeno + "/" #{predmet}/"
	def download_info(self):
		self.fid = databaze_predmetu.DB(DBFILE).findFid(self.kod)
		if self.fid: return
		parse = parse_predmet.DoParsePredmet(self.pid)
		self.fid = parse.fid
		parse.storetoDB(DBFILE)
	def to_div(self):
		pass
	def get_predmet_url(self):
		return self.base_predmet_url + str(self.pid)
	def get_ucebna_url(self):
		return map(lambda u:(u[0], self.base_ucebna_url + str(u[1])),self.ucebna)
	def get_materialy_url(self):
		import string
		f = string.Formatter
		return f.format(template_materialy_url, fakulta = "", obdobi = OBDOBI)
	def get_odcas_s(self):

		m = re.match("([0-9]*):([0-9]*)", self.od)
		return int(m.group(1))*60*60 + int(m.group(1))*60
	def get_docas_s(self):

		m = re.match("([0-9]*):([0-9]*)", self.do)
		return int(m.group(1))*60*60 + int(m.group(1))*60
#FIXME TODO
def dira(radek, predmet):
	predmety = sorted(radek, key=lambda x:x.get_odcas_s())
	for index,predmet in enumerate(predmety):
		if predmet.get_odcas_s() > predmet.get_odcas_s():
			break
#		if not index +1 == length (predmety): pass

def group_by(co, podle_ceho):
	grupy={}
	grupa=[]
	for i in sorted(co, key=podle_ceho):
		if grupa == [] or podle_ceho(grupa[-1]) == podle_ceho(i):
			grupa.append(i)
		else:
			grupy[podle_ceho(grupa[0])]=grupa
			grupa = []
	if not grupa == []:
		grupy[podle_ceho(grupa[0])] = grupa
	return grupy

###
#def drill_down(kam, s_cim):
#	if kam.__class__ == [].__class__ && len(kam) == 0 or kam.__class__ == [].__class__ && not kam[0].__class__ == [].__class__:
#		return s_cim(kam)
#	for i in kam:
#		if 
###

class Den:
	def __init__(self, kod=""):
		self.kod = kod
		self.predmety=[]
		self.radky=[]
	def pridej_predmet(predmet):
		pass
#	def 

class Rozvrh:
	def __init__(self, ):
		self.po = Den(u"Po")
		self.ut = Den(u"Út")
		self.st = Den(u"St")
		self.ct = Den(u"Čt")
		self.pa = Den(u"Pá")
		self.na = Den(None)
	def pridej_predmet(self, predmet):
		if(predmet.den == self.po.kod) : self.po.pridej_predmet(predmet)
		if(predmet.den == self.ut.kod) : self.po.pridej_predmet(predmet)
		if(predmet.den == self.st.kod) : self.po.pridej_predmet(predmet)
		if(predmet.den == self.ct.kod) : self.po.pridej_predmet(predmet)
		if(predmet.den == self.pa.kod) : self.po.pridej_predmet(predmet)
		if(predmet.den == self.na.kod) : self.po.pridej_predmet(predmet)
	def jako_div():
		pass

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

#form = cgi.FieldStorage()
#if "xmlko" not in form:
#    print "<H1>Error</H1>"
#    print "ÂŽĂĄdnĂ˝ rozvrh ke zpracovĂĄnĂ­."

fajl = open("rozvrh.xml")
doc = xml.dom.minidom.parseString(fajl.read())

predmety = []

if False:
	pass
else:
	#doc = xml.dom.minidom.parseString(form["xmlko"])
	
	for predmet in doc.getElementsByTagName("akce"):
		kod = predmet.getElementsByTagName("kod")[0].firstChild.toxml()
		nazev = predmet.getElementsByTagName("nazev")[0].firstChild.toxml()
		predmetid = predmet.getElementsByTagName("predmetid")[0].firstChild.toxml()
		slot = predmet.parentNode
		odcas = slot.getAttribute("odcas")
		docas = slot.getAttribute("docas")
		if len(slot.getElementsByTagName("mistnost")) > 0:
			mistnost = slot.getElementsByTagName("mistnost")[0].firstChild.toxml()
			mistnostid = slot.getElementsByTagName("mistnostid")[0].firstChild.toxml()
		else:
			mistnost = None
			mistnostid = None
		den = slot.parentNode.parentNode
		try:
			denid = den.getAttribute("id")
		except Exception,e:
			denid = None
		
		p = Predmet(nazev, kod, predmetid, [(mistnost, mistnostid)], odcas, docas, denid)
		predmety.append(p)

if __name__ == "__main__":
	for p in predmety:
		p.download_info()
