import os
import json
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as msb
from tkinter import filedialog as fdg
import platform as pl
import ctypes

import tools

PATH = os.getcwd()
DATA_PATH = os.path.join(PATH, "data.json")

def read_file(file_path, json_mode=False): #通用读文件管道
    with open(file_path, "r", encoding="utf-8") as f:
        if json_mode:
            content = json.load(f)
        else: content = f.read()
    return content

def write_file(file_path, content, json_mode=False): #通用写文件管道
    if json_mode:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=True)
    else:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)


class MainWin: #程序主窗
    def __init__(self):
        self.root = Tk()
        self.root.title("超星尔雅学习通查询器")
        self.root.resizable(False,False)
        ScaleFactor = 100
        if not pl.release() == "7":
            ctypes.windll.user32.SetProcessDPIAware()
            ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
            self.root.tk.call('tk', 'scaling', ScaleFactor/75)
        self.SF = ScaleFactor/100
        self.root.geometry("{}x{}".format(int(400*self.SF),int(500*self.SF)))

        self.widget()

    def widget(self): #控件
        font=("宋体",12)
        
        self.Lf1 = LabelFrame(self.root, text="运行记录", labelanchor="nw")
        scrollbar = Scrollbar(self.Lf1)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.Text = Text(self.Lf1, yscrollcommand=scrollbar.set, relief=SUNKEN, state=DISABLED, wrap=WORD, font=font) #运行展示框
        self.Text.pack(fill=BOTH, padx=(20,30), pady=(10,15))
        scrollbar.config(command=self.Text.yview)
        self.Lf1.pack(fill=X, padx=(13,13), pady=(0,10))

        self.Lf2 = LabelFrame(self.root, text="操作", labelanchor="nw")
        self.Bt1 = Button(self.Lf2, text="初 始 化", command=self.browser_init)
        self.Bt1.grid(row=0, column=0, padx=(30,5), pady=(0,5), ipady=10)
        self.Bt2 = Button(self.Lf2, text="开始查询", command=self.start, state=DISABLED)
        self.Bt2.grid(row=0, column=1, padx=(5,40), pady=(0,5), ipady=10)
        self.Bt3 = Button(self.Lf2, text="清空记录", command=self.clear)
        self.Bt3.grid(row=0, column=2, padx=(40,30), pady=(0,5), ipady=10)
        self.Lf2.pack(fill=X, padx=(13,13), pady=(0,20))

        self.mainmenu = Menu(self.root)
        self.menuFile = Menu(self.mainmenu,tearoff=0)
        self.mainmenu.add_cascade(label='Selenium', menu=self.menuFile)
        self.menuFile.add_cascade(label='配置参数', command=set_browser)
        self.root.config(menu=self.mainmenu)

    def insert(self, text:str, end="\n"): #向运行展示框加入文字
        self.Text.config(state=NORMAL)
        self.Text.insert(END, text+end)
        self.Text.config(state=DISABLED)
        self.Text.see(END)
        self.root.update()

    def clear(self): #清空运行展示框
        self.Text.config(state=NORMAL)
        self.Text.delete(1.0, END)
        self.Text.config(state=DISABLED)
        self.root.update()

    def browser_init(self): #初始化selenium
        self.insert("[selenium] init start...",end="")
        self.core = tools.Tools(data_path=DATA_PATH)
        self.Bt1.config(state=DISABLED)
        self.Bt2.config(state=NORMAL)
        self.insert("done")
        
    def start(self): #开始搜索答案
        strings = self.core.get_strings()
        if len(strings) == 0: #没在屏幕内匹配到基准图标，即没找到题目
            self.insert("[  INFO  ] NO tartget on your screen.")
        else:
            n = len(strings); count = 0
            self.insert(f"[  INFO  ] find {n} target(s) on your screen!")
            gen = self.core.get_ans(strings)
            for one in gen:
                count += 1
                self.insert(one, end=f"\n----↑[{n}/{count}]↑----\n")

    def run(self):
        self.root.mainloop()

