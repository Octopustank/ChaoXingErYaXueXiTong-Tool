# ChaoXingErYaXueXiTong-Tool
Python超星尔雅学习通小工具-答题助手

## 功能 Features
 - 截图与OCR文字识别获取题目
 - Selenium访问精华吧(https://m.jhq8.cn/)获取答案并展示

## 更新 What's New
v1.1.0
 - 支持设置浏览器、浏览器插件
v2.0.0
 - 全UI支持

## 使用 Use
v1.1.0
 - 在`main.py`中指定好浏览器、插件安装位置(不指定默认使用自动模式)
 - 启动`main.py`后等待Selenium启动
 - 保证显示有要搜索答案的题目的网页中，题目部分靠屏幕右侧且题目文字的右侧没有其他文字显示（即把浏览器右边界靠屏幕右边界），同时把`main.py`的命令行窗口放到屏幕左侧，输入回车，就会马上截图，并进行搜索、展示出

## 注意 Attention
 - 搜索答案时，因精华吧限制，每4s搜一次
 - 题目文字不应太小，否则OCR不能识别
 - 遇到没查到答案的情况，会在结果中显示None

## 库需求 Package Requirements
未更新...


