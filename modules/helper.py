import sys
import os
from os import remove
from os.path import expanduser



last_dropped_location=None
home = expanduser("~")
format_dic={"video":["mp4","mov","avi","mkv"],"music":["mp3","ogg","wav"],"doc":["pdf"],"image":["jpg","jpeg","png","gif"],"apps":["apk"]}
color_dic={"video":"darkRed","music":"darkMagenta","doc":"darkGreen","unkown":"darkGray","image":"darkCyan","apps":"Green"}

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)



#NOTE: Change it to adb executable path
adb_path="C:/Users/Hp Desk/AppData/Local/Android/Sdk/platform-tools/adb"
adb_path="./tools/win/adb.exe"
adb_path=resource_path(adb_path)
# adb_path="C:/Users/Hp Desk/AppData/Local/Android/Sdk/platform-tools/adb"






#Function to move file to tracked location after being pulled
def exchange_helper(placeholder,actualfile,isFolder=False):

    if isFolder:
        print("isFolder",placeholder,actualfile)
        if placeholder:
            var1 = os.path.split(placeholder)
            first_part=var1[0]
            # actualfile=actualfile.replace("/","\\")
            var2 = os.path.split(actualfile)
            second_part=var2[1]
            remove(placeholder)

            print("parts",first_part,second_part)
            var3 = first_part+"/"+second_part
            try:
                os.rename(actualfile, var3)
                print("FOLDER MOVED")
            except Exception as e:
                print("EXCEPTION WHILE MOVING FOLDER",e)
     

    else:
        if placeholder:
            var1 = os.path.split(placeholder)
            var2 = os.path.split(actualfile)
            first_part=var1[0]
            second_part=var2[1]
            remove(placeholder)
            var3 = first_part+"/"+second_part
            try:
                os.rename(actualfile, var3)
                print("FILE MOVED")
            except Exception as e:
                print("EXCEPTION WHILE MOVING FILE",e)
     