class SetWin: #Selenium配置窗口
    def __init__(self, creat=False):
        self.creat = creat #表示是否初次设置数据
        self.root = Tk()
        self.root.title("Selenium配置")
        self.root.resizable(False,False)
        ScaleFactor = 100
        if not pl.release() == "7":
            ctypes.windll.user32.SetProcessDPIAware()
            ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
            self.root.tk.call('tk', 'scaling', ScaleFactor/75)
        self.SF = ScaleFactor/100
        self.root.geometry("{}x{}".format(int(600*self.SF),int(250*self.SF)))
        
        self.browserOptions = ["Edge", "Chrome", "Firefox"] #浏览器选项
        
        self.browserOption = StringVar(master=self.root)
        self.browserPath = StringVar(master=self.root)
        self.pluginunitPath = StringVar(master=self.root)
        self.pluginunitAutoMode = BooleanVar(master=self.root)
        self.info = StringVar(master=self.root)

        if os.path.isfile(DATA_PATH): #如已有数据
            dic = read_file(DATA_PATH, json_mode=True) #读取数据
            browser_chose = self.browserOptions.index(dic["browser"]) #展示出来
            self.browserPath.set(dic["browser_path"])
            plugin_unit = dic["plugin_unit"]
            if plugin_unit is not None: #有指定浏览器插件
                self.pluginunitPath.set(plugin_unit)
            else: #没指定浏览器插件，即勾选了自动选择
                self.pluginunitAutoMode.set(True)

        self.style_gray = Style()
        self.style_gray.layout("gray.TEntry") #灰色字体
        self.style_gray.configure("gray.TEntry", foreground="gray")
        
        self.style_black = Style()
        self.style_black.layout("black.TEntry") #黑泽字体
        self.style_black.configure("black.TEntry", foreground="black")
        
        self.widget(browser_chose)

    def widget(self, browser_chose=0): #browser_chose:浏览器选项卡默认选项
        font=("宋体",11)
        self.Lf1 = LabelFrame(self.root, text="浏览器配置", labelanchor="nw")
        
        Label(self.Lf1, text="选择浏览器", font=font).grid(row=0, column=0, ipadx=10, padx=(10,0), pady=(0,10))
        comboxlist = Combobox(self.Lf1, textvariable=self.browserOption, width=5) #选项卡
        comboxlist["values"] = self.browserOptions
        comboxlist.current(browser_chose) #设置默认选项
        comboxlist.grid(row=0, column=1, ipadx=10, padx=(0,20), pady=(0,10))
        Label(self.Lf1, text="选择浏览器路径", font=font).grid(row=0, column=2, ipadx=10, padx=(20,0), pady=(0,10))
        self.Et1 = Entry(self.Lf1, textvariable=self.browserPath, width=21, font=font, state="readonly")
        self.Et1.grid(row=0, column=3, padx=(10,10), pady=(0,10))
        self.Bt1 = Button(self.Lf1, text="选择", command=self.__choose_browser)
        self.Bt1.grid(row=0, column=4, pady=(0,10))
        self.Lf1.pack(fill=X, padx=(13,13), pady=(15,15))
        
        self.Lf2 = LabelFrame(self.root, text="浏览器插件配置", labelanchor="nw")
        Checkbutton(self.Lf2, text='自动匹配浏览器插件', variable=self.pluginunitAutoMode,\
                    onvalue=True, offvalue=False, command=self.__pluginunitAuto_choose)\
                    .grid(row=0, column=0, padx=(10,10), pady=(0,10))
        Label(self.Lf2, text="选择插件路径", font=font).grid(row=0, column=1, ipadx=10, padx=(85,0), pady=(0,10))
        self.Et2 = Entry(self.Lf2, textvariable=self.pluginunitPath, width=21, font=font, state="readonly")
        self.Et2.grid(row=0, column=3, padx=(25,10), pady=(0,10))
        self.Bt2 = Button(self.Lf2, text="选择", command=self.__choose_pluginunit)
        self.Bt2.grid(row=0, column=4, pady=(0,10))
        self.Lf2.pack(fill=X, padx=(13,13), pady=(15,20))

        self.Bt3 = Button(self.root, text="确定", command=self.__yesBt)
        self.Bt3.pack(fill=X, padx=(200,200), pady=(20,20))

        Label(self.root, textvariable=self.info, font=font).pack(fill=X, padx=(50,50)) #提示词展示

    def __choose_file(self, text): #文件选择框
        filetypes = (("Executable Files", "*.exe"),)
        path = fdg.askopenfilename(title=text, filetypes=filetypes, parent=self.root)
        return path

    def __choose_browser(self): #选浏览器程序
        path = self.__choose_file("选择浏览器")
        self.browserPath.set(path)
        self.root.update()

    def __choose_pluginunit(self): #选浏览器插件
        path = self.__choose_file("选择浏览器插件")
        self.pluginunitPath.set(path)
        self.root.update()

    def __pluginunitAuto_choose(self): #勾选框（自动选择浏览器插件）事件
        choose = self.pluginunitAutoMode.get()
        if choose: #勾选了，提示
            self.Bt2.config(state=DISABLED) #禁用选择浏览器插件位置
            self.Et2.config(state=DISABLED)
            self.Et2.config(style="gray.TEntry")
            self.info.set("info: 该模式需要联网访问github.com，可能连接不稳定")
            self.root.update()
        else: #未勾选
            self.Bt2.config(state=NORMAL) #启用选择浏览器插件位置
            self.Et2.config(state="readonly")
            self.Et2.config(style="black.TEntry")
            self.info.set("")

    def __yesBt(self): #确认按钮事件
        flag = True #表示数据完整情况
        browser = self.browserOption.get()
        browser_path = self.browserPath.get()
        if "" in [browser, browser_path]: #浏览器\浏览器路径存在缺失
            flag = False
        pluginunitAutoMode = self.pluginunitAutoMode.get()
        if not pluginunitAutoMode: #未选择自动匹配浏览器插件
            pluginunitPath = self.pluginunitPath.get()
            if pluginunitPath is None: #浏览器插件路径缺失
                flag = False
        else: pluginunitPath = None
        if flag:
            self.__output(browser, browser_path, pluginunitPath) #写入文件
        else: self.__err("输入错误", "数据缺失")
            
    def __err(self, title, message):
        msb.showerror(title=title, message=message)

    def __output(self, browser:str, browser_path:str, plugin_unit):
        dic = {"browser":browser, "browser_path":browser_path, "plugin_unit":plugin_unit}
        write_file(DATA_PATH, dic, True)
        if not self.creat: #不是首次设置，即在程序运行中设置
            msb.showinfo(title="提示", message="程序需要重启以应用更改")
        self.root.destroy()

    def run(self):
        self.root.mainloop()

def set_browser(): #按钮事件：启动浏览器配置窗口
    setwin = SetWin()
    setwin.run()

if __name__ == "__main__":
    if not os.path.isfile(DATA_PATH): #不存在数据文件，则先设置
        setwin = SetWin(creat=True)
        setwin.run()
    mainwin = MainWin()
    mainwin.run()

    
    
    
    
