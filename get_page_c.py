import base64
import urllib2
import os.path

def download_page(_uri, _user, _password):
	password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_manager.add_password(None, "https://is.muni.cz", _user, _password)
	
	auth_handler =  urllib2.HTTPBasicAuthHandler(password_manager)
	opener = urllib2.build_opener(auth_handler)
	#urllib2.install_opener(opener)
	
	file = opener.open(_uri)
	filedata = file.read()
	urlopened = file.geturl()
	
	return save_to_cache(_uri, filedata, urlopened)
	
def get_page(_uri, _user, _password):
	if is_cached(_uri):
		return get_from_cache(_uri)
	else:
		return download_page(_uri, _user, _password)
		
def is_cached(_url):
	try:
		file = open("./cache/" + base64.b64encode(_url, "+-"))
		file.close()
		return True
	except:
		return False

def get_from_cache(_uri):
	#try:
	file = open("./cache/" + base64.b64encode(_uri, "+-"), 'rb')
	urlopened = file.readline()
	filedata = "".join(file.readlines())
	file.close()
	return (filedata, urlopened)
	#except:
	return (None, None)

def save_to_cache(_url, _filedata, _uriopened):
	#try:
	file = open("./cache/" + base64.b64encode(_url, "+-"), 'wb')
	file.write(_uriopened + "\n")
	file.write(_filedata)
	file.close()
	return (_filedata, _uriopened)
	#except:
	return (None, None)

	
def dump_url(_url, _user, _password):
	data, uri = get_page(_url, _user, _password)
	filename = './gfx/' + base64.b64encode(_url, "+-")
	dump = open(filename, 'wb')
	dump.write(data)
	dump.close()
	return filename
