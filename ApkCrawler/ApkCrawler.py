# -*-coding:utf-8 -*-

'''
用于爬取pc6应用市场的安卓应用
使用md5前8位作为文件名，生成同名文档写入应用名称
'''

import requests  # 处理网络请求的模块
import os  # 导入os模块
import threading  # 处理线程的模块
import time
import random
import codecs
import traceback
import hashlib  # 生成MD5
import json
from bs4 import BeautifulSoup  # 进行网页解析的模块
from tkinter import *  # 自带的图形化模块

global start  # 程序开始时间
global end  # 程序结束时间
global hold_time  # 两次网络请求的时间间隔

file_names = []  # 已下载app
APP_url = ''  # 要下载的APP地址
APP_name = ''  # 要下载的APP名称
APP_num = 0  # 已下载APP总数
Last_num = 0  # 最终下载总数
thread_num = 0  # 线程编号
timeout = 10.0  # 超时时间设置
numpage = 3 # 爬取3页的代理IP

proxies = {
    #"http": "http://10.10.1.10:3128",
    "http": "http://210.83.203.162:80",
    "https": "http://10.10.1.10:1080",
}  # IP代理池

l_app = ['摄影摄像', '聊天社交', '影音播放', '系统工具', '网络通讯',
         '生活服务', '安全防护', '资讯阅读', '交通导航', '金融理财',
         '效率办公', '游戏辅助', '美食菜谱', '运动健身', '丽人母婴',
         '网络购物', '健康医疗', '旅游出行', '学习教育', 'O2O软件',
         '趣味娱乐', '主题美化', '桌面扩展', '动态壁纸', '美女壁纸']
l_app_url = ['588_', '589_', '584_', '582_', '583_',
             '585_', '586_', '587_', '600_', ' qq_703_',
             'qq_704_', 'qq_708_', 'qq_709_', '875_', '876_',
             '877_', '878_', '879_', '880_', '881_',
             '628_', 'qq_705_', 'qq_706_', '627_', '599_']

