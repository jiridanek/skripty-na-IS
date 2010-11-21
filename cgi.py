#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import xml.dom.minidom
#cgitb.enable()

class Predmet:
	def __init__(self, jmeno="", kod="", id=0, ucebna=("",0), od="", do="", den=""):
		self.jmeno = jmeno
		self.kod = kod
		self.ucebna = ucebna
		self.od = od
		self.do = do
		self.den = den
	def to_div():
		pass
		
def group_by(co, podle_ceho):
	grupy=[]
	grupa=[]
	for i in sorted(co, key=podle_ceho):
		if grupa == [] or podle_ceho(grupa[-1]) == podle_ceho(i):
			grupa.append(i)
		else:
			grupy.append(grupa)
			grupa = []
	if not grupa == []:
		grupy.append(grupa)
	return grupy

###
#def drill_down(kam, s_cim):
#	if kam.__class__ == [].__class__ && len(kam) == 0 or kam.__class__ == [].__class__ && not kam[0].__class__ == [].__class__:
#		return s_cim(kam)
#	for i in kam:
#		if 
###

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

#form = cgi.FieldStorage()
#if "xmlko" not in form:
#    print "<H1>Error</H1>"
#    print "®ádný rozvrh ke zpracování."

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
		
		p = Predmet(nazev, kod, predmetid, (mistnost, mistnostid), odcas, docas, denid)
		predmety.append(p)
	
