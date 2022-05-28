
import os
from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtCore import QPoint, QProcess, QRectF, QSize, Qt, pyqtSlot,QMimeData
from PyQt5.QtGui import QPainter, QPixmap,QDrag
from PyQt5 import QtCore
from modules.CustomHandler import CustomHandler
import time
from modules.helper import resource_path,exchange_helper
from os.path import expanduser
import threading
import modules.helper as helper

#NOTE: Change it to adb executable path
adb_path="C:/Users/Hp Desk/AppData/Local/Android/Sdk/platform-tools/adb"
adb_path="./tools/win/adb.exe"
adb_path=resource_path(adb_path)
# adb_path="C:/Users/Hp Desk/AppData/Local/Android/Sdk/platform-tools/adb"


#Watchdog used to track drag location in system file manager
from watchdog.observers import Observer
from modules.ProcessWindow import ProcessWindow

import tempfile
from modules.helper import exchange_helper
from modules.DelayedMimeData import DelayedMimeData

class CustomDraggableWidget(QWidget):
    instances=[]
    def __init__(self,a,func=None):
        QWidget.__init__(self)
        self.fname=a
        self.listOut=func
        if func:
            self.__class__.instances.append(self)


        self.setAcceptDrops(False)



    def mouseDoubleClickEvent(self,event):
        if self.listOut:
            self.listOut(self.fname)
            return

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
            

            for i in CustomDraggableWidget.instances:
                i.setStyleSheet('''background-color:none;''')

            if self.listOut:
                self.setStyleSheet('''background-color:#777;''')




    def pull_finised(self,name):
        tempfolder = os.path.join(tempfile.gettempdir(), 'ADBFileManager')

            

       
        print("pull_finised")
        helper.last_dropped_location
        exchange_helper(helper.last_dropped_location,tempfolder+"/"+self.just_folder_name,True)
        self.process_window_new.close()

        #Reseting last_dropped_location
        helper.last_dropped_location=None


 
        
            

    def mouseMoveEvent(self, event):

        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return





        if self.listOut:
            print("FOR DROPPING A FOLDER")
            self.drag = QDrag(self)
            mimedata = DelayedMimeData()
            self.path_list=[]
            copy_named=self.fname
            copy_named=copy_named.replace("/\\r","")
            self.just_folder_name=os.path.basename(os.path.normpath(copy_named))
            print("copy_named",self.just_folder_name)
            ptemp = os.path.join(tempfile.gettempdir(), 'ADBFileManager', self.just_folder_name,"folder."+self.just_folder_name+".adbfm")
            # ptempdir = os.path.join(tempfile.gettempdir(), 'ADBFileManager', self.just_folder_name)

            os.makedirs(os.path.dirname(ptemp), exist_ok=True)

            def watcher():

                print("Watching -> Stared")
                event_handler = CustomHandler()
                observer = Observer()
                observer.schedule(event_handler, path=helper.home, recursive=True)
                observer.start()
                try:
                    while helper.last_dropped_location==None:
                        time.sleep(1)
                finally:
                    observer.stop()
                    observer.join()
                print("Watching -> QUIT")



            def write_to_file():
                #Writing a placeholder file to track it's drag location 
                with open(ptemp, 'w+') as f:
                    f.write(f"placeholder folder file")


                #Starting a thread to run watchdog
                watcher_thread = threading.Thread(target=watcher, name="Watcher", args=[])
                watcher_thread.start()


                print("pulling...")
                #Starting a process to pull the dragged file
                name = self.fname
                self.pxf = QProcess()
                self.pxf.finished.connect(lambda : self.pull_finised(self.fname))
                name=name.replace("\\r","")
                # ptempdir=ptemp
                ptempdir= os.path.split(ptemp)
                ptempdir=os.path.split(ptempdir[0])
                print("ptempdir",ptempdir[0])

                self.pxf.start(adb_path,["pull",name,ptempdir[0]])
                print("pxf started")
                self.process_window_new = ProcessWindow(self.just_folder_name,"FILE_TRANSFER")
                self.process_window_new.show()




            mimedata.add_callback(write_to_file)
    
            self.path_list.append(QtCore.QUrl.fromLocalFile(ptemp))
            mimedata.setUrls(self.path_list)
            self.drag.setMimeData(mimedata)
            pixmap = QPixmap(self.size())
            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()
            self.drag.setPixmap(pixmap)
            self.drag.setHotSpot(event.pos())
            self.drag.exec_(Qt.MoveAction)



        else:
            print("FOR DROPPING A FILE")

            self.drag = QDrag(self)
            mimedata = DelayedMimeData()
            self.path_list=[]
            copy_named=self.fname
            copy_named=copy_named.replace("\\","")
            self.actual_filename= os.path.basename(os.path.normpath(copy_named))


            ptemp = os.path.join(tempfile.gettempdir(), 'ADBFileManager', self.actual_filename+".adbfm")
            os.makedirs(os.path.dirname(ptemp), exist_ok=True)

            def watcher():

                print("Watching -> Stared")
                event_handler = CustomHandler()
                observer = Observer()
                observer.schedule(event_handler, path=helper.home, recursive=True)
                observer.start()
                helper.last_dropped_location
                try:
                    while helper.last_dropped_location==None:
                        time.sleep(1)
                finally:
                    observer.stop()
                    observer.join()
                print("Watching -> QUIT")


            def write_to_file():


                print("Www")

                #Writing a placeholder file to track it's drag location 
                with open(ptemp, 'w+') as f:
                    f.write(f"placeholder file")


                #Starting a thread to run watchdog
                watcher_thread = threading.Thread(target=watcher, name="Watcher", args=[])
                watcher_thread.start()

                print("pullll")

                #Starting a process to pull the dragged file
                name = self.fname
                self.px1 = QProcess()
                self.px1.finished.connect(self.pre_pull)
                self.px1.start(adb_path,["shell","ls",name])
                self.process_window_new = ProcessWindow(self.actual_filename,"FILE_TRANSFER")
                self.process_window_new.show()



            mimedata.add_callback(write_to_file)
    
            self.path_list.append(QtCore.QUrl.fromLocalFile(ptemp))
            mimedata.setUrls(self.path_list)
            self.drag.setMimeData(mimedata)
            pixmap = QPixmap(self.size())
            painter = QPainter(pixmap)
            painter.drawPixmap(self.rect(), self.grab())
            painter.end()
            self.drag.setPixmap(pixmap)
            self.drag.setHotSpot(event.pos())
            self.drag.exec_(Qt.MoveAction)



    def pre_pull(self):
        print("fin pp")
        output = self.px1.readAllStandardOutput()
        y=str(output)
        y=y[2:-1]
        xs = y.split("\\n")
        xs=xs[0:len(xs)-1]
        xs[0]=xs[0].replace("\\r","")
        self.pull(xs[0])


    def pull(self,name):
        
        print("ppppppp")
        tempfolder = os.path.join(tempfile.gettempdir(), 'ADBFileManager')

        def finish_all():
            print("fin all")
            print("ldl",helper.last_dropped_location)
            exchange_helper(helper.last_dropped_location,tempfolder+"/"+self.actual_filename)
            self.process_window_new.close()

            #Reseting last_dropped_location
            helper.last_dropped_location=None

        
        self.px2 = QProcess()
        self.px2.finished.connect(finish_all)
        name=name.replace("\\r","")
        self.px2.start(adb_path,["pull",name,tempfolder])
        

