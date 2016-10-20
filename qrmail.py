#!/bin/python
"""
generate QR Code and send it via email
"""

import unirest
import config
import signapp
import urllib
import gmail
import message

class Qrmail(object):
	def __init__(self,NPM,EMAIL,KODEDOSEN):
		self.sign = signapp.Signapp()
		urlenc = self.encode16(NPM)
		url = self.createQr(urlenc,NPM)
		self.downloadQr(url)
		self.mailQr(EMAIL,KODEDOSEN)

	def encode16(self,NPM):
		return self.sign.urlEncode16(config.keyuri+NPM)

	def createQr(self,urlenc,NPM):
		param = config.apiuri+config.logouri1+NPM+config.logoext+config.url1+urlenc
		response = unirest.get(param,headers={"X-Mashape-Key": config.mashapekey})
		return response.body['url']

	def downloadQr(self,URL):
		urllib.urlretrieve(URL,"qr.jpg")

	def mailQr(self,EMAIL,KODEDOSEN):
		gm = gmail.GMail(config.email,config.password)
		isipesan = config.msg.replace("KODEDOSEN",KODEDOSEN)
		msg = message.Message(config.subject,to=EMAIL,text=isipesan,attachments=['qr.jpg'])
		gm.send(msg)

