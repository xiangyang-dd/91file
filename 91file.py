#____author:"xie"
#date:2020-08-19
# -*- coding: utf-8 -*-
import requests
import re
import time
import os
from bs4 import BeautifulSoup

def fileurl(urls,path):
    if urls and path == '':
        return print('Error！ 请输入域名！或下载路径！')
    Current = 1
    Total = 999
    HomePage = urls
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
          }
    while Current <= Total:
        print('------------------------------------当前处理页为{}!------------------------------------'.format(Current))
        url = HomePage+'forumdisplay.php?fid=19&page='+'{}'.format(Current)
        try:
            response = requests.get(url=url, headers=headers, timeout=300)
            response.close()
        except Exception as e:
            data = '超时稍后重试页url:'+url
            with open(path+'超时重试.txt', 'a') as file_handle:
                file_handle.write("{}\n".format(data))
            continue
        link = response.content.decode("utf-8")
        id = re.findall(r'span id="thread_(.*?)"', link, re.I)
        for imt in id:
            urldata = HomePage+'viewthread.php?tid={}'.format(imt)
            try:
                response = requests.get(url=urldata, headers=headers, timeout=300)
                response.close()
            except Exception as e:
                data = '超时稍后重试列表url：'+url
                with open(path + '超时重试.txt', 'a') as file_handle:
                    file_handle.write("{}\n".format(data))
                continue
            link = response.content.decode("utf-8")
            soup = BeautifulSoup(link, 'html.parser')
            div = soup.find('div', attrs={"id": "threadtitle"})
            filepath = path
            try:
                filename = str(div.find('h1').string.replace(' ', '').replace('','').translate({ord(c): "" for c in '@#$%^&*[];":,./<>?\|`~【】「」'}))
            except Exception as e:
                continue
            if not os.path.exists(filepath + str(filename)):
                picture(urldata, headers, filepath, filename, Current)
        time.sleep(0.2)
        Current += 1
def picture(urldata,headers,filepath,filename,Current):
    try:
        response = requests.get(url=urldata, headers=headers, timeout=300)
        response.close()
    except Exception as e:
        print('超时重试详情url：'+urldata+Current+filename)
    link = response.content.decode("utf-8")
    if 'jpg' or 'jpeg' or 'gif' in link:
        id = re.findall(r'file="(.*?)"', link, re.I)
        pic = len(id)
        print('===={}==== 共有{}张图片下载---------------当前处理第{}页-------------'.format(filename, pic, Current))
        i = 1
        for url in id:
            ext = url.split('.')[-1]
            if pic == 0:
                continue
            if not os.path.exists(filepath + str(filename)):
                os.mkdir(filepath + str(filename))
            print('正在下载第{}张图片'.format(i))
            try:
                r = requests.get(url=url, headers=headers, timeout=700)
                r.close()
            except Exception as e:
                data = '超时稍后重试详图片url：'+Current+filename+url
                with open(path + '超时重试.txt', 'a') as file_handle:
                    file_handle.write("{}\n".format(data))
                continue
            time.sleep(1)
            name = '{}.{}'.format(i, ext)
            with open(filepath+filename+'\\'+'{}'.format(name), 'wb') as f:
                f.write(r.content)
            i += 1
        print('提示！！！  {}  下载结束! 准备下载下一个！！！'.format(filename))

if __name__ == '__main__':
    path = ''   #设置下载路径如'G:\\2\\91图片\\'
    HomePage = ''  #输入91的域名如https://www.baidu.com/
    fileurl(HomePage, path)
