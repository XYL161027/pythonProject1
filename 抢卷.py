import time
#from info import PHONE, PASSWORD
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

def get_tracks(distance):
    # 初速度
    v = 5
    # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
    t = 0.2
    # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
    tracks = []
    # 当前的位移
    current = 0
    # 到达mid值开始减速
    mid = distance * 4 / 5
    while current < distance:
        if current < mid:
            # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
            a = 8
        else:
            a = -3
        # 初速度
        v0 = v
        # 0.2秒时间内的位移
        s = v0 * t + 0.5 * a * (t ** 2)
        # 当前的位置
        current += s
        # 添加到轨迹列表
        tracks.append(round(s))
        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t
    return tracks

# 1.1 打开浏览器
options = EdgeOptions()
options.use_chromium = True
options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" # 浏览器的位置
driver = Edge(options=options, executable_path=r"D:\TEST\pythonProject1\msedgedriver.exe") # 相应的浏览器的驱动位置
f = open('stealth.min.js', mode='r', encoding='utf-8').read()
# 移除selenium当中爬虫的特征
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': f})
driver.get("http://www.baidu.com")
# 1.2 打开登陆网页
driver.get("https://login.taobao.com")
# 1.3 输入账号, 输入密码, 点击登陆 (滑块)
try:
    # 进入内嵌页面
    driver.switch_to.frame(0)
    # 账号输入框: #fm-login-id
    driver.find_element_by_css_selector('#fm-login-id').send_keys(PHONE)
    # 密码输入框: #fm-login-password
    driver.find_element_by_css_selector('#fm-login-password').send_keys(PASSWORD)
    time.sleep(1)
    # 为什么会出现滑块, 用selenium打开的浏览器, 和正常用户打开的浏览器不同
    # 过滑块
    driver.switch_to.frame(0)
    slider = driver.find_element_by_css_selector('#nc_1_n1z')
    # 让鼠标执行 点击并且保持按住元素slider
    webdriver.ActionChains(driver).click_and_hold(on_element=slider).perform()
    # 横向移动鼠标
    webdriver.ActionChains(driver).move_by_offset(xoffset=260, yoffset=0).perform()
    # 松开鼠标
    webdriver.ActionChains(driver).pause(0.5).release().perform()
    driver.switch_to.parent_frame()
except:
    print("没有遇到滑块")
# 登陆按钮: #login-form > div.fm-btn > button
driver.find_element_by_css_selector('#login-form > div.fm-btn > button').click()
time.sleep(2)

# 2.1 打开抢购页面
driver.get(target_url)
# 2.2 点击立即购买
driver.find_element_by_css_selector('.buybtn').click()
# 2.3 点击观影人
driver.find_element_by_css_selector('.ticket-buyer-select .next-checkbox-label').click()
# 2.4 点击同意并提交
driver.find_element_by_css_selector('.submit-wrapper .next-btn.next-btn-normal.next-btn-medium').click()
time.sleep(2)

driver.switch_to.frame(0)
slider2 = driver.find_element_by_css_selector('#nc_1_n1z')
tracks = get_tracks(300)  # 剩下的50%在模拟移动
webdriver.ActionChains(driver).click_and_hold(on_element=slider2).perform()
for x in tracks:
    webdriver.ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
else:
    webdriver.ActionChains(driver).move_by_offset(xoffset=2, yoffset=0).perform()
webdriver.ActionChains(driver).pause(0.5).release().perform()