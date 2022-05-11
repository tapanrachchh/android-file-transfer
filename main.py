
from glob import escape
from re import L
import sys
from tkinter import Widget
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow,QLineEdit,QAction, QApplication, QLabel, QMenu, QMessageBox, QToolBar, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout,QListWidgetItem,QListWidget
from PyQt5.QtGui import QColor, QFont, QIcon, QImage, QPainter, QPen, QPixmap,QPalette
from PyQt5.QtCore import QPoint, QProcess, QRectF, QSize, Qt, pyqtSlot
import os
from os.path import expanduser

#Getting Home Directory to Pull files into it
home = expanduser("~")

#Change it to adb executable path
adb_path="C:/Users/Hp Desk/AppData/Local/Android/Sdk/platform-tools/adb"
adb_path="./tools/win/adb.exe"

def resource_path(relative_path):

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

adb_path=resource_path(adb_path)

# adb_path="C:/Users/Hp Desk/AppData/Local/Android/Sdk/platform-tools/adb"

# LoadingButton Snippet by eyllanesc source:stackoverflow
class LoadingButton(QtWidgets.QPushButton):
    @QtCore.pyqtSlot()
    def start(self):
        if hasattr(self, "_movie"):
            self._movie.start()

    @QtCore.pyqtSlot()
    def stop(self):
        if hasattr(self, "_movie"):
            self._movie.stop()
            self.setIcon(QtGui.QIcon())

    def setGif(self, filename):
        if not hasattr(self, "_movie"):
            self._movie = QtGui.QMovie(self)
            self._movie.setFileName(filename)
            self._movie.frameChanged.connect(self.on_frameChanged)
            if self._movie.loopCount() != -1:
                self._movie.finished.connect(self.start)
        self.stop()

    @QtCore.pyqtSlot(int)
    def on_frameChanged(self, frameNumber):
        self.setIcon(QtGui.QIcon(self._movie.currentPixmap()))


format_dic={"video":["mp4","mov","avi","mkv"],"music":["mp3","ogg","wav"],"doc":["pdf"],"image":["jpg","jpeg","png","gif"]}
color_dic={"video":"darkRed","music":"darkMagenta","doc":"darkGreen","unkown":"darkGray","image":"darkCyan"}




class Custom(QWidget):
    def __init__(self,ext="a"):
        QWidget.__init__(self, parent=None)
        self.type="unkown"
        for e in format_dic.keys():
            if ext in format_dic[e]:
                self.type=e
                break
        if len(ext)>3:
            ext=ext[0:2]+".."
        self.ext=ext

    def paintEvent(self, event):

        
        qp = QPainter()
        qp.begin(self)
        image  = QImage(resource_path('images/exclude.png'))
        # image.setColorCount(2)
        # image.setColor( 0, QtGui.qRgba(255,0,0,255) )
        # image.setColor( 1, QtGui.qRgba(0,0,0,0) )
        path = QtGui.QPainterPath()
        path.addRect((self.frameGeometry().width()/2)-18, 0, 35,45)
        qp.fillPath(path,QColor(color_dic[self.type]))
        # qp.setCompositionMode(QPainter.CompositionMode_Xor)


    
        image = image.scaled(QSize(36,45))
        # for i in range(0,30):
        #     for k in range(0,25):
        #         image.setPixel(i, k, value)

        qp.drawImage(QPoint(int(self.frameGeometry().width()/2)-18,0), image)
        qp.setCompositionMode(QPainter.CompositionMode_SourceOver)

        image  = QImage(resource_path('images/tri.png'))
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




