# ApkCrawler
使用requests库和beautifulsoup库编写的爬虫程序，用于爬取PC6应用市场的安卓应用
## 代码解析
核心代码：
···python

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
```