# 给请求指定一个请求头来模拟chrome浏览器
head= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2669.400 QQBrowser/9.6.11148.400'}
# 随机模拟浏览器Request Headers的User-Agent
user_agent = ['Mozilla/5.0 (Windows NT 6.1)\
AppleWebKit/537.11 (KHTML, like Gecko)\
Chrome/23.0.1271.64 Safari/537.11', 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/47.0.2526.106 Safari/537.36', 'Mozilla/5.0 \
(Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0', "Mozilla/5.0\
(X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko)\
Chrome/24.0.1312.56 Safari/537.17", 'Mozilla/5.0\
(Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0']


# 保存APK文件的线程类
class MyThread(threading.Thread):
    def run(self):
        global APP_url  # 当前要保存APP的下载地址
        global APP_name  # 当前要保存APP的名称
        self.save_app(APP_url, APP_name)

    # 下载并保存APP
    def save_app(self, url, name):
        global end
        global hold_time
        global file_names
        global thread_num
        global APP_num
        global Last_num
        number = APP_num 
        print('开始请求APP地址...')
        try:
            app = request(url)
            if app.status_code != 200:
                print('下载请求失败...')
                print('返回码:', str(app.status_code))
                return
            thread_num += 1
            print('开始保存APP:', name)
            save_name = name
            m = hashlib.md5()
            m.update(name.encode('utf-8'))
            name = m.hexdigest()[0:8]
            file_name = name + '.apk'
            try:
                f = open(file_name, 'ab+')
                f.write(app.content)
                print('第' + str(number + 1) + '个APP:' + file_name + '保存成功！')
                Last_num += 1
                file_names.append(file_name)
                with codecs.open(name + '.txt', 'w', encoding='utf-8') as txt:
                    txt.write(save_name)
                    txt.close()
                f.close()
            except:
                print('第' + str(number + 1) + '个APP:' + file_name + '保存失败！')
                traceback.print_exc()
        except:
            print('下载请求失败...')
            traceback.print_exc()
        end = time.clock()
        print('当前APP下载总数:', str(Last_num))
        print('当前所用时间: %.4f s' % (end - start))
        thread_num -= 1  # 释放该线程
        time.sleep(hold_time)  # 延迟结束


class BeautifulAPP():
    # 类的初始化操作
    def __init__(self):
        # 初始化图形化界面
        #self.page_num = 0  # 当前下载页面
        self.per_page_num = 40  # 每页下载量
        self.root = Tk()  # 创建窗口对象实例
        self.root.title('pc6应用市场助手爬虫程序')

        # 下面的这些控件的使用方法自行查阅tkinter提供的方法
        self.frame_text = Frame(self.root, borderwidth=4, relief=RAISED)
        self.text = Text(self.frame_text, font=('宋体', 14))
        self.text.tag_config('a', font=('宋体', 14, 'bold'))
        scroll_text = Scrollbar(self.frame_text, command=self.text.yview)
        self.text.configure(yscrollcommand=scroll_text.set)
        self.text.pack(side=LEFT)
        scroll_text.pack(side=RIGHT, fill=Y)
        self.text.insert(END, '准备运行...\n')  # 这个END表示显示在Text buffer的最后一个字符
        self.frame_text.pack(side=LEFT)

        # 输入框
        self.frame_hold_time = Frame(self.root, borderwidth=4, relief=RAISED)
        Label(self.frame_hold_time, text='延迟时间(s)').pack(side=LEFT)
        self.e1 = IntVar()
        Entry(self.frame_hold_time, width=5, textvariable=self.e1).pack(side=RIGHT)
        self.e1.set(15)
        self.frame_hold_time.pack(anchor=W)

        self.frame_web_url = Frame(self.root, borderwidth=4, relief=RAISED)
        Label(self.frame_web_url, text='根网址').pack(side=LEFT)
        self.e2 = StringVar()
        Entry(self.frame_web_url, width=20, textvariable=self.e2, state=DISABLED).pack(side=RIGHT)
        self.e2.set('http://www.pc6.com/android/')
        self.frame_web_url.pack(anchor=W)

        self.frame_APP_max = Frame(self.root, borderwidth=4, relief=RAISED)
        Label(self.frame_APP_max, text='下载量').pack(side=LEFT)
        self.e3 = IntVar()
        Entry(self.frame_APP_max, width=5, textvariable=self.e3).pack(side=RIGHT)
        self.e3.set(1500)
        self.frame_APP_max.pack(anchor=W)

        self.frame_thread_max = Frame(self.root, borderwidth=4, relief=RAISED)
        Label(self.frame_thread_max, text='线程数').pack(side=LEFT)
        self.e4 = IntVar()
        Entry(self.frame_thread_max, width=5, textvariable=self.e4).pack(side=RIGHT)
        self.e4.set(8)
        self.frame_thread_max.pack(anchor=W)

        self.frame_thread_max = Frame(self.root, borderwidth=4, relief=RAISED)
        Label(self.frame_thread_max, text='开始页数').pack(side=LEFT)
        self.e6 = IntVar()
        Entry(self.frame_thread_max, width=5, textvariable=self.e6).pack(side=RIGHT)
        self.e6.set(1)
        self.frame_thread_max.pack(anchor=W)

        self.frame_folder_path = Frame(self.root, borderwidth=4, relief=RAISED)
        Label(self.frame_folder_path, text='根存储').pack(side=LEFT)
        self.e5 = StringVar()
        Entry(self.frame_folder_path, width=20, textvariable=self.e5).pack(side=RIGHT)
        self.e5.set('E:\\apk\\pc6')
        self.frame_folder_path.pack(anchor=W)

        self.frame_classify_app = Frame(self.root, borderwidth=4, relief=RAISED)
        Label(self.frame_classify_app, text='应用分类').pack(side=LEFT)
        self.classify_app = Listbox(self.frame_classify_app, height=10, width=20)
        scroll_app = Scrollbar(self.frame_classify_app, command=self.classify_app.yview)
        self.classify_app.configure(yscrollcommand=scroll_app.set)
        self.classify_app.pack(side=LEFT)
        scroll_app.pack(side=RIGHT, fill=Y)
        for item in l_app:
            self.classify_app.insert(END, item)
        self.frame_classify_app.pack(anchor=W)

        Button(self.root, text='Start', borderwidth=4, relief=RAISED, command=self.RUN).pack(side=LEFT)
        Button(self.root, text='Reset', borderwidth=4, relief=RAISED, command=self.Reset).pack(side=LEFT)
        Button(self.root, text='Clear', borderwidth=4, relief=RAISED, command=self.Clear).pack(side=LEFT)
        self.text.focus_force()
        self.root.mainloop()

    def get_app(self):
        global start
        global hold_time
        global file_names
        global APP_url
        global APP_name
        global APP_num
        global Last_num
        global thread_num
        start = time.clock()
        self.show_text('创建文件夹', 0)
        self.mkdir(self.folder_path)
        self.show_text('切换文件夹', 0)
        os.chdir(self.folder_path)
        file_names = self.get_files(self.folder_path)
        threads = []
        while (APP_num < self.APP_max):
            self.per_page_num = 0
            download_links = []
            self.show_text('当前所在页面: Page' + str(self.page_num), 0)
            self.page = str(self.page_num)
            self.show_text('进行网页get请求', 0)
            
            # 构造请求的初始网址：根网址 + APP小类 + 页码
            r = request(self.web_url + self.type_classify + self.page + ".html" )
            r.encoding = 'utf-8'
            self.show_text('进入APP详细页面', 0)
            soup=BeautifulSoup(r.content, 'lxml')
            all_a = soup.find('dl',id='listCont').find_all('p')
            for a in all_a:
                if APP_num >= self.APP_max:
                    break
                APP_url = "http://www.pc6.com" + a.find('a', class_="btn")["href"]
                APP_name = a.find('i').string
                if APP_name + '.apk' in file_names:
                    print('APP:' + APP_name + '.apk 已存在')
                    self.show_text('APP:' + APP_name + '.apk 已存在', 0)
                # 有空闲的下载线程
                elif thread_num < self.thread_max:
                    print('APP:' + APP_name + '.apk 开始下载')
                    self.show_text('NO.' + str(APP_num + 1) + ' APP:' + APP_name + '.apk 开始下载', 1)
                    print('下载地址:', APP_url)
                    # 创建新的线程来保存APP
                    t = MyThread()
                    t.start()
                    APP_num += 1
                    # 加入总的子线程列表
                    threads.append(t)
                    # 两次网络请求的间隔时间
                    time.sleep(hold_time)
                # 无空闲的下载线程
                else:
                    print('APP:' + APP_name + '.apk 正等待其余下载线程结束...')
                    self.show_text('NO.' + str(APP_num + 1) + ' APP:' + APP_name + '.apk 正等待其余下载线程结束...', 1)
                    # 每隔1s判断是否有空余子线程
                    while (thread_num >= self.thread_max):
                        time.sleep(1)  # 延时1s
                    print('APP:' + APP_name + '.apk 开始下载')
                    self.show_text('NO.' + str(APP_num + 1) + ' APP:' + APP_name + '.apk 开始下载', 1)
                    print('下载地址:', APP_url)
                    t = MyThread()
                    t.start()
                    APP_num += 1
                    self.per_page_num += 1
                    threads.append(t)
                    time.sleep(hold_time)
            if (per_page_num < 1):
                break
            self.page_num += 1
            self.e6.set(self.page_num)
        # 等待所有线程结束
        for t in threads:
            t.join()
        if APP_num == self.APP_max:
            print('任务完成')
            self.show_text('任务完成', 1)
        # 下载量没达到设置的最大值，表示该类APP的下载量已达网页最大
        else:
            print('页面已达最大')
            self.show_text('页面已达最大', 1)
        end = time.clock()
        self.show_text('总共用时: %.4f s' % (end - start), 1)

    # 获取文件夹中的文件名称列表
    def get_files(self, path):
        app_names = os.listdir(path)
        return app_names

    # 创建文件夹
    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
        else:
            print(path, '文件夹已经存在了，不再创建')

    # 开始下载
    def RUN(self):
        while 1:
            global hold_time
            # 从输入框中获取参数
            hold_time = int(self.e1.get())
            self.web_url = self.e2.get()
            self.APP_max = int(self.e3.get())
            self.thread_max = int(self.e4.get())
            self.root_folder = self.e5.get()  # 获得输入的存储路径
            self.page_num = int(self.e6.get())
            self.show_text('延迟时间:' + str(hold_time), 0)
            self.show_text('下载量:' + str(self.APP_max), 0)
            self.show_text('线程数:' + str(self.thread_max), 0)
            self.show_text('根网址:' + self.web_url, 0)
            self.show_text('根存储:' + self.root_folder, 0)

            l_url = self.classify_app.curselection()
            if len(l_url):
            # 根据预设的列表，找到对应类别的网址特征(l_app_url 和 l_app)
                self.type_classify = l_app_url[l_url[0]]
            # 构造该类APP的保存路径
                self.folder_path = self.root_folder + '\\' + l_app[l_url[0]]
            else:
                self.type_classify = ''
                self.folder_path = self.root_folder + '\综合'
            self.get_app()
            time.sleep(600)   #每隔600秒刷新一次
            self.e4.set(self.thread_max+2)
            self.e1.set(hold_time+5)

    # 重置下载数量和页面位置
    def Reset(self):
        global APP_num
        global Last_num
        Last_num = 0
        APP_num = 0
        self.page_num = 1

    # 显示程序输出
    def show_text(self, info, type):
        if type:
            self.text.insert(END, info + '\n', 'a')
        else:
            self.text.insert(END, info + '\n')
        self.text.see(self.text.index(END))  # 锁定在最后一行，跟进程序输出
        self.text.update()

    # 清空text内容
    def Clear(self):
        self.text.delete(1.0, END)
        self.text.insert(END, '准备运行...\n')


# 返回网页的response
def request(url):
    agent = random.choice(user_agent)
    header = {'User-Agent': '%s' % agent}
    # 向目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
    # allow_redirects = False 禁止状态跳转,此处需要跳转到下载页面
    r = requests.get(url, headers=header, timeout=timeout)
    return r


APP = BeautifulAPP()

