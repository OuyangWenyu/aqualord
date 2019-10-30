import time
from selenium import webdriver

start_year = 2000  # 初始年份
end_year = 2010  # 结束年份
driver = webdriver.Chrome()
driver.get('http://data.cma.cn/user/toLogin.html')
driver.refresh()  # 刷新页面
driver.find_element_by_id("loginWeb").click()
vcode = input()  # 在代码运行窗口（非浏览器窗口）填写验证码
print(vcode)
# 填写用户名 密码 验证码
driver.find_element_by_id("userName").send_keys("*******")  # 填入用户名
driver.find_element_by_id("password").send_keys("********")  # 填入密码
driver.find_element_by_id("verifyCode").send_keys(vcode)
driver.find_element_by_id("loginPage").click()
time.sleep(4)
for i in range(start_year, end_year + 1):
    for j in range(1, 5):
        driver.switch_to_window(driver.window_handles[0])
        driver.get(
            "http://data.cma.cn/dataService/cdcindex/datacode/SURF_CLI_CHN_MUL_DAY_V3.0/show_value/normal.html")  # 填入相应数据集检索页面的地址（就是输入日期页面的地址，该地址仅为示范）
        driver.find_element_by_id("dateS").clear()
        year = '%d' % i
        month = j * 3 - 2
        start_month = '%d' % (month)
        # 月份间隔为3个月
        end_month = '%d' % (month + 2) %
        driver.find_element_by_id("dateS").send_keys(year + "-" + start_month)
        driver.find_element_by_id("dateE").clear()
        driver.find_element_by_id("dateE").send_keys(year + "-" + end_month)
        driver.find_element_by_class_name("search-bt1210").click()
        driver.switch_to_window(driver.window_handles[1])
        time.sleep(4)
        driver.find_element_by_id("buttonAddCar").click()
        time.sleep(4)
        driver.close()
