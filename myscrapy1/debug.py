"""DeBug调试"""
# from scrapy.cmdline import execute
# import os
# import sys
# if __name__ == '__main__':
#
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     execute(['scrapy','crawl','XinHuaWang'])


"""定时爬虫，可多进程同时爬取多个网站"""
from multiprocessing import Process
from scrapy import cmdline
import time,logging

# 配置参数即可, 爬虫名称，运行频率
confs = [
 {
 "spider_name": "XinHuaWang",
 "frequency": 60,  # 秒
 },
]

def start_spider(spider_name, frequency):
    args = ["scrapy", "crawl", spider_name]
    while True:
        start = time.time()
        p = Process(target=cmdline.execute, args=(args,))
        p.start()
        p.join()
        logging.debug("### use time: %s" % (time.time() - start))
        time.sleep(frequency)

if __name__ == '__main__':
    while True:
        for conf in confs:
            process = Process(target=start_spider,args=(conf["spider_name"], conf["frequency"]))
            process.start()
            time.sleep(86400)

