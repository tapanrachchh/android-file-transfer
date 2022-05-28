
import modules.helper as helper
from PyQt5 import QtGui
from PyQt5.QtWidgets import  QWidget
from PyQt5.QtGui import QColor, QPainter, QPen,QImage,QFont
from PyQt5.QtCore import QPoint, QRectF, QSize, Qt
from modules.helper import resource_path

class CustomFileWidget(QWidget):
    def __init__(self,theme_type,ext="a"):
        QWidget.__init__(self, parent=None)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.type="unkown"
        self.theme_type=theme_type
        for e in helper.format_dic.keys():
            if ext in helper.format_dic[e]:
                self.type=e
                break
        if len(ext)>3:
            ext=ext[0:2]+".."
        self.ext=ext





    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.theme_type=="Dark":
            image  = QImage(resource_path('images/exclude.png'))
        else:
            image  = QImage(resource_path('images/exclude-white.png'))
        path = QtGui.QPainterPath()
        path.addRect((self.frameGeometry().width()/2)-18, 0, 35,45)
        qp.fillPath(path,QColor(helper.color_dic[self.type]))

        image = image.scaled(QSize(36,45))



        qp.drawImage(QPoint(int(self.frameGeometry().width()/2)-18,0), image)
        qp.setCompositionMode(QPainter.CompositionMode_SourceOver)

        image  = QImage(resource_path('images/peak.png'))
        image = image.scaled(QSize(36,45))
        qp.drawImage(QPoint(int(self.frameGeometry().width()/2)-18,0), image)


        pen = QPen(Qt.white)
        pen.setWidth(2)
        qp.setPen(pen)        
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        qp.setFont(font)
        qp.drawText(QRectF(0.0,0.0,self.frameGeometry().width(),50.0), Qt.AlignCenter|Qt.AlignTop, self.ext)
        qp.end()



