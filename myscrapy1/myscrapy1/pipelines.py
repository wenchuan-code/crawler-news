# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import hashlib
import time
import re

class Myscrapy1Pipeline:
    def __init__(self):
        self.mysql_conn = pymysql.Connection(
            host='localhost',
            port=3306,
            user='root',
            password='12345678',
            database='test',
            charset='utf8',
        )
    def process_item(self, item, spider):
        # 创建光标对象
        cs = self.mysql_conn.cursor()
        # 入库item_XinHuaWang
        item_XinHuaWang = self.item_XinHuaWang(item,model='XinHuaWang')
        sql_column = ','.join([key for key in item_XinHuaWang.keys()])
        sql_value = ','.join(['"%s"' % item_XinHuaWang[key] for key in item_XinHuaWang.keys()])
        sql_str = 'insert into XinHuaWang (%s) value (%s);' % (sql_column, sql_value)
        cs.execute(sql_str)
        self.mysql_conn.commit()
        # 入库item_XinHuaWang_img
        """MySQL直接存储图片内容没调通， 用本地路径代替"""
        for i in item['img']:
            item_XinHuaWang_img = self.item_XinHuaWang(item,model='XinHuaWang_img',img_name=i,img_content=item['img'][i])

            # 调试直接存储图片内容
            # with open(item_XinHuaWang_img['img_content'], "rb") as f:  # 读取本地图片
            #     item_XinHuaWang_img['img_content'] = pymysql.Binary(f.read())
            #
            #     # item_XinHuaWang_img['img_content'] = re.sub('"', '\\"', item_XinHuaWang_img['img_content'])
            #
            #
            #     # sql_str = 'insert into XinHuaWang_img (img_content) value (%s)'%item_XinHuaWang_img['img_content'][:10]
            #     # sql_str = 'insert into XinHuaWang_img (id_,img_name) value ({0},{1});'.format(str(item_XinHuaWang_img["id_"]),str(item_XinHuaWang_img["img_name"]))
            #     cs.execute(sql_str)
            #     self.mysql_conn.commit()
            sql_column = ','.join([key for key in item_XinHuaWang_img.keys()])
            sql_value = ','.join(['"%s"' % item_XinHuaWang_img[key] for key in item_XinHuaWang_img.keys()])
            sql_str = 'insert into XinHuaWang_img (%s) value (%s);' % (sql_column, sql_value)
            cs.execute(sql_str)
            self.mysql_conn.commit()

        # sql_column = ','.join([key for key in item.keys()])
        # sql_value = ','.join(['"%s"' % item[key] for key in item.keys()])
        # sql_str = 'insert into XinHuaWang (%s) value (%s);' % (sql_column, sql_value)
        # print(sql_str)

        # cs.execute(sql_str)
        # self.mysql_conn.commit()
        return item

    def item_XinHuaWang(self,item,model,img_name=None,img_content=None):
        """存放新华网主体"""
        if model == 'XinHuaWang':
            XinHuaWang = {}
            XinHuaWang['id'] = item['id']
            XinHuaWang['title'] = item['title']
            XinHuaWang['detail_url'] = item['detail_url']
            XinHuaWang['release_date'] = item['release_date']
            XinHuaWang['laiyuan'] = item['laiyuan']
            XinHuaWang['content'] = item['content']
            XinHuaWang['redactor'] = item['redactor']
            XinHuaWang['type'] = item['type']
            return XinHuaWang
        elif model == 'XinHuaWang_img':
            """存放新华网图片"""
            XinHuaWang_img = {}
            XinHuaWang_img['id_'] = item['id']
            XinHuaWang_img['img_name'] = img_name
            XinHuaWang_img['img_content'] = img_content
            return XinHuaWang_img
        else:
            raise print("item_XinHuaWang中model选择错误！！")

