import os
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'
}
def title_href():
    url = 'http://pic.netbian.com/'
    response = requests.get(url).content.decode('gbk')
    # print(response)
    html = etree.HTML(response)
    divs = html.xpath('//*[@id="main"]/div[2]/a')
    for div in divs:
        title = div.xpath('./@title')[0]
        href = 'http://pic.netbian.com/' + div.xpath('./@href')[0]
        # print(title, href)
        name_link(title, href)  # 传参

def name_link(title, href):
    for i in range(1, 5):  # 需要全站图片， 扩大循环范围即可
        if i == 1:
            url = href
        else:
            url = href + 'index_{}.html'.format(i)
        # print(title, url)
        response = requests.get(url, headers=headers).content.decode('gbk')
        # print(response)
        html = etree.HTML(response)
        lis = html.xpath('//*[@id="main"]/div[3]/ul/li')
        for li in lis:
            img_name = li.xpath('./a/img/@alt')[0]
            img_href = 'http://pic.netbian.com' + li.xpath('./a/@href')[0]
            # print(img_name, img_href)
            img_name_url(title, img_name, img_href)  # 传参

def img_name_url(title, name, url):
    response = requests.get(url, headers=headers).content.decode('gbk')
    # print(response)
    html = etree.HTML(response)
    image_url = 'http://pic.netbian.com/' + html.xpath('//*[@id="img"]/img/@src')[0]
    # print(name, image_url)
    download(title, name, image_url)  # 传参

count = 1
def download(title, img_name, img_url):
    global count
    path = '彼岸图库/{}'.format(title)
    if not os.path.exists(path):
        os.makedirs(path)
        print('-------[{}]文件夹已经创建成功，开始下载图片-------'.format(title))
    print('正在下载{}， 这是第{}张图片'.format(img_name, count))
    response = requests.get(img_url, headers=headers)
    with open('彼岸图库/{}/{}.jpg'.format(title, img_name), 'wb')as f:
        count += 1
        f.write(response.content)
        print('{}已经成功下载， 这是第{}张图片'.format(img_name, count))
title_href()

