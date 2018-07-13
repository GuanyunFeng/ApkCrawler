# ApkCrawler
使用requests库和beautifulsoup库编写的爬虫程序，用于爬取PC6应用市场的安卓应用
## 代码解析
### request库处理：
请求头处理：
```Python
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
