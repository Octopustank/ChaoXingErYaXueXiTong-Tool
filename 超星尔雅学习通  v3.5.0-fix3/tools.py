import os
from re import A
import pyautogui as pg
import time as tm

import web_grab, img_process


class Tools:
    def __init__(self, browser=None, browser_path=None, plugin_unit=None, data_path=None):
        self.browser = web_grab.Browser(browser, browser_path, plugin_unit, data_path)
        self.cropper = img_process.Cropper(data_path)
        self.path = os.getcwd()
##        self.log_path = os.path.join(self.path, "log.txt")
        self.browser.login()

    def get_strings(self): #截屏、裁剪、识别得到题目
        img = pg.screenshot() #调用pyautogui截图
        pieces = self.cropper.process(img) #裁剪图片
        strings = img_process.ocr(pieces) #ocr文字识别
        return strings

    def get_ans(self, strings:list): #生成器，用于依次出答案
        ans = None; l = len(strings)
        p = 0
        while p < l:
            ans = self.browser.get_ans(strings[p]) #获取答案
            yield ans
            p += 1
            if p < l:
                tm.sleep(3) #精华吧网站限制3s搜索一次


if __name__ == "__main__":
    BROWSER = "Firefox"
    BROWSER_PATH = r'D:\Mozilla Firefox\firefox.exe'
    PLUGIN_UNIT = r"D:\Mozilla Firefox\geckodriver.exe"
    tool = Tools(BROWSER, BROWSER_PATH, PLUGIN_UNIT)
    while 1:
        input("start?")
        strings = tool.get_strings()
        gen = tool.get_ans(strings)
        for one in gen:
            print(one)
        

