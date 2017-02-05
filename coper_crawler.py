#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re
import pymongo
import matplotlib.pyplot as plt
import operator
import ip_acquire
import info_init
import json
import os
import urllib
import time
import requests
from bs4 import BeautifulSoup

weburl = "http://copper.ccmn.cn/historyprice/cjxh_1/"

webheaders= {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}


def floatrange(start,stop,steps):
    return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]

class Application():
    def __init__(self,root=None,Label_info=None,use_net=True):
        self.date_detal = []
        # self.__app_init()
        ip_get = ip_acquire.Applaction()
        info_app = info_init.Applaction()
        info_data = info_app.load(r"E:\\")
        user = info_data["mongo_user"]
        pwd = info_data["mongo_pw"]
        self.update_font(1,root,Label_info)
        ip = ip_get.ip_get()
        uri = 'mongodb://' + user + ":" + pwd + "@" + ip + ":" + "27017"
        client = pymongo.MongoClient(uri)
        self.update_font(2, root, Label_info)
        metal = client['金属价格']
        coper = metal['coper']
        self.urls = coper['url']
        self.real_urls = coper['real_url_2016_3']
        self.price_info = coper['price_info']
        self.lost_index = coper['lost_index']
        self.last_data = coper['last_date']
        self.update_font(3, root, Label_info)
        if use_net is False:
            path = os.getcwd()
            path_data_detal = path + "\\"+"Config"+'\\' + "coper_back_up.jason"
            path_date_last = path + "\\" +"Config"+'\\'"last_time.jason"
            if os.path.isfile(path_data_detal) is True and use_net is False:
                print("读取数据文件")
                self.update_font(4, root, Label_info)
                with open(path_data_detal, "r") as json_file:
                    self.date_detal = json.load(json_file)
            else:
                print("无法读取")
                use_net = True
            if os.path.isfile(path_date_last) is True and use_net is False:
                print("读取配置文件")
                self.update_font(4, root, Label_info)
                with open(path_date_last, 'r') as json_file:
                    self.last_data_item = json.load(json_file)
            else:
                print("无法读取")
                use_net = True
        if use_net is True:
            for item in (self.price_info).find():
                data = {
                    "url": item["url"],
                    "coper_price": item["coper_price"],
                    "aluminium_price": item["aluminium_price"],
                    "num": item["num"],
                    "date": item["date"],
                }
                self.date_detal.append(data)
            self.update_font(4, root, Label_info)
            for item in self.last_data.find():
                data={
                    "date":item["date"],
                    "index":item["index"],
                    "count":item["count"],
                    "url":item["url"],
                }
                self.last_data_item=data
        self.update_font(5, root, Label_info)

    def update_font(self,step,root,Label_info):
        if root !=None and Label_info != None:
            if step == 1:
                Label_info["text"] = "获取服务器地址..."
            elif step ==2:
                Label_info["text"] = "连接服务器..."
            elif step ==3:
                Label_info["text"] = "加载数据..."
            elif step ==4:
                Label_info["text"] = "加载数据..."
            elif step ==5:
                Label_info["text"] = "加载成功！"
            root.update()
        else:
            if step == 1:
                print("获取服务器地址...")
            elif step == 2:
                print("连接服务器...")
            elif step == 3:
                print("加载数据...")
            elif step == 4:
                print("加载数据...")
            elif step == 5:
                print("加载成功！")

    def __app_init(self):
        pass

    def __get_avg(self,avg):
        avg_list = re.split(" |-|/",avg)
        if (re.match("\d{4}", avg) is not None )and (int(avg_list[0]) in range(2009,2050)):
            if re.match("\d{4}-\d{2}|\d{4}\s\d{2}", avg) and int(avg_list[1]) in range(1,13) :
                if (re.match("\d{4}-\d{2}-\d{2}|\d{4}\s\d{2}\s\d{2}", avg) is not None) and int(avg_list[2]) in range(1,13) :
                    return avg_list
                return avg_list
            return avg_list
        elif avg_list[0] == "end":
            return avg_list

    def date_trans(self,date):
        fulday_list = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        date = date.split("/")
        ful_day = fulday_list[int(date[1])]
        if (int(date[1]) == 2) and (int(date[0]) % 4 == 0):
            ful_day = ful_day + 1
        date_tmp = (float(date[2]) / ful_day)
        date_tmp = round(date_tmp, 2)
        return ((float(date[1]) - 1) + date_tmp)

    def date_judge(self,avg_list):
        flag = len(avg_list)
        date=[]
        for item in avg_list:
            a = int(item)
            date.append(a)
        fulday_list = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        ful_day = fulday_list[date[1]]
        if (int(date[1]) == 2) and (int(date[0]) % 4 == 0):
            ful_day = ful_day + 1
        return ful_day

    def get_info(self,avg):
        avg_list = self.__get_avg(avg)
        data_list =[]
        flag = len(avg_list)
        for item in self.date_detal:
            data = {
                "url": item["url"],
                "coper_price": item["coper_price"],
                "aluminium_price": item["aluminium_price"],
                "num": item["num"],
                "date": item["date"],
            }
            if flag == 1:
                if avg_list[0] in item["date"]:
                    data_list.append(data)
            elif flag == 2:
                if (avg_list[0] + '/' + avg_list[1]) in item["date"]:
                    data_list.append(data)
            elif flag == 3:
                if (avg_list[0] + '/' + avg_list[1] + '/' + avg_list[2]) in item["date"]:
                    data_list.append(data)
        data_list=sorted(data_list,key = operator.itemgetter('date'))
        return data_list


    def print_info(self,data_list):
        for item in data_list:
            print("时间:{}  铜价:{}  铝价:{}\n".format(item["date"],item["coper_price"],item["aluminium_price"]))

    def plt_list(self,data_list,date):
        date = self.__get_avg(date)
        if len(data_list) is 0:
            print("无该时间相关数据，请重新输入")
            return False
        # print(date)
        real_date = date
        flag = len(date)
        x = []
        y = []
        plt.figure(figsize=(8, 8))
        ax = plt.gca()
        if flag == 1:
            month_ticks = range(1, 13)
            plt.xlim((1, 13))
            plt.xticks(month_ticks)
            xticklabels = ["M:" + str(n) for n in range(1, len(month_ticks) + 1)]
            xticklabels[-1] = '{}'.format(int(date[0]) + 1)
            ax.set_xticks(month_ticks)
            ax.set_xticklabels(xticklabels, rotation=13)
            for item in data_list:
                y.append(item["coper_price"])
                date = item["date"]
                date = self.date_trans(date)
                x.append(date)
        elif flag ==2:
            ful_day = self.date_judge(date)
            day_ticks = range(1, ful_day+1)
            plt.xlim((1,ful_day+1))
            plt.xticks(day_ticks)
            xticklabels = [str(n) for n in range(1, len(day_ticks) + 1)]
            xticklabels[-1] = 'D:{}'.format(int(date[1])+1)
            ax.set_xticks(day_ticks)
            ax.set_xticklabels(xticklabels, rotation=13)
            for item in data_list:
                y.append(item["coper_price"])
                date = int(item["date"].split("/")[2])
                x.append(date)
        elif flag ==3:
            return False
        xlabels = ax.get_xticklabels()
        for xl in xlabels:
            xl.set_rotation(75)  # 把x轴上的label旋转15度,以免太密集时有重叠
        plt.plot(x, y)
        plt.xlabel("Date{}".format(real_date))
        plt.ylabel("Price of Coper")

    def plt_show(self):
        plt.show()

    def plt_close(self):
        plt.close('all')

    def data_backup(self):
        path = os.getcwd()
        path = path + "\\" + "Config"
        if os.path.isdir(path) is False:
            os.mkdir(path)
        path_data = path + '\\' + "coper_back_up.jason"
        path_date = path+"\\" + "last_time.jason"
        if os.path.isfile(path_date) is False:
            print("创建备份")
            with open(path_date, "w") as json_file:
                json_file.write(json.dumps(self.last_data_item))
            with open(path_data, 'w') as json_file:
                json_file.write(json.dumps(self.date_detal))
        else:
            with open(path_date,"r") as json_file:
                data = json.load(json_file)
            date =data["date"]
            if str(date) == str(self.last_data_item["date"]):
                print("无更改")
                return False
            else:
                print("修改备份")
                os.remove(path_date)
                with open(path_date, "w") as json_file:
                    json_file.write(json.dumps(self.last_data_item))
                os.remove(path_data)
                with open(path_data, 'w') as json_file:
                    json_file.write(json.dumps(self.date_detal))
                return True

    def get_price_from_url(self,url_list,last_info):
        index = last_info["count"]
        for item in url_list:
            url = item['url']
            date = item['date']
            index = index + 1
            wb_data = requests.get(weburl, headers=webheaders)
            try:
                soup = BeautifulSoup(wb_data.text, 'lxml')
                soup = soup.decode("utf-8", "ignore")
                price = (((soup.split("1#铜"))[1]).split("1#锌"))[0]
                coper_price = price.split("A00铝")[0]
                altium_price = price.split("A00铝")[1]
                coper_price = (re.findall(r"\d{5}\—\d{5}", coper_price, re.M))[0]
                altium_price = (re.findall(r"\d{5}\—\d{5}", altium_price, re.M))[0]
                data={
                    "url":url,
                    "num":str(index),
                    "date":date,
                    "coper_price":str(coper_price),
                    "aluminium_price":str(altium_price),
                }
                self.price_info.insert_one(data)
            except Exception as e:
                print(e)
                return 0
        return index


    def web_coper_crawler(self):
        url_list = self.geturl_perpage()
        url_list = self.get_real_url(url_list)
        url_list = self.judge_real_url(url_list, self.last_data_item["date"])
        print(url_list)
        if self.coper_info_update(url_list,self.last_data_item) is True:
            print("数据更新成功")
            return True
        else:
            print("数据没有更新")
            return False

    def coper_info_update(self,url_list,last_info):
        if len(url_list) == 0:
            return False
        count = self.get_price_from_url(url_list, last_info)
        if count != 0:
            self.last_data.update({"index": 0},
                             {'$set': {'date': (url_list[0])["date"], "url": (url_list[0])["url"], "count": count}})
            return True
        else:
            return False

    def geturl_perpage(slef):
        url_list =[]
        url="http://tj.copperhome.net/cjys/jiage1.html"
        wb_data = requests.get(url,headers=webheaders)
        soup = BeautifulSoup(wb_data.text,"lxml")
        links = soup.select('body > div > div.m_l.f_l > div > div.catlist > ul > li')
        for link in links:
            link =str(link)
            content = link[link.find("href")+6:link.find("target") -2]
            if "http" in content:
                date = content[content.find("net/")+4:content.find("/tongjia")]
                date = date.split("/")
                date= (date[0])[0:4] +'/'+(date[0])[4:7]+'/'+date[1]
                data ={
                    "url":content,
                    "date":date
                }
                url_list.append(data)
        return url_list
    def get_real_url(self,data_list):
        realurl_list = []
        for item in data_list:
            url = item['url']
            date = item['date']
            req = urllib.request.Request(url, headers=webheaders)
            try:
                wp = urllib.request.urlopen(req)
                content = wp.read()
                soup = content.decode('utf-8','ignore')  # utf-8解码
            except Exception as e:
                print(e)
                pass
            try:
                soup = soup.split("<title>")[1]
                soup = soup.split("</title>")[0]
                if ("基本金属行情" in soup) or ("价格行情" in soup) or ("市场行情" in soup):
                    data = {
                        "url": url,
                        "date": date
                    }
                    realurl_list.append(data)
                else:
                    pass
            except Exception as e:
                print(e)
            time.sleep(1)
        return realurl_list

    def judge_real_url(self,realurl_list, last_date):
        remove_list = []
        date_now = last_date.split("/")
        date_now = int(date_now[0]) * 10000 + int(date_now[1]) * 100 + int(date_now[2])
        for item in realurl_list:
            date_tmp = item["date"].split("/")
            date_tmp = int(date_tmp[0]) * 10000 + int(date_tmp[1]) * 100 + int(date_tmp[2])
            if date_now >= date_tmp:
                print("remove{}".format(item))
                remove_list.append(item)
        for item in remove_list:
            realurl_list.remove(item)
        return realurl_list

if __name__ == '__main__':
    coper_app = Application()
    while True:
        if coper_app.web_coper_crawler() is True:
            time.sleep(3600)
        else:
            time.sleep(300)







