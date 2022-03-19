import math
import os
import random
import re
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

##获取第几页的HTML内容
def getContent(pageNum):

    print("马上开始爬第%d页数据"%pageNum)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
        'Connection': 'keep-alive'
    }

    #https://pic.netbian.com/4kmeinv/index_6.html
    url = "https://pic.netbian.com/4kmeinv/index_%d.html"%pageNum
    if(pageNum == 1):
        url = "https://pic.netbian.com/4kmeinv/index.html"


    ##请求对象(URL + 请求头)
    req = urllib.request.Request(url, headers=headers)

    page = urllib.request.urlopen(req).read()
    page = page.decode("GBK")
    print("完成第%d页数据爬虫" %pageNum)
    return page

##从内容页面中 获取 图片的URL地址
def getPhotoUrl(content):
    pattern = re.compile(r'<img src="(.+?)" alt=".*?" />')
    res = re.findall(pattern, content)
   # res = "https://pic.netbian.com/4kmeinv/"+res
    list = []
    for url in res:
        newUrl = "https://pic.netbian.com" + url
        list.append(newUrl)
    return list

def downLoadAllPhoto(list,page):
    ##创建目录
    path = "E:\李泽成\素材\人像2"
    if os.path.isdir(path) == False:
        os.mkdir(path)

    for (index,url) in enumerate(list):
        filePath = "%s/%d_%d"%(path,page,index)
        print("正在下载第%d:%s图片"%(index,url))
        downloadFile(url,filePath)


##下周一张图片
def downloadFile(url,path):
    ##后缀名
    ext = url.split(".")[-1]
    path = path + "." + ext  ##aaa.png

    #设置请求头
    opener = urllib.request.build_opener()
    opener.addheaders=[("User-Agent", "Mozilla/5.0")]
    urllib.request.install_opener(opener)
    ##下载
    urllib.request.urlretrieve(url, path)



if __name__ == '__main__':
   for i in range(1,140):
       page = getContent(i)
       photoList = getPhotoUrl(page)
       downLoadAllPhoto(photoList,i)