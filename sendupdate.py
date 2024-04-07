import json
import hashlib
import os
import sys
import zipfile
import urllib.request
import requests
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
	message = eee.split("##")[1].replace(eee.split("##")[1].split("\r")[0] + "\r\n", "")
	data = {
		"content": "@everyone",
		"embeds": [
			{
				"description": "# New Update!\n### - Version: v" + modVer['version'],
				"color": 16307200,
				"fields": [
					{
						"name": "Changelog",
						"value": message
					}
				],
				"author": {
					"name": "User Reviews"
				},
				"footer": {
					"text": "Download in Geometry Dash right now!"
				},
				"thumbnail": {
					"url": "https://raw.githubusercontent.com/Uproxide/user-reviews/main/logo.png"
				}
			}
		],
		"attachments": []
	}
	request.urlopen(req, data=json.dumps(data).encode('utf-8'))



for mod in json.loads(os.getenv('THE_OBJECT')):
	send_webhook(mod['changelog'],mod)
	

def send_webhook3(eee,modVer):
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
	message = eee.split("##")[1].replace(eee.split("##")[1].split("\r")[0] + "\r\n", "")
	data = {
		"content": "@everyone",
		"embeds": [
			{
				"description": "# New Update!\n### - Version: v" + modVer['version'],
				"color": 16307200,
				"fields": [
					{
						"name": "Changelog",
						"value": message
					}
				],
				"author": {
					"name": modVer["modJSON"]["name"]
				},
				"footer": {
					"text": "Download in Geometry Dash right now!"
				}
			}
		],
		"attachments": []
	}
	request.urlopen(req, data=json.dumps(data).encode('utf-8'))



for mod in json.loads(os.getenv('THE_OBJECT3')):
	send_webhook3(mod['changelog'],mod)

def send_webhook4(eee,modVer):
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
	message = eee.split("##")[1].replace(eee.split("##")[1].split("\r")[0] + "\r\n", "")
	data = {
		"content": null,
		"embeds": [
			{
			"description": "# New Update!\n### - Version: v" + modVer['version'],
			"color": 16644552,
			"fields": [
				{
					"name": "Changelog",
					"value": message
				}
			],
			"author": {
				"name": "Level Thumbnails"
			},
			"footer": {
				"text": "Download in Geometry Dash right now!"
			},
			"thumbnail": {
				"url": "https://github.com/cdc-sys/level-thumbs-mod/blob/main/logo.png?raw=true"
			}
			}
		],
		"attachments": []
	}
	request.urlopen(req, data=json.dumps(data).encode('utf-8'))



for mod in json.loads(os.getenv('THE_OBJECT4')):
	send_webhook4(mod['changelog'],mod)

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
	title = (eee.split("##")[1].split("\r")[0]).replace((eee.split("##")[1]).split("\r")[0], modVer['modJSON']['name'] + " v" + modVer['version'])
	message = eee.split("##")[1].replace(eee.split("##")[1].split("\r")[0] + "\r\n", "")
	data = {
		'content': ("# :" + modVer["tags"] + ": " + modVer["tags2"] + "\n# " + eee.split("##")[1]).replace((eee.split("##")[1]).split("\r")[0], modVer['modJSON']['name'] + " v" + modVer['version'] + " is out on Geode!") + shouldslashn + "[View Mod](<https://geode-sdk.org/mods/" + modVer['bundleId'] + ">)\nDownload or Update in Geometry Dash right now!\n||<@&" + os.getenv('ROLE_ID2') + ">||\n",
	}
	request.urlopen(req, data=json.dumps(data).encode('utf-8'))

	requests.post("https://ntfy.sh/",
    		data=json.dumps({
			"topic": os.getenv('NTFY_GROUP'),
			"message": message,
			"title": modVer["tags2"] + " | " + title,
			"tags": [modVer["tags"],modVer["tags3"]],
			"markdown": True,
			"icon": "https://raw.githubusercontent.com/geode-sdk/mods/main/mods-v2/" + modVer["bundleId"] + "/logo.png",
			"click": "https://geode-sdk.org/mods/" + modVer['bundleId']
		})
	)	



for mod in json.loads(os.getenv('THE_OBJECT2')):
	send_webhook2(mod['changelog'],mod)
