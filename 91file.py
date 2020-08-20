#____author:"xie"
#date:2020-08-19
# -*- coding: utf-8 -*-
import requests
import re
import time
import os
from bs4 import BeautifulSoup
def fileurl(urls):
    if urls =='':
        return print('请输入域名！')
    Current=1
    Total=991
    HomePage =urls
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
          }
    while Current <= Total:
        url =HomePage+'forumdisplay.php?fid=19&page='+'{}'.format(Current)
        response = requests.get(url=url, headers=headers)
        link = response.content.decode("utf-8")
        id = re.findall(r'span id="thread_(.*?)"', link, re.I)
        for imt in id:
            urldata=HomePage+'viewthread.php?tid={}'.format(imt)
            response = requests.get(url=urldata, headers=headers)
            link = response.content.decode("utf-8")
            soup = BeautifulSoup(link, 'html.parser')
            div = soup.find('div', attrs={"id": "threadtitle"})
            filename = str(div.find('h1').string.replace(' ', '').replace('【', '').replace('】', '').replace('~', '').replace('/',''))
            if not os.path.exists('D:\\2\\91图片\\' + str(filename)):
                picture(urldata,headers)
        time.sleep(0.2)
        Current+=1
def picture(urldata,headers):
    response = requests.get(url=urldata, headers=headers)
    link = response.content.decode("utf-8")
    soup=BeautifulSoup(link,'html.parser')
    div=soup.find('div', attrs={"id": "threadtitle"})
    filename=str(div.find('h1').string.replace(' ','').replace('【','').replace('】','').replace('~','').replace('/',''))
    if 'jpg'or'jpeg'or'gif' in link:
        id = re.findall(r'file="(.*?)"', link, re.I)
        pic=len(id)
        print('{} 共有{}张图片下载'.format(filename, pic))
        i=1
        for url in id:
            ext = url.split('.')[-1]
            if pic == 0:
                continue
            if not os.path.exists('D:\\2\\91图片\\' + str(filename)):
                os.mkdir('D:\\2\\91图片\\' + str(filename))
            print('正在下载第{}张图片'.format(i))
            try:
                r = requests.get(url=url, headers=headers)
            except ZeroDivisionError:
                continue
            time.sleep(1)
            name='{}.{}'.format(i,ext)
            with open('D:\\2\\91图片\\'+filename+'\\'+'{}'.format(name), 'wb') as f:
                f.write(r.content)
            i+=1
        print('提示！！！  {}  下载结束! 准备下载下一个！！！'.format(filename))
if __name__ == '__main__':
    HomePage =''   #输入url以/结束
    fileurl(HomePage)
