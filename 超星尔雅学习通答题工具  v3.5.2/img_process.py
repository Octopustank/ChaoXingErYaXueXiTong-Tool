import cv2
import aircv as ac
from PIL import Image
import numpy as np
import os
import pytesseract
import json

class Cropper:
    def __init__(self, data_path=None):
        if data_path is not None: #指定了数据路径，使用其中指定的tesseract路径
            with open(data_path, "r", encoding="utf-8") as f:
                dic = json.load(f)
            pytesseract.pytesseract.tesseract_cmd = dic["TesseractOCR_path"]
        self.path = os.getcwd()
        self.res_path = os.path.join(self.path, 'res')
        benchmarkFloders = next(os.walk(self.res_path))[1]
        benchmarkFloders.sort(reverse=True) #从大图文件夹到小图文件夹排
        benchmarkFloders = list(map(lambda x: os.path.join(self.res_path, x), benchmarkFloders))
        self.BENCHMARKS = []
        print(benchmarkFloders)
        for folder in benchmarkFloders:
            files = next(os.walk(folder))[2]
            self.BENCHMARKS.append([])
            for one in files: #读取该目录下的基准图标
                one = os.path.join(folder, one)
                one = cv2.cvtColor(np.asarray(Image.open(one)), cv2.COLOR_RGB2BGR)
                self.BENCHMARKS[-1].append(one)

    def __locate(self, img_cv2): #对图像中的基准进行定位
        global aa
        res = []; temp = []; max_ = -1
        for group in self.BENCHMARKS:
            for one in group:
                loc = ac.find_all_template(img_cv2, one, 0.9) #识别
                temp += loc
            l = len(temp)
            print("|" + "-"*l + "|")
            if l > max_: #如果该组 识别结果更多，取该组
                max_ = l
                res = temp.copy()
            elif l < max_: #如果该组 识别结果少了
                break #终止遍历
            temp = [] #初始化temp

        res = list(map(lambda x:x["rectangle"], res)) #取四角
        res = list(map(lambda x:(x[2], x[3]), res)) #取右上和右下的点
        l = len(res)
        for i in range(l-1): #冒泡排序
            flag = False
            for j in range(0,l-i-1):
                if res[j][0][1] > res[j+1][0][1]:
                    res[j], res[j+1] = res[j+1], res[j]
                    flag = True
            if not flag:
                break
        return res

    def __crop(self, img_pil, top_left:tuple, bottom_left:tuple): #裁切图像得到题目
        width = img_pil.size[0]
        left = top_left[0]
        top = top_left[1]
        right = width #一直切到最右边
        bottom = bottom_left[1]
        cropped_image = img_pil.crop((left, top, right, bottom)) #裁切
        return cropped_image

    def process(self, img_pil): #全过程总函数
        img_cv2 = cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR) #转PIL对象为cv2
        lst = self.__locate(img_cv2) #定位
        ans = []
        for one in lst: #依次裁切得题目
            cropped_image = self.__crop(img_pil, one[0], one[1])
            ans.append(cropped_image)
        return ans

def ocr(img_lst:list): #批量文字识别
    ans = []
    for one in img_lst:
        res = pytesseract.image_to_string(one, lang="eng+chi_sim")
        res = res.replace(" ", "") #替换英文字符为中文
        res = res.replace("\n", "").replace("|", "")
        res = res.replace("?", "？").replace("!", "！")
        res = res.replace("(", "（").replace(")", "）")
        res = res.replace(",", "，").replace(";", "；")
        tag = 0; icon = ["“", "”"]
        while res.find('"') != -1: #交替使用”“
            res = res.replace('"', icon[tag])
            tag = 1-tag
        ans.append(res)
    return ans

if __name__ == "__main__":
    cropper = Cropper()
    material = Image.open(".\\material.png")
    pieces = cropper.process(material)
    print(pieces)
##    for one in pieces:
##        one.show()
    strings = ocr(pieces)
    print("\n".join(strings))
