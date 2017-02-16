#coding=utf-8
import urllib2
from BeautifulSoup import *
import os
import time

starttime = time.time()

def url_open(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',"HeJingjing's Browser") 
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html)
    return soup

def text(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',"HeJingjing's Browser") 
    html = urllib2.urlopen(req).read()
    return html


def get_pic(url):
    soup = url_open(url)
    tags = soup.img
    pic_address = tags.get('src', 1)
    picture = text(pic_address)
    print '正在下载'+ str(pic_address)
    return picture

#坑，以后爬虫都要加这段，不然被403坑死了

keyword = raw_input('请输入搜索关键词：')
pages = raw_input('请输入爬取页面：')



os.mkdir(keyword)

n = 0
for page in range(0,int(pages)):
    url='https://e-hentai.org/lofi/?page='+str(page)+'&f_search='+str(keyword)+'&f_sname=1&f_stags=1&f_apply=Apply+Filter'
    addresslist = []
    try:
        soup = url_open(url)
        tags = soup('a')
        for tag in tags:
            address = tag.get('href', None)
            if 'e-hentai.org/lofi/g' in str(address):  #过滤出搜索页面结果中的所有内容的链接 
                if address in addresslist:
                    continue
                else:
                    addresslist.append(address)
                    pagenum = 0
                    while True:
                        pic_page = text(address+str(pagenum))
                    
                        pagenum = pagenum+1
                        pic_pg = BeautifulSoup(pic_page) 
                        temps = pic_pg('a')
                        for temp in temps:
                            pic_address = temp.get('href', None)
                            if 'e-hentai.org/lofi/s' in pic_address:
                                picture = get_pic(pic_address)
                                filename = str(pic_address.split('/')[-1]) #下载到指定路径
                                pic = open(keyword+'/'+filename+'.jpg','wb')
                                pic.write(picture)
                                n = n+1
                                pic.close()
                                    
                            else:
                                continue

                        if "Next Page" not in pic_page: #避免页面溢出
                            break
                
    except:
        continue
#print addresslist   #调试语句，使用时请注释掉


endtime = time.time()

print '用时总计' + str((endtime - starttime)) + '秒' 
print '总计下载' + str(n) + '张图片'

