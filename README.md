# ApkCrawler
使用requests库和beautifulsoup库编写的爬虫程序，用于爬取PC6应用市场的安卓应用
## 代码解析
核心代码：
···Python
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
