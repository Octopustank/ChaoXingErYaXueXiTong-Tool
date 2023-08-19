# ChaoXingErYaXueXiTong-Tool
Python超星尔雅学习通小工具-答题助手

## 声明 Statement 
#### 本程序提供的答案仅供参考，不保证准确性和有效性。使用者应自行承担答案的后果和责任，作者不承担任何责任。使用本程序即表示您同意此声明。
#### The answers provided by this program are for reference only and are not guaranteed to be accurate or effective. Users are responsible for the consequences and liabilities of using the answers, and the author assumes no responsibility. By using this program, you agree to this disclaimer.

## 功能 Features
 - 缘于超星尔雅学习通网站答题文字内容编码未知、难以爬取，故选取【获取截图与OCR文字识别获取题目】的方式
 - Selenium访问精华吧(https://m.jhq8.cn/) 获取答案并展示

## 更新 What's New
https://github.com/Octopustank/ChaoXingErYaXueXiTong-Tool/releases

## 使用 Use
安装好浏览器驱动（也可以选择不安装），安装好Tesseract OCR  
（见下方【库需求】）
### ≤ v1.1.0
 - 在`main.py`中指定好浏览器、插件安装位置(不指定默认使用自动模式)
 - 启动`main.py`后等待Selenium启动
 - 保证显示有要搜索答案的题目的网页中，题目部分靠屏幕右侧且题目文字的右侧没有其他文字显示（即把浏览器右边界靠屏幕右边界），同时把`main.py`的命令行窗口放到屏幕左侧，输入回车，就会马上截图，并进行搜索、展示出来

### ≥ v3.0.0
 - 启动main.pyw，按指示操作即可

### exe文件
https://github.com/Octopustank/ChaoXingErYaXueXiTong-Tool/releases/tag/v3.5.2-Packed
 - 确保文件夹内有完整res目录，打开exe即可

## 注意 Attention
 - 搜索答案时，因精华吧限制，每4s搜一次
 - 题目文字不应太小，否则OCR不能识别
 - 题目没被捕获时，可以尝试更改浏览器缩放
 - 适当使用屏幕右边框”裁剪“题目至合适长度
 - 遇到没查到答案的情况，会在结果中显示None

## 库需求 Package Requirements
`pip install aircv opencv-python Pillow PyAutoGUI selenium webdriver-manager pytesseract`  
### 浏览器驱动 - browser plug-in unit：
 - Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
 - Chrome：http://chromedriver.storage.googleapis.com/index.html
 - Chrome(a mirror in China)：https://registry.npmmirror.com/binary.html?path=chromedriver/
 - Firefox：https://github.com/mozilla/geckodriver
### pytesseract所需 - pytesseract Requiry
 - Tesseract OCR: https://github.com/tesseract-ocr/tesseract
 - Tesseract for Windows: https://digi.bib.uni-mannheim.de/tesseract/
#### 安装时需要You Need To Do When Installing:
 - 安装时勾选语言包`chi-sm` - Need language package `chi-sm`


