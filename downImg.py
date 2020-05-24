import requests
from bs4 import BeautifulSoup
import lxml
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import os
import re

#HTTP User-Agent
header = {'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
page = input("输入要爬取多少篇:")

class downYoumaMan():

    def getChapter(self, url):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        #request章节页面源码
        chapter_html = requests.get(url,headers=header,verify=False)
        #章节链接
        chapter_list = BeautifulSoup(chapter_html.text, 'lxml').find('ul',class_="detail-list-select").find_all('a')
        #文章标题
        chapter_title = BeautifulSoup(chapter_html.text, 'lxml').find('span',class_="normal-top-title")
        titles = chapter_title.get_text()
        path = str(titles)
        #创建文章标题的文件夹
        Youma.mkdir(path)
        #print(titles)
        for a in chapter_list:
            href = 'https://www.youmamh.com' + a['href']
            title = a['title']
            chapter_title = str(title)
            #创建章节文件夹
            Youma.mkdir(chapter_title)
            print(os.getcwd())
            #print(href)
            #print(title)
            time.sleep(3)
            #获取章节下图片的链接
            source = requests.get(href,headers=header,verify=False)
            source_list = BeautifulSoup(source.text, 'lxml').find('div',class_='view-main-1 readForm').find_all('img')
            img_page = 1
            for li2 in source_list:
                img_url = li2['data-original']
                name = str(img_page) + '.jpg'
                #获取图片
                imgData = requests.get(img_url,headers=header,verify=False)
                #下载图片
                with open(name,'wb' ) as f:
                    time.sleep(0.5)
                    print('正在保存' + title + '第' + str(img_page) + '张图片.')
                    f.write(imgData.content)
                #print(name)
                #print(img_url)
                img_page = img_page + 1
            dir = os.path.abspath(os.path.dirname(os.getcwd()))
            os.chdir(dir)
        os.chdir('.')
    #创建文件夹函数
    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(os.path.join(".", path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join(".", path))
            os.chdir(os.path.join(".", path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

for i in range(1,int(page)+1):
    chapterUrl = "https://www.youmamh.com/book/%s" %i
    #print(chapterUrl)
    #实例化
    Youma = downYoumaMan()
    Youma.getChapter(chapterUrl)
