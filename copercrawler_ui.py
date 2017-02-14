import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import time
import coper_crawler
import re
import json
import os
import win32api
from win32api import GetSystemMetrics


class Application():
    def __init__(self,main):
        self.path = os.getcwd()
        self.author = "林聪聪"
        self.version = "1.2.6"
        self.__update_init()
        self.root = main
        self.root2 = tk.Toplevel(self.root)
        self.root2.withdraw()
        self.root.withdraw()
        font,Label_info = self.show_font()
        self.info_detal=coper_crawler.Application(font,Label_info,use_net = True)
        self.date =time.strftime("%Y-%m-%d")
        self.coper_price_today,self.aluminium_price_today,self.price_show_date = self.get_miss_date(self.date)
        self.histy_price_preday = self.get_histry_date(self.date)
        self.createFrameTop()
        self.createFrameBody()
        self.createFrameBottom()
        font.withdraw()
        main.deiconify()

    def show_font(self):
        font = tk.Toplevel(self.root)
        font.geometry('500x100+500+400')
        Label_info = tk.Label(font, text="程序启动", fg='blue')
        Label_info.place(x=230, y=20)
        return font,Label_info

    def date_mins(self,date):
        date = date.split("-")
        day = int(date[2]) -1
        if day <10:
            date = date[0]+'-'+date[1]+'-'+'0'+str(day)
        else :
            date = date[0] + '-' + date[1] + '-'+ str(day)
        if day == 0:
            date =None
        return date

    def get_miss_date(self,date):
        while True:
            coper_price = (self.info_detal.get_info(date))
            aluminium_price = (self.info_detal.get_info(date))
            if coper_price == []:
                date = self.date_mins(date)
                if date == None:
                    return None,None,None
            else:
                return (coper_price[0])["coper_price"],(aluminium_price[0])["aluminium_price"],(coper_price[0])["date"]

    def get_histry_date(self, date):
        date_list = []
        date=date.split("-")
        year_list = ["2011","2012","2013","2014","2015","2016"]
        for year in year_list:
            date_tmp = year+'-'+date[1]+'-'+date[2]
            coper_price,aluminium_price,date_unuse=self.get_miss_date(date_tmp)
            data={
                "coper_price":coper_price,
                "aluminium_price":aluminium_price,
                "date":date_tmp,
            }
            date_list.append(data)
        return date_list

    def createFrameTop(self):
        self.root.geometry('600x600+150+100')
        self.frm_top_label_0 = tk.Label(self.root,text='铜价查看器',fg='blue',font=("TEMPUS Sans ITC",20))
        self.frm_top_label_0.place(x=300,y=15,anchor="center")

        self.frm_top_label_1 =tk.Label(self.root,text='今日时间:{}'.format(self.date),fg='blue',font=("TEMPUS Sans ITC",10))
        self.frm_top_label_1.place(x=440,y=10,anchor="w")

        self.frm_top_label_1 = tk.Label(self.root, text='今日铜价:{}'.format(self.coper_price_today), fg='blue',font=("TEMPUS Sans ITC", 10))
        self.frm_top_label_1.place(x=440,y=30,anchor="w")

        self.frm_top_label_1 = tk.Label(self.root, text='今日铝价:{}'.format(self.aluminium_price_today), fg='blue',font=("TEMPUS Sans ITC", 10))
        self.frm_top_label_1.place(x=440, y=50, anchor="w")

        self.frm_top_label_1 = tk.Label(self.root, text='价格所在时间:{}'.format(self.price_show_date), fg='blue',font=("TEMPUS Sans ITC", 10))
        self.frm_top_label_1.place(x=440, y=70, anchor="w")

        self.frm_top_menubar = tk.Menu(self.root)
        self.frm_top_menu_file = tk.Menu(self.frm_top_menubar,tearoff=0)
        self.frm_top_menu_file.add_command(label="保存数据",command=self.data_backup)
        self.frm_top_menu_file.add_command(label="打开数据",command=self.data_open)
        self.frm_top_menu_file.add_command(label="Exit", command=self.root.quit)
        self.frm_top_menubar.add_cascade(label="文件", menu=self.frm_top_menu_file)

        self.frm_top_menu_about = tk.Menu(self.frm_top_menubar, tearoff=0)
        self.frm_top_menu_about.add_command(label="检查更新", command=self.program_update)
        self.frm_top_menu_about.add_command(label="关于", command=self.program_about)
        self.frm_top_menubar.add_cascade(label="说明", menu=self.frm_top_menu_about)
        self.root.config(menu=self.frm_top_menubar)

    def createFrameBody(self):
        self.frm_body = tk.LabelFrame(self.root)

        self.frm_body_Label_0 = tk.Label(self.root, text="区间查看",fg='blue',font=("TEMPUS Sans ITC", 12))
        self.frm_body_Label_0.place(x=20,y=90)

        self.frm_body_Label_0=tk.Label(self.root, text="开始年限:")
        self.frm_body_Label_0.place(x=150,y=70,anchor="w")

        self.frm_body_start_date = tk.StringVar()
        self.frm_body_entry_0=tk.Entry(self.root,textvariable=self.frm_body_start_date,width=10)
        self.frm_body_entry_0.place(x=150,y=100,anchor="w")

        self.frm_body_Label_1=tk.Label(self.root, text="结束年限:")
        self.frm_body_Label_1.place(x=270,y=70,anchor="w")

        self.frm_body_stop_date = tk.StringVar()
        self.frm_body_entry_1 = tk.Entry(self.root, textvariable=self.frm_body_stop_date,width=10)
        self.frm_body_entry_1.place(x=270,y=100,anchor="w")

        self.frm_body_Button_0=tk.Button(self.root,relief=tk.SOLID, bd=1, text="确定", command=self.button_0_process)
        self.frm_body_Button_0.place(x=400,y=95,anchor="w")

        '''
        第一排结束，开始第二排
       '''
        self.frm_body_Label_2 = tk.Label(self.root, text="单月查看", fg='blue',font=("TEMPUS Sans ITC", 12))
        self.frm_body_Label_2.place(x=20,y=150)

        self.frm_body_Label_2 = tk.Label(self.root, text="年份:")
        self.frm_body_Label_2.place(x=150,y=130)

        self.frm_body_year_date = tk.StringVar()
        self.frm_body_entry_2 = tk.Entry(self.root, textvariable=self.frm_body_year_date,width=10)
        self.frm_body_entry_2.place(x=150,y=160)

        self.frm_body_Label_3 = tk.Label(self.root, text="月:")
        self.frm_body_Label_3.place(x=270,y=130)

        self.frm_body_month_date = tk.StringVar()
        self.frm_body_entry_3 = tk.Entry(self.root, textvariable=self.frm_body_month_date,width=10)
        self.frm_body_entry_3.place(x=270,y=160)

        self.frm_body_Button_2 = tk.Button(self.root, relief=tk.SOLID, bd=1, text="确定", command=self.button_1_process)
        self.frm_body_Button_2.place(x=400,y=155)

        '''
            第二排结束，开始第三排
       '''
        self.frm_body_Label_4 = tk.Label(self.root, text="单日查看", fg='blue',font=("TEMPUS Sans ITC", 12))
        self.frm_body_Label_4.place(x=20,y=210)

        self.frm_body_Label_4 = tk.Label(self.root, text="年份:")
        self.frm_body_Label_4.place(x=150,y=190)

        self.frm_body_year_date1 = tk.StringVar()
        self.frm_body_entry_4 = tk.Entry(self.root, textvariable=self.frm_body_year_date1,width=10)
        self.frm_body_entry_4.place(x=150,y=220)

        self.frm_body_Label_5 = tk.Label(self.root, text="月:")
        self.frm_body_Label_5.place(x=270,y=190)

        self.frm_body_month_date1 = tk.StringVar()
        self.frm_body_entry_5 = tk.Entry(self.root, textvariable=self.frm_body_month_date1,width =10)
        self.frm_body_entry_5.place(x=270,y=220)

        self.frm_body_Label_6 = tk.Label(self.root, text="日:")
        self.frm_body_Label_6.place(x=390,y=190)

        self.frm_body_day_date1 = tk.StringVar()
        self.frm_body_entry_6 = tk.Entry(self.root, textvariable=self.frm_body_day_date1,width=10)
        self.frm_body_entry_6.place(x=390,y=220)

        self.frm_body_Button_3 = tk.Button(self.root, relief=tk.SOLID, bd=1, text="确定", command=self.button_2_process)
        self.frm_body_Button_3.place(x=520,y=215)



        self.frm_body_Label_12 = tk.Label(self.root, text="单日 查询日期:", fg='blue')
        self.frm_body_Label_12.place(x=410,y=280)

        self.frm_body_Label_6 = tk.Label(self.root, text="单日 铜价 查询结果:",fg = 'blue')
        self.frm_body_Label_6.place(x=410,y=310)

        self.frm_body_Label_7 = tk.Label(self.root, text="单日 铝价 查询结果:", fg='blue')
        self.frm_body_Label_7.place(x=410,y=340)

        self.frm_body_Label_13 = tk.Label(self.root, text="无")
        self.frm_body_Label_13.place(x=525,y=280)

        self.frm_body_Label_8 = tk.Label(self.root, text="无")
        self.frm_body_Label_8.place(x=525,y=310)

        self.frm_body_Label_9 = tk.Label(self.root, text="无")
        self.frm_body_Label_9.place(x=525,y=340)


    def createFrameBottom(self):
        self.frm_bottom_Label_4 = tk.Label(self.root, text="版本号: {}".format(self.version), fg='blue')
        self.frm_bottom_Label_4.place(x=580,y=570,anchor="se")

        self.frm_bottom_Label_5 = tk.Label(self.root, text="制作: {}".format(self.author), fg='blue')
        self.frm_bottom_Label_5.place(x=578,y=550,anchor="se")

        self.frm_body_Button_3 = tk.Button(self.root, relief=tk.SOLID, bd=1, text="关闭图形",command=self.button_3_process)
        self.frm_body_Button_3.place(x=530,y=145,anchor="se")

        self.v = tk.IntVar()
        self.frm_body_radiobutton_0 = tk.Radiobutton(self.root, text="不显示历史数据", variable=self.v, value=1, command=lambda: self.show_histry_price(1)).place(x=10, y=280)
        self.frm_body_radiobutton_1 = tk.Radiobutton(self.root, text="显示历史数据", variable=self.v, value=2, command=lambda: self.show_histry_price(2)).place(x=150, y=280)

        self.root.update

    def button_0_process(self):
        start_year=self.frm_body_entry_0.get()
        stop_year=self.frm_body_entry_1.get()
        print(len(start_year))
        if ((len(start_year) == 0) or (len(stop_year) == 0) or self.date_judge(str(stop_year)) is False) or (self.date_judge(str(start_year))is False):
            self.output_error(1)
            return
        start_year= int(self.frm_body_entry_0.get())
        stop_year= int(self.frm_body_entry_1.get())+1
        if start_year >=stop_year:
            self.output_error(1)
            return
        for year in range(start_year,stop_year):
            data_list = self.info_detal.get_info(str(year))
            self.info_detal.plt_list(data_list,str(year))
        self.info_detal.plt_show()

    def button_1_process(self):
        date = None
        date_year = self.frm_body_entry_2.get()
        date_month = self.frm_body_entry_3.get()
        if len(date_year) is not 0 and len(date_month) is not 0:
            date = date_year+'-'+date_month
        if self.date_judge(date) is False:
            self.output_error(1)
            return
        date = self.date_compensation(date)
        data_list =self.info_detal.get_info(date)
        self.info_detal.plt_list(data_list,date)
        self.info_detal.plt_show()

    def button_2_process(self):
        date = None
        date_year = self.frm_body_entry_4.get()
        date_month = self.frm_body_entry_5.get()
        date_day = self.frm_body_entry_6.get()
        if len(date_year) is not 0 and len(date_month) is not 0 and len(date_day) is not 0:
            date = date_year + '-' + date_month + "-" + date_day
        if self.date_judge(date) is False:
            self.output_error(1)
            return
        date = self.date_compensation(date)
        print(date)
        coper_price,aluminium_price,date=self.get_miss_date(date)
        if coper_price is None:
            self.frm_body_Label_8['text'] = "无"
            self.frm_body_Label_9['text'] = "无"
        else:
            self.frm_body_Label_8['text'] = coper_price
            self.frm_body_Label_9['text'] = aluminium_price
            self.frm_body_Label_13['text'] = date
        self.root.update()

    def button_3_process(self):
        self.info_detal.plt_close()


    def output_error(self,errornum):
        errornum = int(errornum)
        if errornum ==1:
            messagebox.showerror('中国沈力电机科技股份有限公司', '输入错误')

    def date_compensation(self,date):
        date=date.split("-")
        if len(date)>=2:
            month_tmp = re.match('\d{2}', date[1])
            if (re.match('\d{1}', date[1])) and month_tmp is None:
                date[1] = '0' + date[1]
        if len(date)==3:
            day_tmp = re.match('\d{2}', date[2])
            if (re.match('\d{1}', date[2])) and day_tmp is None:
                date[2] = '0' + date[2]
            return date[0] + '-' + date[1] + '-' + date[2]
        return date[0] + '-' + date[1]

    def date_judge(self,date):
        print("输入时间为{}".format(date))
        if date is None:
            return False
        max_year = int(self.date.split('-')[0]) + 1
        date =date.split("-")
        if int(date[0]) < 2010 or int(date[0]) >= max_year:
            return False
        if len(date)>=2:
            if int(date[1])>12 or int(date[1])<1:
                return False
        if len(date)>2:
            if int(date[2])>31 or int(date[2])<1:
                return False
        return True

    def data_backup(self):
        world = simpledialog.askstring('中国沈力电机科技股份有限公司', '请输入指令', initialvalue='在此输入')
        if str(world) =='backup':
            if self.info_detal.data_backup() is True:
                messagebox.showinfo('中国沈力电机科技股份有限公司', '保存成功')
            else:
                messagebox.showinfo('中国沈力电机科技股份有限公司', '无需更新')
        else:
            messagebox.showinfo('中国沈力电机科技股份有限公司', '无效指令')
    def data_open(self):
        messagebox.showinfo('中国沈力电机科技股份有限公司', '暂无此功能')

    def __update_init(self):
        path = self.path + "\\" + "update"
        if os.path.isdir(path) is False:
            os.mkdir("update")
        path = path + "\\"+'update_config.jason'
        data = {
            "version": self.version,
            "path": path,
            "filename": "copercrawler"
        }
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(data))

    def program_update(self):
        update_soft_path = self.path + "\\" +"myupdate.exe"
        win32api.ShellExecute(0, 'open', update_soft_path, '', '', 0)
        self.root.quit()

    def program_about(self):
        messagebox.showinfo('中国沈力电机科技股份有限公司', '版本号:{}\n制作者:{}'.format(self.version,self.author))

    def show_histry_price(self,flag):
        self.root2.geometry('410x180+150+520')
        if flag ==1:
            self.root2.withdraw()
        else:
            self.frm_bottom_Label_0 = tk.Label(self.root2, text="历史本日价格:2016年 铜", fg='blue')
            self.frm_bottom_Label_0.place(x=20, y=10)
            self.frm_bottom_Label_1 = tk.Label(self.root2, text=(self.histy_price_preday[5]["coper_price"]))
            self.frm_bottom_Label_1.place(x=165, y=10)

            self.frm_bottom_Label_2 = tk.Label(self.root2, text="历史本日价格:2016年 铝", fg='blue')
            self.frm_bottom_Label_2.place(x=220, y=10)
            self.frm_bottom_Label_3 = tk.Label(self.root2, text=(self.histy_price_preday[5])["aluminium_price"])
            self.frm_bottom_Label_3.place(x=365, y=10)

            self.frm_bottom_Label_0 = tk.Label(self.root2, text="历史本日价格:2015年 铜", fg='blue')
            self.frm_bottom_Label_0.place(x=20, y=40)
            self.frm_bottom_Label_1 = tk.Label(self.root2, text=(self.histy_price_preday[4]["coper_price"]))
            self.frm_bottom_Label_1.place(x=165, y=40)

            self.frm_bottom_Label_2 = tk.Label(self.root2, text="历史本日价格:2015年 铝", fg='blue')
            self.frm_bottom_Label_2.place(x=220, y=40)
            self.frm_bottom_Label_3 = tk.Label(self.root2, text=(self.histy_price_preday[4])["aluminium_price"])
            self.frm_bottom_Label_3.place(x=365, y=40)

            self.frm_bottom_Label_0 = tk.Label(self.root2, text="历史本日价格:2014年 铜", fg='blue')
            self.frm_bottom_Label_0.place(x=20, y=70)
            self.frm_bottom_Label_1 = tk.Label(self.root2, text=(self.histy_price_preday[3]["coper_price"]))
            self.frm_bottom_Label_1.place(x=165, y=70)

            self.frm_bottom_Label_2 = tk.Label(self.root2, text="历史本日价格:2014年 铝", fg='blue')
            self.frm_bottom_Label_2.place(x=220, y=70)
            self.frm_bottom_Label_3 = tk.Label(self.root2, text=(self.histy_price_preday[3])["aluminium_price"])
            self.frm_bottom_Label_3.place(x=365, y=70)

            self.frm_bottom_Label_0 = tk.Label(self.root2, text="历史本日价格:2013年 铜", fg='blue')
            self.frm_bottom_Label_0.place(x=20, y=100)
            self.frm_bottom_Label_1 = tk.Label(self.root2, text=(self.histy_price_preday[2]["coper_price"]))
            self.frm_bottom_Label_1.place(x=165, y=100)

            self.frm_bottom_Label_2 = tk.Label(self.root2, text="历史本日价格:2013年 铝", fg='blue')
            self.frm_bottom_Label_2.place(x=220, y=100)
            self.frm_bottom_Label_3 = tk.Label(self.root2, text=(self.histy_price_preday[2])["aluminium_price"])
            self.frm_bottom_Label_3.place(x=365, y=100)

            self.frm_bottom_Label_0 = tk.Label(self.root2, text="历史本日价格:2012年 铜", fg='blue')
            self.frm_bottom_Label_0.place(x=20, y=130)
            self.frm_bottom_Label_1 = tk.Label(self.root2, text=(self.histy_price_preday[1]["coper_price"]))
            self.frm_bottom_Label_1.place(x=165, y=130)

            self.frm_bottom_Label_2 = tk.Label(self.root2, text="历史本日价格:2012年 铝", fg='blue')
            self.frm_bottom_Label_2.place(x=220, y=130)
            self.frm_bottom_Label_3 = tk.Label(self.root2, text=(self.histy_price_preday[1])["aluminium_price"])
            self.frm_bottom_Label_3.place(x=365, y=130)
            self.root2.deiconify()

def Create_win(font):
    font.geometry('500x100+500+400')
    Label_info = tk.Label(font, text="程序启动", fg='blue')
    Label_info.place(x=230, y=20)
    Application(font,Label_info)

if __name__  == "__main__":
    main=tk.Tk()
    main.title("沈力电机科技股份有限公司")
    Application(main)
    main.mainloop()



