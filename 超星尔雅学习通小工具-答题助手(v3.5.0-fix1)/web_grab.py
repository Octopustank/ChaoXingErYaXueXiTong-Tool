from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            webdriverManager_browser = ipt.import_module(f"webdriver_manager.{browser.lower()}")
            GeckoDriverManager = webdriverManager_browser.GeckoDriverManager
            plugin_unit = GeckoDriverManager().install()
        options = BrowserOptions()
        options.binary = browser_path
        self.driver = Browser(service=Service(plugin_unit), options=options) #启动浏览器

    def login(self): #打开网站
        self.driver.get("https://www.jhq8.cn/")

    def search(self, words:str): #找到输入控件 并 输入文字、跳转搜索
        wait = WebDriverWait(self.driver, 10)
        input_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "input"))) #等待元素加载完毕后获取
        button_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button.is-link")))
        input_element.send_keys(words) #输入文字
        button_element.click() #跳转

    def select(self): #选择一个结果、点击跳转
        if "404" in self.driver.title: #搜索未找到
            return None
        else:
            wait = WebDriverWait(self.driver, 10)
            piece = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "lift_remen-list"))) #等待元素加载完毕后获取
            piece = piece.find_element(By.TAG_NAME, "li")
            link = piece.find_element(By.TAG_NAME, "a") #找到第一个搜索结果的链接
            link.click() #打开链接
            all_handles = self.driver.window_handles
            self.driver.switch_to.window(all_handles[-1]) #选择最新跳出来的标签页
            return True
        
    def grab(self): #找到答案、回退界面、返回结果
        wait = WebDriverWait(self.driver, 10)
        ans_obj = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@style="font-size: 15px;"]'))) #等待元素加载完毕后获取
        text = ans_obj.text #获取文字内容
        all_handles = self.driver.window_handles
        self.driver.close() #关闭答案标签页
        self.driver.switch_to.window(all_handles[0]) #回到搜索标签页
        return text

    def get_ans(self, question:str): #搜索集成函数
        self.search(question) #搜索
        res = self.select() #选择答案
        if res is not None:
            ans = self.grab() #获取答案
        else:ans = None
        return ans

if __name__ == "__main__":
    FireFox_PATH = r'D:\Mozilla Firefox\firefox.exe'
    plugin_unit = r"D:\Mozilla Firefox\geckodriver.exe"
    b = Browser("Firefox", FireFox_PATH, plugin_unit)
    b.login()
    print(b.get_ans("按记忆是否受到意识的控制可分为（）"))