class App(QDialog):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.title = 'ADB File Manager'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.currentPath="/"
        self.initUI()
        self.xc=0
        self.yc=0
        self.num_c=5
        self.drawings=[]


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    
    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.push(files[0])



    def pre_pull(self,btn):
        output = self.p3.readAllStandardOutput()
        y=str(output)
        y=y[2:-1]
        xs = y.split("\\n")
        xs=xs[0:len(xs)-1]
        xs[0]=xs[0].replace("\\r","")
        self.pull(xs[0],btn)


    def onSearchTextChanged(self,text):

        for row in range(self.listWidget.count()):
            it = self.listWidget.item(row)
            widget = self.listWidget.itemWidget(it)
            if text: 
                it.setHidden(not self.filter(text, it.id))
            else:
                it.setHidden(False)

    def filter(self, text, keywords):

        return text in keywords

    def afterRemoval(self,packageId):
        print("Removed",packageId)
        output = bytearray(self.processRemoveApp.readAllStandardOutput())
        print(output)

        print(output)
    def disableApp(self,packageId):
        print("disable this",packageId)
        self.processRemoveApp = QProcess()
        self.processRemoveApp.finished.connect( lambda : self.afterRemoval(packageId))
        self.processRemoveApp.start(adb_path,["shell","pm","disable-user","--user","0",packageId])

    def uninstallApp(self,packageId):
        print("uninstall this",packageId)
        self.processRemoveApp = QProcess()
        self.processRemoveApp.finished.connect( lambda : self.afterRemoval(packageId))
        self.processRemoveApp.start(adb_path,["shell","pm","uninstall ","--user","0",packageId])



    def afterFetch(self):
        print("AFTER FETCH")

        output = bytearray(self.processGetAllPackages.readAllStandardOutput())

        # output = self.processGetAllPackages.readAllStandardOutput()
        output = output.decode("ascii")

        self.sList = output.split("\n")

                
        global window
        window = QWidget()
        self.listWidget = QListWidget()
        window.setWindowTitle("Remove System Apps")
    
        for e in self.sList:


            e=e.replace("package:","")
            horizontalLayout = QHBoxLayout(window)
            l1 = QLabel(e)
            b1 = QPushButton("Disable")
            b1.clicked.connect(lambda checked,txt=e: self.disableApp(txt.strip()))
            b2 = QPushButton("Uninstall")
            b2.clicked.connect(lambda checked,txt=e: self.uninstallApp(txt.strip()))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(1)
            l1.setSizePolicy(sizePolicy)
            horizontalLayout.addWidget(l1)
            horizontalLayout.addWidget(b1)
            horizontalLayout.addWidget(b2)

            wid = QWidget()
            wid.setLayout(horizontalLayout)


            

            temp = QListWidgetItem()

            temp.setSizeHint(wid.sizeHint())

            temp.id = e

            self.listWidget.addItem(temp)
            self.listWidget.setItemWidget(temp,wid)

            # QListWidgetItem(wid,self.listWidget)
    

        
        self.listWidget.itemClicked.connect(self.listWidgetItemClick)

        window_layout = QVBoxLayout(window)

        searchEdit = QLineEdit(self)
        searchEdit.textChanged.connect(self.onSearchTextChanged)


        window_layout.addWidget(searchEdit)

        window_layout.addWidget(self.listWidget)
        window.setLayout(window_layout)
        window.resize(800, 600)

    
        window.show()
        # return window


    def onRemove(self):


        self.processGetAllPackages = QProcess()
        self.processGetAllPackages.finished.connect( lambda : self.afterFetch())
        self.processGetAllPackages.start(adb_path,["shell","pm","list","packages"])



    def listWidgetItemClick(self,item):
        print("CLICKED",item.id)

    def onAbout(self):
        text = "<center>" \
           "<h1> ADB File Manger</h1>" \
           "&#8291;" \
           "</center>" \
           "<p> <center>Version 1.1.0 </center><br/></p>" \
           "<p> <center>LAST UPDATE : Added Color-Cordinated File Icons, Ability to Push Files and Bug fixes </center><br/></p>" \

        QMessageBox.about(self, "About ADB File Manger", text)
        
    def initUI(self):
        
        self.setWindowIcon(QtGui.QIcon(resource_path(resource_path('images/logo.png'))))
        self.setWindowTitle(self.title)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.glayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        # self.setStyleSheet("background-color:white; ")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)


        horizontalLayout = QtWidgets.QHBoxLayout()
        button1 = QtWidgets.QPushButton("Go Back")
        button1.clicked.connect(self.goBack)
        button1.setIcon(QIcon(resource_path('images/back.png')))
        button2 = QtWidgets.QPushButton("SD Card")
        button2.clicked.connect(lambda : self.goto("/sdcard/"))
        button3 = QtWidgets.QPushButton("Download")
        button3.clicked.connect(lambda : self.goto("/sdcard/download/"))
        button4 = QtWidgets.QPushButton("DCIM")
        button4.clicked.connect(lambda : self.goto("/sdcard/DCIM/"))
        button5 = QtWidgets.QPushButton("Remove System Apps")
        button5.clicked.connect(self.onRemove)
        button6 = QtWidgets.QPushButton("About")
        button6.clicked.connect(self.onAbout)


        self.button6 = LoadingButton("PUSH")
        self.button6.clicked.connect(self.onPush)
        self.button6.setIcon(QIcon(resource_path('images/loader.gif')))

        self.button6.setGif(resource_path('images/loader.gif'))
        


        horizontalLayout.addWidget(button1)
        horizontalLayout.addWidget(button2)
        horizontalLayout.addWidget(button3)
        horizontalLayout.addWidget(button4)
        horizontalLayout.addWidget(self.button6)
        horizontalLayout.addWidget(button5)

        wid = QWidget()
        wid.setLayout(horizontalLayout)
        self.layout.addWidget(wid)
        self.layout.addWidget(self.scrollArea)

        self.glayout.setAlignment(QtCore.Qt.AlignTop)


        
        self.getDeviceName()
        self.listOut("/")


        
        self.showMaximized()
        self.show()

    def onPush(self):
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.push(filenames[0])
                



    def goto(self,arg):
        self.listOut(arg)


    def escape(self,string):
        special_characters = '"!@#$%^&*()-+?_=,<>[] '

        escapedString=""
        for e in string:
            if e in special_characters:
                escapedString=escapedString+'\\'+e
            else:
                escapedString=escapedString+e

        escapedString = escapedString.replace("\\r","")
        return escapedString




    def goBack(self):
        path = self.currentPath
        pathArr = path.split("/")
        pathArr2=[]
        for e in pathArr:
            if e:
                pathArr2.append(e)
        temp="/"
        for e in pathArr2[:len(pathArr2)-1]:
            temp=temp+e+"/"
        self.listOut(temp)






    def createFileItem(self,name):


        picLabel = QLabel(self)
        pixmap = QPixmap(resource_path('images/file.png'))
        pixmapScaled = pixmap.scaled(QSize(35,45))


        picLabel.setPixmap(pixmapScaled)
        textLabel = QLabel()
        picLabel.setAlignment(QtCore.Qt.AlignCenter)
        textLabel.setAlignment(QtCore.Qt.AlignCenter)
        textLabel.setText(name)


        button2 = LoadingButton("PULL")
        button2.clicked.connect(lambda : self.gotAbsolutePath(name,button2))
        button2.setGif(resource_path('images/loader.gif'))


        arg="?"
        if "." in name:
            nArr= name.split(".")
            arg=nArr[-1]



        vLayout = QVBoxLayout()
        vLayout.addWidget(Custom(arg))
        vLayout.addWidget(textLabel)
        vLayout.addWidget(button2)

        a = QWidget()
        a.setLayout(vLayout)
        a.setFixedHeight(150)
        return a


    def createFolderItem(self,name):


        picLabel = QLabel(self)
        pixmap = QPixmap(resource_path('images/folder.png'))
        pixmapScaled = pixmap.scaled(QSize(50,50))
        picLabel.setPixmap(pixmapScaled)
        textLabel = QLabel()
        picLabel.setAlignment(QtCore.Qt.AlignCenter)
        textLabel.setAlignment(QtCore.Qt.AlignCenter)


        arr = name.split("/")

        textLabel.setText(arr[-2])
        vLayout = QVBoxLayout()
        vLayout.addWidget(picLabel)
        vLayout.addWidget(textLabel)


        button2 = LoadingButton("PULL")
        button2.clicked.connect(lambda : self.pull(name,button2))
        button2.setGif(resource_path('images/loader.gif'))
        vLayout.addWidget(button2)


        a = QWidget()
        a.setLayout(vLayout)
        a.mousePressEvent =  lambda event:self.listOut(name)

        return a


    def getDeviceName(self):
        self.p0 = QProcess()
        self.p0.finished.connect(self.get_device_name_finished)
        self.p0.errorOccurred.connect(self.onError)
        self.p0.start(adb_path,["devices","-l"])



    def onError(self):
        print("INSTALL ADB OR VERIFY IT'S EXECUTABLE PATH")
        QMessageBox.critical(self, "Error", "INSTALL ADB OR VERIFY IT'S EXECUTABLE PATH")


    def get_device_name_finished(self):
        output = self.p0.readAllStandardOutput()
        y=str(output)
        y=y[2:-1]
        xs = y.split("\\n")
        xs=xs[0:len(xs)-1]
        term="model:"
        term_len=len(term)
        occ = y.find(term)
        if occ==-1:
            print("FOUND")
        else:
            occ=occ+term_len
            space_occ = y[occ:].find(" ")
            space_occ=space_occ+occ
            if y[occ:space_occ]:
                self.setWindowTitle(y[occ:space_occ])


    def listOut(self,name):
        self.p = QProcess()
        self.p.finished.connect(self.list_out_process_finished)
        name=self.escape(name)   
        self.p.start(adb_path,["shell","ls","-d",name+"*/"])
        self.currentPath=name



    def gotAbsolutePath(self,name,btn):
        escaped_name=self.escape(name)
        np=self.currentPath+escaped_name
        self.p3 = QProcess()
        self.p3.finished.connect( lambda : self.pre_pull(btn))
        print("pp",np)
        self.p3.start(adb_path,["shell","ls",np])



    def pre_pull(self,btn):
        output = self.p3.readAllStandardOutput()
        y=str(output)
        y=y[2:-1]
        xs = y.split("\\n")
        xs=xs[0:len(xs)-1]
        xs[0]=xs[0].replace("\\r","")
        self.pull(xs[0],btn)


    def push(self,filePath):
        self.button6.setEnabled(False)
        self.button6.start()
        self.p4 = QProcess()
        self.p4.finished.connect(self.process_finished_push)
        self.p4.start(adb_path,["push",filePath,self.currentPath])


    def pull(self,name,btn):
        btn.setEnabled(False)
        btn.start()
        self.p2 = QProcess()
        self.p2.finished.connect( lambda : self.process_finished_pull(btn))
        name=name.replace("\\r","")
        print("check",name,home)
        self.p2.start(adb_path,["pull",name,home])


    def process_finished_push(self):
        self.button6.setEnabled(True)
        self.button6.stop()
        self.listOut(self.currentPath)

    def process_finished_pull(self,btn):
        output = self.p2.readAllStandardOutput()
        y=str(output)
        print("p2 output",y)
        btn.setText("PULLED")
        btn.stop()


    def process_finished_for_files(self):
        output = self.p1.readAllStandardOutput()
        y=str(output)
        y=y[2:-1]
        xs = y.split("\\n")
        xs=xs[0:len(xs)-1]
        l=len(xs)
        c=0
        x=self.xc
        y=self.yc
        while True:
            while x<self.num_c:
                if c==l:
                    break
                xs[c]=xs[c].replace("\\r","")
                item = self.createFileItem(xs[c])  
                self.glayout.addWidget(item,y,x)
                x=x+1
                c=c+1
            if c==l:
                break           
            if x==self.num_c:
                y=y+1
                x=0

    def list_out_process_finished(self):
        output = self.p.readAllStandardOutput()
        y=str(output)
        y=y[2:-1]
        xs = y.split("\\n")
        xs=xs[0:len(xs)-1]
        l=len(xs)

        for i in reversed(range(self.glayout.count())): 
            self.glayout.itemAt(i).widget().setParent(None)

        c=0
        x=0
        y=0

        while True:
            while x<self.num_c:
                if c==l:
                    self.xc=x
                    break
                item = self.createFolderItem(xs[c])  
                self.glayout.addWidget(item,y,x)
                x=x+1
                c=c+1

            if x==self.num_c:
                y=y+1
                x=0
            if c==l:
                self.yc=y
                self.xc=x
                break  
   
        self.p1 = QProcess()
        self.p1.finished.connect(self.process_finished_for_files)   
        self.p1.start(adb_path,["shell","ls","-p",self.currentPath,"|","grep","-v","/"])
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    ex = App()
    sys.exit(app.exec_())