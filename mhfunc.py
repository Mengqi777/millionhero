import millonhero,sys,os
from PyQt5.QtWidgets import (QApplication,QMainWindow,QGraphicsScene,QGraphicsPixmapItem)
from PyQt5.QtGui import QPixmap
import ocrapi

class mhapp(QMainWindow,millonhero.Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.doSearch)


    def doSearch(self):
        ip = ocrapi.ImageProgress()
        ip.cutImg()
        scene = QGraphicsScene(self)
        pixmap = QPixmap("save.png")
        item = QGraphicsPixmapItem(pixmap)
        scene.addItem(item)
        self.graphicsView.scale(1, 1)
        self.graphicsView.setScene(scene)
        oad = ocrapi.OCRApiDemo('save.png')
        self.textBrowser.setText(oad.getBaiduResult())




def main():

    pp=os.popen('adb devices')
    devices=pp.read().split("\n")[1:]
    if(devices[0]==''):
        os.system('msg %username% /w /v 设备未正常连接')
        return
    if(devices[0].split('\t')[1] != 'device'):
        os.system('msg %username% /w /v '+devices[0].split('\t')[1])
        return
    if(devices[0].split('\t')[1] == 'device'):
        '''主函数'''
        app=QApplication(sys.argv)
        win=mhapp()
        win.show()
        sys.exit(app.exec_())
    else:
        os.system('msg %username% /w /v 发生了不可描述的错误')
if __name__=="__main__":
    main()