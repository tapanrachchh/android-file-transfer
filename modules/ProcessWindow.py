from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QLabel, QVBoxLayout, QWidget,QPushButton
import weakref
from modules.helper import resource_path



class ProcessWindow(QWidget):
    instances = []
    def __init__(self,processText="Processing...",processType="GENERAL"):
        QWidget.__init__(self)
        self.__class__.instances.append(weakref.proxy(self))

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.resize(800, 300)
        # self.setWindowTitle("File Transfer")



        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addStretch()

        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)


        if len(processText)>20:
            processText=processText[0:17]+"..."

        self.label2 = QtWidgets.QLabel(processText)
        self.label2.setGeometry(QtCore.QRect(95, 0, 800, 300))

        self.label2.setStyleSheet(''' font-size: 24px; ''')
        self.label2.setAlignment(Qt.AlignCenter)


        layout.addWidget(self.label2)


        layout.addStretch()

        if processType=="GENERAL":
            image = resource_path("images/process_general.gif")

        elif processType=="FILE_TRANSFER":
            image = resource_path("images/process_file_transfer.gif")



        self.movie = QMovie(image)
        self.label.setMovie(self.movie)
        self.movie.start()        

        self.setLayout(layout)
