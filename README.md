得益于 [zhl 同学](https://piggyzhl.top/) 提供的灵感和核心代码，我们实现了微校园每日健康打卡脚本。

这几天闲来无事，我给代码增加了 MySQL 模块，使得批量打卡高度自动化。

其实原理很简单，就是利用 Python Selenium 库控制浏览器自动操作，可以把它理解为高级的按键精灵。

源代码如下：

``` python
import time
import pymysql
from selenium import webdriver

url = 'http://202.194.40.67:9090/relax/index.html#/login.login'
path = r'/usr/local/bin/chromedriver'  # ChromeDriver 路径
db = pymysql.connect('macrohard.cn', '*****', '*****', 'check_in') # 连接数据库
cursor = db.cursor()
sql = 'select * from info'
cursor.execute(sql)
all = cursor.fetchall()
db.close()

for each in all:
    # 整理信息
    id = each[0]
    name = each[1]
    inst = each[2]
    add = each[3].split('，')
    temp = '36.5'

    # 登录系统
    wd = webdriver.Chrome(path)
    wd.implicitly_wait(20)
    wd.get(url)
    wd.find_element_by_css_selector('input[name="username"]').send_keys(id)
    wd.find_element_by_css_selector(
        'input[data-frame-id="password"]').send_keys('whsdu@' + id)
    wd.find_element_by_css_selector('button').click()
    
    # 进入问卷
    wd.find_element_by_css_selector('a.tab-button').click()
    wd.find_element_by_css_selector('span.service-catalog-name-span').click()
    time.sleep(1)
    wd.switch_to.window(wd.window_handles[1])
    
    # 填写问卷
    btns = wd.find_elements_by_css_selector(
        'div.radio.radio-primary.radio-inline')
    btns[0].click()  # 国内本科生
    wd.find_element_by_css_selector(
        'input.form-control[name="suozaixueyuan"]').send_keys(inst)  # 所在学院
    btns[7].click()  # 目前是否在校: 否
    btns[8].click()  # 今日健康状况: 健康
    btns[18].click()  # 今日本人状态: 正常
    wd.find_element_by_css_selector(
        'input.form-control[name="dangritiwen"]').send_keys(temp)  # 当日体温
    btns[23].click()  # 目前所在地: 国内
    btns[26].click()  # 今日是否外出: 否
    wd.find_element_by_css_selector(
        'div.form-group > label[title="省"] + div').click()
    wd.find_elements_by_css_selector(
        'body > div > div > label + input')[-1].send_keys(add[0])
    wd.find_element_by_css_selector('ul > li > div > div > span').click()
    wd.find_element_by_css_selector(
        'div.form-group > label[title="市"] + div').click()
    wd.find_elements_by_css_selector(
        'body > div > div > label + input')[-1].send_keys(add[1])
    wd.find_element_by_css_selector('ul > li > div > div > span').click()
    wd.find_element_by_css_selector(
        'div.form-group > label[title="区/县"] + div').click()
    wd.find_elements_by_css_selector(
        'body > div > div > label + input')[-1].send_keys(add[2])
    wd.find_element_by_css_selector('ul > li > div > div > span').click()
    wd.find_element_by_css_selector(
        'label[title="详细地址"]+input').send_keys(add[3])
    
    # 提交问卷并退出
    wd.find_element_by_css_selector('button.btn.btn-sm.btn-primary').click()
    print(name, '打卡成功')
    time.sleep(2)
    wd.quit()
```

保存信息的数据库表结构也很简单：

<img src = "https://cdn.jsdelivr.net/gh/singularity0909/cdn/img/screenshot/check_in_mysql.png" width = "600"/>

感兴趣的同学可以自己动手调试，日后若问卷页面结构发生变化，可以一起讨论改进方案。

想要体验打卡的同学可以在 [博文](https://www.macrohard.cn/archives/19/) 下方备注自己的学号，为了便于数据库读取，**仅学号即可**。

最后，希望疫情早日结束，武汉加油，中国加油！