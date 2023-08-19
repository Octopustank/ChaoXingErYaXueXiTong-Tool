from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException

import importlib as ipt
import json



class Browser:
    def __init__(self, browser=None, browser_path=None, plugin_unit=None, data_path=None): #初始化selenium浏览器
        if None in (browser, browser_path) and data_path is not None: #传值支持从文件读取数据运行程序
            with open(data_path, "r", encoding="utf-8") as f:
                dic = json.load(f)
            browser = dic["browser"]
            browser_path = dic["browser_path"]
            plugin_unit = dic["plugin_unit"]
        elif None in (browser, browser_path) and data_path is None: #传值缺失，无法进行任意一种模式
            print("[ selenium ] 信息缺失")
            exit()
        #else：传值支持使用传入的数据运行程序
        selenium_webdriver = ipt.import_module("selenium.webdriver")
        BrowserOptions = eval(f"selenium_webdriver.{browser}Options") #动态导入实现不同浏览器的导入
        Browser = eval(f"selenium_webdriver.{browser}")
        selenium_webdriver_browser_service = ipt.import_module(f"selenium.webdriver.{browser.lower()}.service")
        Service = selenium_webdriver_browser_service.Service
        if plugin_unit is None: #浏览区插件未指明，默认自动
            if browser == "Edge": #Edge调用名格式不同
                webdriverManager_browser = ipt.import_module("webdriver_manager.microsoft")
            else:
                webdriverManager_browser = ipt.import_module(f"webdriver_manager.{browser.lower()}")
            manager_name = {"Firefox": "GeckoDriverManager", "Chrome": "ChromeDriverManager", "Edge": "EdgeChromiumDriverManager"}[browser]
            DriverManager = eval(f"webdriverManager_browser.{manager_name}")
            plugin_unit = DriverManager().install()
        options = BrowserOptions()
        options.binary = browser_path
        self.driver = Browser(service=Service(plugin_unit), options=options) #启动浏览器
        self.driver.set_window_size(1366, 768)
        self.driver.minimize_window()

    def login(self): #打开网站
        self.driver.get("https://www.jhq8.cn/")

    def search(self, words:str): #找到输入控件 并 输入文字、跳转搜索
        wait = WebDriverWait(self.driver, 10)
        input_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "input"))) #等待元素加载完毕后获取
        button_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button.is-link")))
        input_element.send_keys(words) #输入文字
        button_element.click() #跳转

    def select(self): #选择一个结果、点击跳转
        try: #输入少于2字，弹出Dismissed user prompt dialog
            alert = Alert(self.driver)
            alert.accept() #Dismissed user prompt dialog点击确认
            wait = WebDriverWait(self.driver, 10)
            input_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "input"))) #等待元素加载完毕后获取
            input_element.clear() #清除输入框内的文字
            return (False, "输入文字太短了(≤2)")
        except NoAlertPresentException: #没弹出Dismissed user prompt dialog
            title = self.driver.title
            if title == "404 - 找不到文件或目录。": #搜索未找到
                return (False, "无结果")
            elif title == "500 - 内部服务器错误。": #输入内容异常
                self.login()
                return (False, "输入内容异常（如输入了“|”），请尝试限制识别区域")
            else:
                wait = WebDriverWait(self.driver, 10)
                piece = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lift_remen-list"))) #等待元素加载完毕后获取
                piece = piece.find_element(By.TAG_NAME, "li")
                link = piece.find_element(By.TAG_NAME, "a") #找到第一个搜索结果的链接
                link.click() #打开链接
                all_handles = self.driver.window_handles
                self.driver.switch_to.window(all_handles[-1]) #选择最新跳出来的标签页
                return (True, None)
        
    def grab(self): #找到答案、回退界面、返回结果
        wait = WebDriverWait(self.driver, 10)
        ans_obj = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@style="font-size: 15px;"]'))) #等待元素加载完毕后获取
        text = ans_obj.text #获取文字内容
        all_handles = self.driver.window_handles
        self.driver.close() #关闭答案标签页
        self.driver.switch_to.window(all_handles[0]) #回到搜索标签页
        self.driver.minimize_window() #最小化窗口（针对部分浏览器弹出现象）
        return text

    def get_ans(self, question:str): #搜索集成函数
        self.search(question) #搜索
        res = self.select() #选择答案
        if res[0]:
            ans = self.grab() #获取答案
        else:ans = res[1]
        return ans

if __name__ == "__main__":
    FireFox_PATH = r'D:\Mozilla Firefox\firefox.exe'
    plugin_unit = r"D:\Mozilla Firefox\geckodriver.exe"
    b = Browser("Firefox", FireFox_PATH, plugin_unit)
    b.login()
    print(b.get_ans("按记忆是否受到意识的控制可分为（）|"))
    print(b.get_ans("按"))
    print(b.get_ans("按记忆是否受到意识的控制可分为（）"))
