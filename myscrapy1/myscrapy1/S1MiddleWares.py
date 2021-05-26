"""
解决新华网使用request返回的数据不完整
注意：需要下载phantojs，并加入正确路径
"""

from selenium import webdriver
from scrapy.http import HtmlResponse
import time
import urllib.request as ur

class S1MidleWares(object):
    def process_request(self, request, spider):
        # 代理IP
        # request.meta['proxy'] = 'http://'+ur.urlopen('http://api.ip.data5u.com/dynamic/get.html?order=d5b777ff5fb3f128385b6e0b57f96f3b&sep=4').read().decode('utf-8').strip()
        if spider.name == 'XinHuaWang':
            driver = webdriver.PhantomJS(executable_path=r'..\software\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            driver.get(request.url)
            time.sleep(0.1)
            html = driver.page_source
            return HtmlResponse(url=request.url, request=request,body=html.encode(), encoding='utf-8')