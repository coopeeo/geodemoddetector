import json
import hashlib
import os
import sys
import zipfile
import urllib.request
import re

#print(os.getenv('THE_OBJECT'))
#release_url = os.getenv('LE_RELEASE')
#urllib.request.urlretrieve((release_url + "/" + os.getenv('THE_MOD_ID') + ".geode").replace("/tag/","/download/"), 'le.geode')
#archive = zipfile.ZipFile('le.geode', 'r')
#e = archive.open('changelog.md')
#file_list = archive.namelist()	



def send_webhook(eee,modVer):
	from urllib import request
	import json
	import os
	eeee = []
	for eeeee in eee:
		# print(eeeee.decode('utf-8'))
		eeee.append(eeeee.decode('utf-8'))
	# print(eeee)
	eeeeee = "".join(eeee)
	# print(eeeeee)
	print(eeeeee.split("##")[1])
	print((eeeeee.split("##")[1]).split("\r")[0])
	req = request.Request(os.getenv('DISCORD_WEBHOOK_URL'), method='POST')
	req.add_header('User-Agent', 'python urllib')
	req.add_header('Content-Type', 'application/json')
	data = {
		'content': ("# " + eeeeee.split("##")[1]).replace((eeeeee.split("##")[1]).split("\r")[0], modVer['modJSON']['name'] + " v" + modVer['version'] + " is out on Geode!") + "\n||<@&" + os.getenv('ROLE_ID') + ">||\n",
	}
	request.urlopen(req, data=json.dumps(data).encode('utf-8'))



for mod in json.loads(os.getenv('THE_OBJECT')):
	print(mod)
	send_webhook(mod['changelog'],mod)