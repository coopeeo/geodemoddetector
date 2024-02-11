import json
import hashlib
import os
import sys
import zipfile
import urllib.request
import re

	



def send_webhook(eee,modVer):
	from urllib import request
	import json
	import os
	
	req = request.Request(os.getenv('DISCORD_WEBHOOK_URL'), method='POST')
	req.add_header('User-Agent', 'python urllib')
	req.add_header('Content-Type', 'application/json')
	if eee == "No changelog provided":
		eee = "## Le version gets replaced\r\n `no changelog (changelog.md file) found`"
	if ("# " + modVer['modJSON']['name']) not in eee.split('##')[0] and ("# Changelog") not in eee.split('##')[0]:
		eee= modVer['modJSON']['name'] + eee.replace("# ","## ")
	data = {
		'content': ("# " + eee.split("##")[1]).replace((eee.split("##")[1]).split("\r")[0], modVer['modJSON']['name'] + " v" + modVer['version'] + " is out on Geode!") + "\nDownload or Update in Geometry Dash right now!\n[View Mod](https://geode-sdk.org/mods/" + modVer['bundleId'] + ")\n||<@&" + os.getenv('ROLE_ID') + ">||\n",
	}
	request.urlopen(req, data=json.dumps(data).encode('utf-8'))



for mod in json.loads(os.getenv('THE_OBJECT')):
	print(mod)
	send_webhook(mod['changelog'],mod)