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
