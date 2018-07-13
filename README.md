# ApkCrawler
使用requests库和beautifulsoup库编写的爬虫程序，用于爬取PC6应用市场的安卓应用

## 代码解析
### 预定义参数：
```Python
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
```

### request库处理：
请求头处理：
```Python
proxies = {
    #"http": "http://10.10.1.10:3128",
    "http": "http://210.83.203.162:80",
    "https": "http://10.10.1.10:1080",
}  # IP代理池

head= {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2669.400 QQBrowser/9.6.11148.400'}

user_agent = ['Mozilla/5.0 (Windows NT 6.1)\
    AppleWebKit/537.11 (KHTML, like Gecko)\
    Chrome/23.0.1271.64 Safari/537.11', 'Mozilla/5.0 (Windows NT 6.1; WOW64)\
    AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/47.0.2526.106 Safari/537.36', 'Mozilla/5.0 \
    (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0', "Mozilla/5.0\
    (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko)\
    Chrome/24.0.1312.56 Safari/537.17", 'Mozilla/5.0\
    (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0']
```
requests函数封装：
```Python
def request(url):
    agent = random.choice(user_agent)
    header = {'User-Agent': '%s' % agent}
    r = requests.get(url, headers=header, timeout=timeout)
    return r
```
### 核心代码：
```Python
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
        end = time.clock()
        self.show_text('总共用时: %.4f s' % (end - start), 1)
        
 def save_app(self, url, name):
        global end
        global hold_time
        global file_names
        global thread_num
        global APP_num
        global Last_num
        number = APP_num 
        try:
            app = request(url)
            if app.status_code != 200:
                return
            thread_num += 1
            save_name = name
            m = hashlib.md5()
            m.update(name.encode('utf-8'))
            name = m.hexdigest()[0:8]
            file_name = name + '.apk'
            try:
                f = open(file_name, 'ab+')
                f.write(app.content)
                Last_num += 1
                file_names.append(file_name)
                with codecs.open(name + '.txt', 'w', encoding='utf-8') as txt:
                    txt.write(save_name)
                    txt.close()
                f.close()
            except:
                traceback.print_exc()
        except:
            traceback.print_exc()
        end = time.clock()
        thread_num -= 1  # 释放该线程
        time.sleep(hold_time)  # 延迟结束
```
