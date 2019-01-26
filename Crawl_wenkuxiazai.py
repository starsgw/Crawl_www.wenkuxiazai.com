# 爬取网站：https://www.wenkuxiazai.com/

import requests
from Ip_and_Agent.ip_and_agent2 import User_Agent,Inland_ip#在这里放入高匿ip，User_Agent
from lxml import etree
from pymongo import MongoClient
from multiprocessing import Pool
import time
import urllib.parse
import random
import os
import hashlib
import re

con=MongoClient("192.168.8.211",27017)
db=con.Runoob
download_set=db.wenkuxiazaiwang_data#下载这里
# keyword_set=db.Runoob#从这里取出url（测试关键字）
keyword_set=db.key_cn#从这里取出url
coll_ip=db.coll_ip
db_dtip=con.proxy#连接动态ip的mongo库
dtip_set=db_dtip.proxies_ip_dongtai


# class haixuewang_spider(object):
#     def __init__(self,keyword,page):
#         self.prox={"http":Inland_ip}
#         self.headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "zh-CN,zh;q=0.9",
#         "Connection": "keep-alive",
#         # "Cookie": "ASP.NET_SessionId=swciagkmit0wgon1optvezol; UM_distinctid=167e377fe96227-02ebec8327d1c7-671b1b7c-1fa400-167e377fe97ff; Hm_lvt_1cb6d926d0e483d882157f92a7640d52=1545709552,1545709555,1545709557,1545709570; Hm_lpvt_1cb6d926d0e483d882157f92a7640d52=1545716426; CNZZDATA1253566994=1799924477-1545709207-%7C1545714908",
#         "Host": "www.wenkuxiazai.com",
#         "Referer": "https://www.wenkuxiazai.com/search/"+keyword+str(page)+".html",
#         # "Upgrade-Insecure-Requests": "1",
#         "User-Agent":User_Agent}

def get_req(keyword,page):
    headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    # "Cookie": "ASP.NET_SessionId=swciagkmit0wgon1optvezol; UM_distinctid=167e377fe96227-02ebec8327d1c7-671b1b7c-1fa400-167e377fe97ff; Hm_lvt_1cb6d926d0e483d882157f92a7640d52=1545709552,1545709555,1545709557,1545709570; Hm_lpvt_1cb6d926d0e483d882157f92a7640d52=1545716426; CNZZDATA1253566994=1799924477-1545709207-%7C1545714908",
    "Host": "www.wenkuxiazai.com",
    "Referer": "https://www.wenkuxiazai.com/",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent":random.choice(User_Agent)}
    # parm={"q":urllib.parse.quote(keyword,encoding="gb2312"),
    #       "s":"search"}

    ip=random.choice(get_ip())
    proxies={"http":ip,"https":ip}
    print(proxies)
    req=requests.get("https://www.wenkuxiazai.com/search/"+urllib.parse.quote(keyword,encoding="gb2312")+"-"+str(page)+".html",proxies=proxies,headers=headers,timeout=100)
    # time.sleep(random.choice(range(5,8)))
    # print("https://www.wenkuxiazai.com/search/"+urllib.parse.quote(keyword,encoding="gb2312")+"-"+str(page)+".html&s=search")
    # req_test = requests.get("http://icanhazip.com", headers=headers, proxies=proxies, timeout=360)
    # print("进程id:",os.getpid(),"访问ip:", req_test.text)
    # print(req.text)
    return req.text

def get_data(keyword,page):
    data=get_req(keyword,page)
    print("get_data",)
    html=etree.HTML(data)
    url_list=html.xpath("//div[@class='lista']/div/p/a/@href")
    title_list=html.xpath("//div[@class='lista']/div/p/a/@title")
    summary_list=html.xpath("//div[@class='lista']/div/p[2]")
    if url_list==[]:
        return "over"

    index=0
    test_list=[]
    for url in url_list:
        try:
            MD5_url = hashlib.md5()
            MD5_url.update(url.encode())
            download_set.insert_one({"title":title_list[index],"summary":summary_list[index].xpath('string(.)').strip(),"url":"https://www.wenkuxiazai.com/word"+url[4:-5]+"-1.doc","MD5_url":MD5_url.hexdigest(),"status":0,"status_test":0})
            print("插入成功")
            test_list.append(1)
            index+=1
        except:
            index+=1
            test_list.append(0)
            print("重复数据")

    if sum(test_list)<5:
        return "over"

def get_ip():
    dtip_list=dtip_set.find({})
    ip_list=[]
    for ip in dtip_list:
        # print(ip.get("ip"))
        ip_list.append(ip.get("ip"))
    return ip_list

def get_keyword():
    # proxies = get_ip()
    # print(":",proxies)
    # if proxies == 2:
    #     print("所有代理都被使用")
    #     return

    while True:
        data=keyword_set.find_one_and_update({"status": 1}, {"$set": {"status": 2}})
        print(data["_id"])
        # time.sleep(3)
        if not data:
            return
        for page in range(0,5000,10):
            print(page)
            if page==0:
                page=""
            key = get_data(data["_id"],page)

            # key=get_data("撒地方", page) #测试
            if key == "over":
                # time.sleep(180)
                break


def pro():
    pool = Pool(10)
    for i in range(1000000):
        # if i >9:
        #     i=i-10
        pool.apply_async(get_keyword)
    pool.close()
    pool.join()


if __name__=="__main__":
    # get_req("python","10")
    # get_data("java","-10")
    pro()
    # get_keyword()
    # get_ip()

