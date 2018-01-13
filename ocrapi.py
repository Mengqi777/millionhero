import os
import base64,json
import urllib.request as request
import urllib.parse as parse
from PIL import Image


class ImageProgress(object):
    def __init__(self):
        pass

    def screenFromPhone(self):
        os.system(r'adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        return os.system(r'adb pull /sdcard/screenshot.png screenshot.png')


    def cutImg(self):
        if(self.screenFromPhone()==0):
            # 加载原始图片
            img = Image.open("screenshot.png")
            size=img.size
            # 从左上角开始 剪切 200*200的图片
            cs=self.getCutSize(size[1])
            img2 = img.crop((0, cs[0], size[0], cs[1]))
            img2.save("save.png")

    def getCutSize(self,height):
        s=[]
        s.append(height*0.25)
        s.append(height*0.45)
        return s

class OCRApiDemo(object):
    def __init__(self,imgPath):
        self.imagePath=imgPath
        self.searchUrl=r'http://www.baidu.com/s?wd='
        self.host = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=24.6ed815fe0b82847e2cf8da4d8ae2af7c.2592000.1518408420.282335-10680156'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def getImgBase64Data(self):
        with open(self.imagePath, "rb") as f:
            # b64encode是编码，b64decode是解码
            return base64.b64encode(f.read())
            # base64.b64decode(base64data)

    def getUrlencodeData(self):
        values={
            'image':self.getImgBase64Data()
        }
        return parse.urlencode(values).encode(encoding='UTF8')

    def getOCRData(self):
        req = request.Request(self.host, data=self.getUrlencodeData(), headers=self.headers)
        response = request.urlopen(req)
        return json.loads(response.read().decode('utf-8'))

    def parseWordsResult(self):
        data = self.getOCRData()

        wr = data['words_result']
        keyWord = ''
        for w in wr:
            keyWord += w['words']
        return keyWord

    def getBaiduResult(self):
        kw=self.parseWordsResult()
        os.system('start "C:\Program Files (x86)\Internet Explorer\iexplore.exe" https://www.baidu.com/s?wd='+kw)
        return kw

if __name__ == '__main__':
    ip=ImageProgress()
    ip.cutImg()
    oad=OCRApiDemo('save.png')
    oad.getBaiduResult()