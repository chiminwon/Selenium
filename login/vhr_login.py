from selenium import webdriver
from PIL import Image
from aip import AipOcr
import pytesseract
import time


# 验证码的获取和处理
def get_captcha():
    # 获取验证码图片
    url = 'http://127.0.0.1:8081/index.html'
    browser.get(url)
    png = browser.find_element_by_xpath('//*[@id="app"]/div/form/div[3]/div/img')
    png.screenshot('capt.png')  # 将图片截屏并保存
    # 处理验证码
    image = Image.open('capt.png')
    img = image.convert('L')  # P模式转换为L模式(灰度模式默认阈值127)
    count = 160  # 设定阈值
    table = []
    for i in range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)

    img = img.point(table, '1')

    # pixdata = img.load()
    # w, h = img.size
    # threshold = 160  # 该阈值不适合所有验证码，具体阈值请根据验证码情况设置
    # # 遍历所有像素，大于阈值的为黑色
    # for y in range(h):
    #     for x in range(w):
    #         if pixdata[x, y] < threshold:
    #             pixdata[x, y] = 0
    #         else:
    #             pixdata[x, y] = 255

    img.save('captcha.png')  # 保存处理后的验证码


# # 删除一些扰乱识别的像素点
# def delete_spot():
#     images = Image.open('captcha.png')
#     data = images.getdata()
#     w, h = images.size
#     black_point = 0
#     for x in range(1, w - 1):
#         for y in range(1, h - 1):
#             mid_pixel = data[w * y + x]  # 中央像素点像素值
#             if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
#                 top_pixel = data[w * (y - 1) + x]
#                 left_pixel = data[w * y + (x - 1)]
#                 down_pixel = data[w * (y + 1) + x]
#                 right_pixel = data[w * y + (x + 1)]
#                 # 判断上下左右的黑色像素点总个数
#                 if top_pixel < 10:
#                     black_point += 1
#                 if left_pixel < 10:
#                     black_point += 1
#                 if down_pixel < 10:
#                     black_point += 1
#                 if right_pixel < 10:
#                     black_point += 1
#                 if black_point < 1:
#                     images.putpixel((x, y), 255)
#                 black_point = 0
#     images.save('captcha2.png')  # 保存处理后的验证码


def scan_caps():
    testdata_dir_config = '--tessdata-dir "F:\\Tools\\Tesseract-OCR\\tessdata"'
    text_code = pytesseract.image_to_string(Image.open('captcha.png'), lang='eng', config=testdata_dir_config)
    print('识别结果：' + text_code)
    return text_code


# 验证码的识别
def discern_captcha():
    # 识别码
    APP_ID = '20043381'
    API_KEY = 'uYc3rdno7YrC62bldEqpgEy4'
    SECRET_KEY = 'Pwb98Y6NSEkty8slbHD7iKwpLPcURg9u'
    # 初始化对象
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    # 读取图片
    def get_file_content(file_path):
        with open(file_path, 'rb') as f:
            return f.read()

    image = get_file_content('captcha.png')
    # 定义参数变量
    options = {'language_type': 'ENG', }  # 识别语言类型，默认为'CHN_ENG'中英文混合
    #  调用通用文字识别
    result = client.basicGeneral(image, options)  # 高精度接口 basicAccurate
    for word in result['words_result']:
        captcha = (word['words'])
        print('识别结果：' + captcha)
        return captcha


# 登录网页
def login(captcha):
    # 清除账号
    browser.find_element_by_xpath('//*[@id="app"]/div/form/div[1]/div/div/input').clear()
    # 找到账号框并输入账号
    browser.find_element_by_xpath('//*[@id="app"]/div/form/div[1]/div/div/input').send_keys('admin')
    # 清除密码
    browser.find_element_by_xpath('//*[@id="app"]/div/form/div[2]/div/div/input').clear()
    # 找到密码框并输入密码
    browser.find_element_by_xpath('//*[@id="app"]/div/form/div[2]/div/div/input').send_keys('123')
    # 找到验证码框并输入验证码
    browser.find_element_by_xpath('//*[@id="app"]/div/form/div[3]/div/div/input').send_keys(captcha)
    # 找到登陆按钮并点击
    browser.find_element_by_xpath('//*[@id="app"]/div/form/button').click()


def query_employee():
    # 点击员工资料菜单
    browser.find_element_by_xpath('//*[@id="app"]/div/section/section/aside/ul/li[1]/div').click()
    # 点击基本资料菜单
    browser.find_element_by_xpath('//*[@id="app"]/div/section/section/aside/ul/li[1]/ul').click()


if __name__ == '__main__':
    browser = webdriver.Chrome()  # 实例化对象
    browser.maximize_window()

    get_captcha()
    # Baidu OCR API
    # captcha = discern_captcha()
    captcha = scan_caps()
    while captcha == '':
        get_captcha()
        captcha = scan_caps()
        time.sleep(2)
    # 万能验证码
    captcha = '1949'
    login(captcha)
    time.sleep(2)
    query_employee()

    # while browser.find_element_by_xpath('//*[@id="app"]/div/form/button'):
    #     get_captcha()
    #     captcha = scan_caps()
    #     while captcha == '':
    #         get_captcha()
    #         captcha = scan_caps()
    #         time.sleep(2)
    #     login(captcha)


    # get_file()