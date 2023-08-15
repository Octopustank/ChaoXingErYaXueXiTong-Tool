# ChaoXingErYaXueXiTong-Tool
Python超星尔雅学习通小工具-答题助手

# 公告 Notice
如果你在2023年8月15日上午11时前下载了任意版本，其中包含一个bug可能导致问题。你可以重新下载修复后的新文件。
If you downloaded any version before 11:00 AM on August 15, 2023, there might be a bug that could cause issues. You can download the fixed file again.

## 功能 Features
 - 截图与OCR文字识别获取题目
 - Selenium访问精华吧(https://m.jhq8.cn/) 获取答案并展示

## 更新 What's New
https://github.com/Octopustank/ChaoXingErYaXueXiTong-Tool/releases

## 使用 Use
### ≤ v1.1.0
 - 在`main.py`中指定好浏览器、插件安装位置(不指定默认使用自动模式)
 - 启动`main.py`后等待Selenium启动
 - 保证显示有要搜索答案的题目的网页中，题目部分靠屏幕右侧且题目文字的右侧没有其他文字显示（即把浏览器右边界靠屏幕右边界），同时把`main.py`的命令行窗口放到屏幕左侧，输入回车，就会马上截图，并进行搜索、展示出来

### ≥ v3.0.0
 - 启动main.pyw，按指示操作即可

## 注意 Attention
 - 搜索答案时，因精华吧限制，每4s搜一次
 - 题目文字不应太小，否则OCR不能识别
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
 - Tesseract on Windows: https://digi.bib.uni-mannheim.de/tesseract/
#### 安装时需要You Need To Do When Installing:
 - 勾选语言包`chi-sm` - Need language package `chi-sm`


