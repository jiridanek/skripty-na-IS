#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import shutil
import codecs
import datetime

import urllib2
import re

import parse_student
import find_student
import auth_muni
import urllib

base_url="http://prvakoviny.dnk.cz"

def priprav_prostredi(_cache, _vysledek, _gfx):
	if not os.path.isdir(_cache):
		os.mkdir(_cache)
	if not os.path.isdir(_vysledek):
		os.mkdir(_vysledek)
	if not os.path.isdir(_gfx):
		os.mkdir(_gfx)
def presun_vysledek(_trida, _gfx, _vysledek):
	if not os.path.isdir(_vysledek):
		raise Exception("slozka neexistuje: " + _vysledek)
	if not os.path.isfile("index.html"):
		raise Exception("soubor neexistuje: index.html")
	os.mkdir(_vysledek+os.sep+_trida)
	shutil.move("index.html", _vysledek+os.sep+_trida+os.sep)
	shutil.move(_gfx, _vysledek + os.sep + _trida)
def zpracuj_tridu(_tridy,_trida, _lidi):
	o = codecs.open('index.html', mode='w', encoding="utf-8")
	print >>o,u'''
<!DOCTYPE html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="../screen.css">
<title>Spolužáci na Masarykově univerzitě</title>

</head>
<body>

<div id="fb-root"></div>
<script>
  window.fbAsyncInit = function() {
    FB.init({appId: 'your app id', status: true, cookie: true,
             xfbml: true});
  };
  (function() {
    var e = document.createElement('script'); e.async = true;
    e.src = document.location.protocol +
      '//connect.facebook.net/en_US/all.js';
    document.getElementById('fb-root').appendChild(e);
  }());
</script>


<h1 align="center">Spolužáci na <i>MUNI</i></h1>'''
	print >>o, '''<h6 align="center"><i>Ke dni: ''' + str(datetime.date.today()) + '''</i></h6>'''
	print >>o, '''<ul class="menu">'''
	print >>o, u'''<li><a class="first" href="''' + str(base_url.decode('utf-8')) + u'''/''' + str(_tridy[0].decode('utf-8')) + u'''/">''' + str(_tridy[0].decode('utf-8')) + u'''</a></li>'''
	for t in _tridy[1:]:
		print >>o, u'''<li><a class="a" href="''' + base_url + u'''/''' + t.decode('utf-8') + u'''/">''' + t.decode('utf-8') + u'''</a></li>'''
	#print >>o, u'''<li><a class="a" href="http://zdrojak.root.cz">Zdroják </a></li>'''
	print >>o, u'''
</ul>

<iframe src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fprvakoviny.dnk.cz&amp;layout=standard&amp;show_faces=true&amp;width=450&amp;action=like&amp;colorscheme=light&amp;height=80" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:450px; height:80px;" allowTransparency="true"></iframe>

<a class = "a b" href="http://muni.dnk.cz/zdrojak.zip">;-)</a>'''
	for line in _lidi:
		print >>o,u'''<div class="clovek">'''
		name = line.strip()
		print >>o,u'''<h3>''' + name.decode("utf-8") + u'''</h3>'''
	
		s = find_student.DoFindStudent(name)
		if s.lidi == None:
			print >>o,u'''<div class="zaznam"><span class="error">NIC NENALEZENO</span></div>'''
		else:
			i = 0
			for l in s.lidi:
				if l.has_key('uco') and l['uco'] != None:
					if i % 2 == 0:
						print >>o,u'''<hr>'''
					i = i+1
					print >>o,u'''<div class="zaznam">'''
	#				print l['uco']
					info = parse_student.DoParseStudentInfo(l['uco'])
				
					try:
						jmeno = info.name
					except:
						jmeno = "..."
				
				
					print >>o,u'''<h4><img src="''' + info.logourl + '''"><a href="http://is.muni.cz/osoba/''' + l['uco']+ '''">''' + jmeno + '''</a> <a href="https://is.muni.cz/auth/osoba/''' + l['uco']+ '''">(&#8734;)</a></h4>'''
					print >>o,u'''<img src="''' + info.fotourl + '''"><div'''
					
					print >>o, u'''<h5>Studium:</h5>''' 
					print >>o,u'''<ul>'''
					
					for studium in info.studia:
						print >>o,u'''<li><b>''' + studium['obor'] + '''</b>'''
						try:
							print >>o,u'''<i>semestr: ''' + studium['semestr'] + '''</i>.<br>'''
						except:
							pass
						print >>o,u'''</li>'''
					print >>o,u'''</ul>'''
					
					if len(info.vyuka) > 0:
						print >>o, u'''<h5>Výuka:</h5>''' 
						print >>o,u'''<ul>'''
					
					for uka in info.vyuka:
						try:
							odk, odk_text = uka
							print >>o,u'''<li><a href="''' + odk + '''">''' + odk_text + '''</a>'''
						except:
							pass
					if len(info.vyuka) > 0:
						print >>o,u'''</ul>'''
					
					print >>o,u'''</div>'''
					print >>o,u'''</div>'''	
				
				else:
					info = None
			
			
	#		print "="
		print >>o,u'''</div>'''
	print >>o,u'''
	</body>
	</html>
	'''

	o.close()




try:
	target_slozka = os.path.abspath(sys.argv[1])
except:
	raise Exception("Parametrem je složka se seznamy studentů")

if not os.path.isdir(target_slozka):
	raise IOError("Složka neexistuje: " + target_slozka)

tridy = []
for f in os.listdir(target_slozka):
	fi = target_slozka + os.sep + f
	if not os.path.isfile(fi):
		continue
	jmeno = ".".join(f.split(".")[:-1])
	tridy.append(jmeno)

for f in os.listdir(target_slozka):
	fi = target_slozka + os.sep + f
	if not os.path.isfile(fi):
		continue
	fil = open(fi, 'r')
	
	trida = ".".join(f.split(".")[:-1])
	
	priprav_prostredi("cache", "vysledek", "gfx")
	zpracuj_tridu(tridy, trida, fil.readlines())
	presun_vysledek(trida, "gfx", "vysledek")
	fil.close()
	

