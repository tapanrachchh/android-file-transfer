
from glob import escape
import os
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow,QLineEdit, QApplication, QLabel, QMessageBox, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,QListWidgetItem,QListWidget
from PyQt5.QtGui import QColor,  QIcon, QPixmap,QPalette
from PyQt5.QtCore import  QProcess, QSize, Qt
import darkdetect
from modules.ProcessWindow import ProcessWindow
from modules.helper import resource_path
import modules.helper as helper
from modules.CustomDraggableWidget import CustomDraggableWidget
from modules.CustomFileWidget import CustomFileWidget


class App(QMainWindow):

    def __init__(self,theme_type):
        super().__init__()
        self.setAcceptDrops(True)
        self.theme_type=theme_type
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
        

    def closeEvent(self, event):
        for instance in ProcessWindow.instances:
            try:
                instance.close()
            except:
                print("Exception while closing instace")

    def dragEnterEvent(self, event):
        if not event.source():
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()
        else:
            return


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
        self.searchEdit.setText("")

        print(output)
    def disableApp(self,packageId):
        print("disable this",packageId)
        self.processRemoveApp = QProcess()
        self.processRemoveApp.finished.connect( lambda : self.afterRemoval(packageId))
        self.processRemoveApp.start(helper.adb_path,["shell","pm","disable-user","--user","0",packageId])

    def uninstallApp(self,packageId):
        print("uninstall this",packageId)
        self.processRemoveApp = QProcess()
        self.processRemoveApp.finished.connect( lambda : self.afterRemoval(packageId))
        self.processRemoveApp.start(helper.adb_path,["shell","pm","uninstall ","--user","0",packageId])



    def afterFetch(self):
        print("AFTER FETCH")

        output = bytearray(self.processGetAllPackages.readAllStandardOutput())
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

        self.searchEdit = QLineEdit(self)
        self.searchEdit.textChanged.connect(self.onSearchTextChanged)


        window_layout.addWidget(self.searchEdit)

        window_layout.addWidget(self.listWidget)
        window.setLayout(window_layout)
        window.resize(800, 600)

    
        window.show()
        # return window


    def onRemove(self):


        self.processGetAllPackages = QProcess()
        self.processGetAllPackages.finished.connect( lambda : self.afterFetch())
        self.processGetAllPackages.start(helper.adb_path,["shell","pm","list","packages"])



    def listWidgetItemClick(self,item):
        print("CLICKED",item.id)


    def showProcess(self,processText):

        process_window = ProcessWindow(processText,processType="GENERAL")
        process_window.show()

        return process_window


    def hideProcess(self,process_window):
        process_window.close()

    def onAbout(self,processText="Transfering File..."):

        text = "<center>" \
           "<h1> ADB File Manager</h1>" \
           "&#8291;" \
           "</center>" \
           "<p> <center>Version 1.2.0 </center><br/></p>" \
           "<p> <center> Android file transfer using Adb </center><br/></p>" \
            "<p> <center>NOTE: Make sure you enable adb debugging on your device.</center><br/></p>" \


        QMessageBox.about(self, "About - ADB File Manger", text)


        
    def initUI(self):
        
        self.setWindowIcon(QtGui.QIcon(resource_path(resource_path('images/logo.png'))))
        self.setWindowTitle(self.title)



        self.layout = QtWidgets.QVBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.glayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        horizontalLayout = QtWidgets.QHBoxLayout()
        button1 = QtWidgets.QPushButton("Go Back")
        button1.clicked.connect(self.goBack)
        if self.theme_type=="Dark":
            button1.setIcon(QIcon(resource_path('images/back-white.png')))
        else:
            button1.setIcon(QIcon(resource_path('images/back.png')))
        button2 = QtWidgets.QPushButton("SD Card")
        button2.clicked.connect(lambda : self.goto("/sdcard/"))
        button3 = QtWidgets.QPushButton("Download")
        button3.clicked.connect(lambda : self.goto("/sdcard/download/"))
        button4 = QtWidgets.QPushButton("DCIM")
        button4.clicked.connect(lambda : self.goto("/sdcard/DCIM/"))
        button5 = QtWidgets.QPushButton("Remove System Apps")
        button5.clicked.connect(self.onRemove)
        aboutButton = QtWidgets.QPushButton("About")
        aboutButton.clicked.connect(self.onAbout)

        


        horizontalLayout.addWidget(button1)
        horizontalLayout.addWidget(button2)
        horizontalLayout.addWidget(button3)
        horizontalLayout.addWidget(button4)
        horizontalLayout.addWidget(button5)

        horizontalLayout.addWidget(aboutButton)

        wid = QWidget()
        wid.setLayout(horizontalLayout)
        self.layout.addWidget(wid)
        self.layout.addWidget(self.scrollArea)

        self.glayout.setAlignment(QtCore.Qt.AlignTop)


        
        self.getDeviceName()
        self.listOut("/")



        widgetcheck = QWidget()
        widgetcheck.setLayout(self.layout)
        self.setCentralWidget(widgetcheck)


        
        self.showMaximized()
        self.show()



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



        escaped_name=self.escape(name)
        np=self.currentPath+escaped_name
        textLabel = QLabel()
        dWid = CustomDraggableWidget(np)
        draggbleVLayout = QVBoxLayout()  

        

        
        textLabel.setAlignment(QtCore.Qt.AlignCenter)
        textLabel.setText(name)



        arg="?"
        if "." in name:
            nArr= name.split(".")
            arg=nArr[-1]




        vLayout = QVBoxLayout()

        draggbleVLayout.addWidget(CustomFileWidget(self.theme_type,arg))
        draggbleVLayout.addWidget(textLabel)
        dWid.setLayout(draggbleVLayout)
        # vLayout.addWidget(Custom(arg))
        # vLayout2 = QVBoxLayout()
        vLayout.addWidget(dWid)
        # vLayout.addWidget(button2)

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

        # picLabel.setContentsMargins(100, -1, -1, 0)

        textLabel.setText(arr[-2])
        vLayout = QVBoxLayout()
        vLayout.addWidget(picLabel)

        vLayout.addWidget(textLabel)
        vLayout.setSpacing(0)
        vLayout.setContentsMargins(0,0,0,20)








        dWid = CustomDraggableWidget(name,func=self.listOut)



        # vLayout.addWidget(button2)




        dWid.setLayout(vLayout)

        # dWid.mousePressEvent =  lambda event:self.listOut(name)

        # return a
        return dWid


    def getDeviceName(self):
        process_window = self.showProcess("Getting Device Name")

        self.p0 = QProcess()
        self.p0.finished.connect(lambda :  self.on_found_device(process_window))
        self.p0.errorOccurred.connect(self.onError)
        self.p0.start(helper.adb_path,["devices","-l"])



    def onError(self):
        print("INSTALL ADB OR VERIFY IT'S EXECUTABLE PATH")
        QMessageBox.critical(self, "Error", "INSTALL ADB OR VERIFY IT'S EXECUTABLE PATH")



    def on_found_device(self,process_window):
        output = self.p0.readAllStandardOutput()
        y=str(output)
        y=y[2:-1]
        xs = y.split("\\n")
        xs=xs[0:len(xs)-1]
        term="model:"
        term_len=len(term)
        occ = y.find(term)
        if occ==-1:
            self.hideProcess(process_window)


            def msgbtn(i):
                print ("Button pressed is:",i.text())
                if i.text()=="Exit":
                    sys.exit(0)
                else:
                    self.getDeviceName()
                    self.listOut("/")


            print("NOT FOUND")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Could not find any connected device on this computer")
            msg.setWindowTitle("Device Not Found")
            msg.setInformativeText("NOTE: Turn on USB debuging in the developer options")
            msg.addButton("Exit",QMessageBox.RejectRole)
            msg.addButton("Try Again",QMessageBox.AcceptRole)
            msg.buttonClicked.connect(msgbtn)
            retval = msg.exec_()


        
        else:
            occ=occ+term_len
            space_occ = y[occ:].find(" ")
            space_occ=space_occ+occ
            if y[occ:space_occ]:
                self.setWindowTitle(y[occ:space_occ])

        self.hideProcess(process_window)


    def listOut(self,name):
        self.p = QProcess()
        self.p.finished.connect(self.list_out_process_finished)
        name=self.escape(name)   
        self.p.start(helper.adb_path,["shell","ls","-d",name+"*/"])
        self.currentPath=name



    def gotAbsolutePath(self,name,btn):
        escaped_name=self.escape(name)
        np=self.currentPath+escaped_name
        self.p3 = QProcess()
        self.p3.finished.connect( lambda : self.pre_pull(btn))
        print("pp",np)
        self.p3.start(helper.adb_path,["shell","ls",np])



    def pre_pull(self,btn):
        output = self.p3.readAllStandardOutput()
        y=str(output)
        y=y[2:-1]
        xs = y.split("\\n")
        xs=xs[0:len(xs)-1]
        xs[0]=xs[0].replace("\\r","")
        self.pull(xs[0],btn)


    def push(self,filePath):

        patharr = os.path.split(filePath)
        # if patharr[1]=="":
        #     patharr = os.path.split(patharr[0])

        process_window_push = ProcessWindow(patharr[1],"FILE_TRANSFER")
        process_window_push.show()
        self.p4 = QProcess()
        self.p4.finished.connect(lambda : self.process_finished_push(process_window_push))
        self.p4.start(helper.adb_path,["push",filePath,self.currentPath])



    def pull(self,name,btn):
        btn.setEnabled(False)
        btn.start()
        self.p2 = QProcess()
        self.p2.finished.connect( lambda : self.process_finished_pull(btn))
        name=name.replace("\\r","")
        print("check",name,helper.home)
        self.p2.start(helper.adb_path,["pull",name,helper.home])


    def process_finished_push(self,process_window_push):
        process_window_push.close()
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
        self.p1.start(helper.adb_path,["shell","ls","-p",self.currentPath,"|","grep","-v","/"])
        


if __name__ == '__main__':

    app = QApplication(sys.argv)
    theme_type = darkdetect.theme()
    print("theme_type",theme_type)
    if theme_type == 'Dark':
        app.setStyle("Fusion")
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
    ex = App(theme_type)

    sys.exit(app.exec_())