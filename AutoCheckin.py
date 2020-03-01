import time
import pymysql
from selenium import webdriver

url = 'http://202.194.40.67:9090/relax/index.html#/login.login'
path = r'/usr/local/bin/chromedriver'  # ChromeDriver 路径
con = pymysql.connect('macrohard.cn', '*****', '*****', 'check_in')  # 连接数据库
cur = con.cursor()
sql = 'select * from info'
cur.execute(sql)
all = cur.fetchall()  # 获取所有打卡人信息

tim = time.localtime(time.time())  # 获取本地时间
year = str(tim.tm_year).zfill(4)
mon = str(tim.tm_mon).zfill(2)
day = str(tim.tm_mday).zfill(2)
date_now = year + mon + day  # 拼接成 yymmdd 的日期格式

# 逐个打卡
for each in all:
    # 整理信息
    id = each[0]
    name = each[1]
    inst = each[2]
    add = each[3].split('，')
    date_last = each[4]

    if (date_last == date_now):
        print(name, '今日已打卡')
        continue

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
        'input.form-control[name="dangritiwen"]').send_keys('36.5')  # 当日体温
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
    sql = "update info set date = '" + date_now + "' where id = '" + id + "'"
    cur.execute(sql)
    con.commit()
    time.sleep(2)
    wd.quit()

con.close()
