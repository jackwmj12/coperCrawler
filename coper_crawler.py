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

def floatrange(start,stop,steps):
    return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]

class Application():
    def __init__(self,root,Label_info):
        ip_get = ip_acquire.IpAcquire()
        info_app = info_init.LocalInfo()
        self.date_detal = []
        info_data = info_app.load(r"E:\\")
        user = info_data["mongo_user"]
        pwd = info_data["mongo_pw"]
        Label_info["text"] = "获取服务器地址..."
        root.update()
        print("获取服务器地址...")
        ip = ip_get.ip_get()
        uri = 'mongodb://' + user + ":" + pwd + "@" + ip + ":" + "27017"
        client = pymongo.MongoClient(uri)
        Label_info["text"] = "连接服务器..."
        root.update()
        print("连接服务器...")
        metal = client['金属价格']
        coper = metal['coper']
        self.urls = coper['url']
        self.real_urls = coper['real_url_2016_3']
        self.price_info = coper['price_info']
        self.lost_index = coper['lost_index']
        self.last_data = coper['last_date']
        Label_info["text"] = "加载数据..."
        root.update()
        print("加载数据...")
        for item in (self.price_info).find():
            data = {
                "url": item["url"],
                "coper_price": item["coper_price"],
                "aluminium_price": item["aluminium_price"],
                "num": item["num"],
                "date": item["date"],
            }
            self.date_detal.append(data)
        Label_info["text"] = "加载数据..."
        root.update()
        print("加载数据...")
        for item in self.last_data.find():
            data={
                "date":item["date"],
                "index":item["index"],
                "count":item["count"],
                "url":item["url"],
            }
            self.last_data=data
        # self.data_backup()
        Label_info["text"] ="加载成功！"
        root.update()
        print("加载成功!")

    def get_avg(self,avg):
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
        avg_list = self.get_avg(avg)
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
        date = self.get_avg(date)
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
                json_file.write(json.dumps(self.last_data))
            with open(path_data, 'w') as json_file:
                json_file.write(json.dumps(self.date_detal))
        else:
            with open(path_date,"r") as json_file:
                data = json.load(json_file)
            date =data["date"]
            if str(date) == str(self.last_data["date"]):
                print("无更改")
                return
            else:
                print("修改备份")
                os.remove(path_date)
                with open(path_date, "w") as json_file:
                    json_file.write(json.dumps(self.last_data))
                os.remove(path_data)
                with open(path_data, 'w') as json_file:
                    json_file.write(json.dumps(self.date_detal))


# if __name__ == '__main__':
#     info_detal = Application()
#     while True:
#         avg_list = info_detal.get_avg()
#         data_list = info_detal.get_info(avg_list)
#         info_detal.print_info(data_list)
#         info_detal.plt_list(data_list,avg_list)
#         if avg_list[0] == "end":
#             info_detal.plt_show()







