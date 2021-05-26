import scrapy
from copy import deepcopy
import re
import hashlib
import time
import requests

import numpy as np
from PIL import Image
import io
import os

class S1Spider(scrapy.Spider):
    name = 'XinHuaWang'
    allowed_domains = ['xinhuanet.com']
    # start_urls = ['http://xinhuanet.com/politicspro/szgz.htm']

    # 存储的数据格式
    sql_data = dict(
        id = '',
        title = '',   # 标题
        detail_url = '',  # 详细页网址
        release_date = '',   # 发布日期
        laiyuan = '',  # 来源
         content = '',  # 内容
        redactor = '',  # 编辑
        img = '',  # 图片
        type = '',  # 文章类型
    )

    def start_requests(self):
        yield scrapy.Request(
            url = 'http://www.xinhuanet.com/politicspro/szgz.htm',
            callback=self.parse
        )

    def parse(self, response):
        # 1级页面：提取 标题、详细页url
        i = 0
        content_list_x_s = response.xpath('//div[@class="sdjj_left left"]//div[@class="tit"]')
        for content_list_x in content_list_x_s:
            # 定量爬取
            # i += 1
            # if i == 6:
            #     break
            sql_data = deepcopy(self.sql_data)
            sql_data['id'] = self.create_id()
            sql_data['title'] = content_list_x.xpath('./a/text()').extract_first()
            sql_data['detail_url'] = content_list_x.xpath('./a/@href').extract_first()
            sql_data['type'] = content_list_x.xpath('./span[@class="qian"]/text()').extract_first()

            # 去重
            f = open('urled.csv','r')
            r = f.read()
            f.close()
            if sql_data['detail_url'] in r:
                continue  # 跳过改页
            else:
                f = open('urled.csv','a+')
                f.write(sql_data['detail_url']+'\n')
                f.close()

            request = scrapy.Request(
                url=sql_data['detail_url'],
                callback=self.parse2
            )
            request.meta['sql_data'] = sql_data
            yield request


    def parse2(self,response):
        sql_data = response.meta['sql_data']

        # 爬取“日期”字段
        sql_data['release_date'] = response.xpath('//div[@class="info"]/text()').extract_first()

        # 爬取“来源”字段
        # sql_data['laiyuan'] = response.xpath('//div[@class="info"]/span/text()').extract_first()
        sql_data['laiyuan'] = re.findall('来源：\n(.*?)\n', response.xpath('//div[@class="info"]/span/text()').extract_first())[0]

        # 爬取“正文”字段，包括图片信息
        # sql_data['content'] = response.xpath('//div[@id="detail"]/p').extract()
        content = response.xpath('//div[@id="detail"]').extract_first()
        sql_data['content'] = re.sub('"','\\"', content)  # 添加转义符，才能成功入库

        # 爬取“图片”字段，键值对存储
        # 提取url前缀，用于图片的正确下载
        img = {}  # 用于存储图片名和对应图片，{[图片名：本地图片地址], ...}
        deteil_url_pre = re.findall('(.*?)c_',sql_data['detail_url'])[0]  # 图片url前缀
        img_name = re.findall('src="(.*?)"',content)  # 提前出所以图片名称，包含不需要的
        img_name = map(self.pic, img_name)  # 筛选出不需要的图片名称
        for img_n in img_name:  # 遍历所有爬取到的需要的图片名称
            if img_n:  # 根据图片名称得到该图片内容，并存入img字典
                img_url = deteil_url_pre+img_n  # 获取图片完整url，用于获取其图片内容
                _img = requests.get(img_url).content  # 获取其图片内容

                img_addree = './img/'+sql_data['id'] + '/' +img_n
                self.save_img(_img, img_addree)

                # _img = re.sub('"', '\\"', str(_img))  # 添加转义符，才能成功入库
                img[img_n] = img_addree  # 存入img字典



        sql_data['img'] = img  # 存入sql_data




        # sql_data['redactor'] = response.xpath('//span[@class="editor"]/text()').extract_first()
        sql_data['redactor'] = re.findall('责任编辑:(.*?)\n', content)[0]  # 爬取“责任编辑”字段
        yield sql_data


    # 生成随机主键id
    def create_id(self):
        m = hashlib.md5(str(time.perf_counter()).encode('utf-8'))
        return m.hexdigest()

    # 筛选出需要的图片名称
    def pic(self,x):
        if x[-3:] == 'jpg':
            return x

    # 保存图片
    def save_img(self,img,img_addree):
        response_byte = img
        byte_stream = io.BytesIO(response_byte)
        roiImg = Image.open(byte_stream)  # Image打开二进制流Byte字节流数据
        imgByteArr = io.BytesIO()  # 创建一个空的Bytes对象
        roiImg.save(imgByteArr, format='png')  # PNG就是图片格式
        imgByteArr = imgByteArr.getvalue()  # 保存的二进制流
        os.makedirs(os.path.dirname(img_addree), exist_ok=True)
        with open(img_addree, "wb") as f:
            f.write(imgByteArr)
        return None