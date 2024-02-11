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
		eee = "## Le version gets replaced\r\n* `no changelog (changelog.md file) found`\n"
	if ("# " + modVer['modJSON']['name']) not in eee.split('##')[0] and ("# Changelog") not in eee.split('##')[0]:
		eee= modVer['modJSON']['name'] + eee.replace("# ","## ")
	shouldslashn = "\n\n"
	if "\n" in eee.split("##")[1].split("*")[len(eee.split("##")[1].split("*")) - 1]:
		shouldslashn = "\n"
	data = {
		'content': ("# " + eee.split("##")[1]).replace((eee.split("##")[1]).split("\r")[0], modVer['modJSON']['name'] + " v" + modVer['version'] + " is out on Geode!") + shouldslashn + "[View Mod](<https://geode-sdk.org/mods/" + modVer['bundleId'] + ">)\nDownload or Update in Geometry Dash right now!\n||<@&" + os.getenv('ROLE_ID') + ">||\n",
	}
	request.urlopen(req, data=json.dumps(data).encode('utf-8'))



for mod in json.loads(os.getenv('THE_OBJECT')):
	send_webhook(mod['changelog'],mod)

def send_webhook2(eee,modVer):
	from urllib import request
	import json
	import os
	
	req = request.Request(os.getenv('DISCORD_WEBHOOK_URL2'), method='POST')
	req.add_header('User-Agent', 'python urllib')
	req.add_header('Content-Type', 'application/json')
	if eee == "No changelog provided":
		eee = "## Le version gets replaced\r\n* `no changelog (changelog.md file) found`\n"
	if ("# " + modVer['modJSON']['name']) not in eee.split('##')[0] and ("# Changelog") not in eee.split('##')[0]:
		eee= modVer['modJSON']['name'] + eee.replace("# ","## ")
	shouldslashn = "\n\n"
	if "\n" in eee.split("##")[1].split("*")[len(eee.split("##")[1].split("*")) - 1]:
		shouldslashn = "\n"
	data = {
		'content': ("# Mod Updates\n# " + eee.split("##")[1]).replace((eee.split("##")[1]).split("\r")[0], modVer['modJSON']['name'] + " v" + modVer['version'] + " is out on Geode!") + shouldslashn + "[View Mod](<https://geode-sdk.org/mods/" + modVer['bundleId'] + ">)\nDownload or Update in Geometry Dash right now!\n||<@&" + os.getenv('ROLE_ID2') + ">||\n",
	}
	request.urlopen(req, data=json.dumps(data).encode('utf-8'))



for mod in json.loads(os.getenv('THE_OBJECT2')):
	send_webhook2(mod['changelog'],mod)