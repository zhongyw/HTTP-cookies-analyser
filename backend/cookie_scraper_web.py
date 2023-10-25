import io
import os
from flask import make_response, send_file
import prettytable as pt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import datetime as dt
from dashscope_text import call_with_messages_short

def timestamp_to_timestr(timestamp):
    # return dt.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S.%f")
    return dt.datetime.fromtimestamp(timestamp)

pathOutput = "output.txt"
pathExcel = "cookie-db-custom.xlsx"
PATH_TO_URLS = "URLS-custom.txt"

DRIVER_PATH = "chromedriver_win32/chromedriver-new.exe"
s = Service(DRIVER_PATH)
options = webdriver.ChromeOptions()
# options.binary_location = r"C:/Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

options.binary_location = r"C:\Users\zw198\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe"
# options.add_argument(
#     "--user-data-dir=C:\\Users\\dhyey\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default")
# options.add_argument("--profile-directory=Default")
options.add_argument("--log-level=3")
options.headless = True
driver = webdriver.Chrome(options=options, service=s)
import re

def split_urls(url_string):
    # 使用正则表达式匹配逗号或分号作为分隔符
    delimiter_pattern = r'[;,，]'
    url_list = re.split(delimiter_pattern, url_string)
    
    # 移除每个URL周围可能存在的空格
    url_list = [url.strip() for url in url_list]
    
    return url_list

def getAllurls(path):
    with open(path, 'r') as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls]
    return urls


def getAllParams(driver, urls):
    cookies = []
    for url in urls:
        print('Getting cookies for: ' + url)
        try:
            driver.get(url=url)
            cookies.append(driver.get_cookies())
            driver.implicitly_wait(3)
        except Exception as e:
            print(e)
    # print(cookies)
    paramList = []
    c = 0
    for cookie in cookies:
        params = {'url': urls[c], 'name': [], 'value': [], 'domain': [],
                  'expires': [], 'httpOnly': [], 'secure': [], 'sameSite': [], 'explain': []}
        for i in cookie:
            params['name'].append(i['name'])
            params['value'].append(i['value'])
            params['domain'].append(i['domain'])
            expires = ''
            if 'expiry' in i:
                expires = timestamp_to_timestr(i['expiry'])
            
            # params['path'].append(i['path'])
            params['expires'].append(expires)
            params['httpOnly'].append(i['httpOnly'])
            params['secure'].append(i['secure'])
            params['sameSite'].append(
                i['sameSite']) if 'sameSite' in i else params['sameSite'].append('')
            # params['explain'].append(call_with_messages_short(f"请猜测一下下面的cookie中{i['name']}的含义，回答要简洁，在20个字以内: {i['domain']} {i['name']} {i['value']} {expires}"))
            params['explain'].append("")
        paramList.append(params)
        c += 1

    return paramList


def printCookieTable(paramList, urls):
    if os.path.exists(pathOutput):
        os.remove(pathOutput)
    for i in range(len(paramList)):
        params = paramList[i]
        table = pt.PrettyTable()
        table.title = 'Cookies for: ' + urls[i]
        table.field_names = ['名称', '值', '域名',
                             'Path', 'Expires', 'HttpOnly', 'Secure', 'SameSite', '含义']
        table.align = 'l'
        table.max_width = 40
        for i in range(len(params['name'])):
            table.add_row([params['name'][i], params['value'][i], params['domain'][i], params['path'][i],
                          params['expires'][i], params['httpOnly'][i], params['secure'][i], params['sameSite'][i], params['explain'][i]])

        with open(pathOutput, 'a') as f:
            f.write(table.get_string())
            f.write('\n\n')
        print(table)
        print()


def SaveToExcel(paramList, urls):
    if os.path.exists(pathExcel):
        os.remove(pathExcel)
    df_main = pd.DataFrame()
    for i in range(len(paramList)):
        params = paramList[i]
        df = pd.DataFrame(params)
        df_main = pd.concat([df_main, df], ignore_index=True)
    df_main.to_excel(pathExcel, index=False)


def scrape(urlsStr):
    # urls = getAllurls(PATH_TO_URLS)
    urls = split_urls(urlsStr)
    paramList = getAllParams(driver, urls)
    # printCookieTable(params, urls)
    # SaveToExcel(params, urls)
    out = io.BytesIO()
    df_main = pd.DataFrame()
    for i in range(len(paramList)):
        params = paramList[i]
        df = pd.DataFrame(params)
        df_main = pd.concat([df_main, df], ignore_index=True)
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    df_main.to_excel(excel_writer=writer, sheet_name='Sheet1', index=False)
    writer.close()

    out.seek(0)

    file_name = 'xxx.xlsx'
    response = make_response(out.getvalue())
    # response = send_file(out, as_attachment=True, download_name=file_name)
# 设置响应的内容类型
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    # 设置文件名并进行UTF-8编码
    file_name = 'xxx.xlsx'
    encoded_filename = file_name.encode('utf-8')
    response.headers['Content-Disposition'] = 'attachment; filename="{}"; filename*=UTF-8''{}'.format(encoded_filename, encoded_filename)
    return response

if __name__ == '__main__':
    urls = getAllurls(PATH_TO_URLS)
    params = getAllParams(driver, urls)
    # printCookieTable(params, urls)
    SaveToExcel(params, urls)
