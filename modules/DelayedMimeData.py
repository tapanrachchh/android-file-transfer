

import os
from PyQt5 import QtCore

if os.name == 'nt':
    import win32api
    def mouse_pressed():
        return win32api.GetKeyState(0x01) not in [0, 1]
else:
    import mouse
    def mouse_pressed():
        return mouse.is_pressed()


#Code Reference for DelayedMimeData :  pyjamas - stackoverflow
class DelayedMimeData(QtCore.QMimeData):
    def __init__(self):
        super().__init__()
        self.callbacks = []

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def retrieveData(self, mime_type: str, preferred_type: QtCore.QVariant.Type):
        mp = mouse_pressed()
        if not mp:
            for callback in self.callbacks.copy():
                self.callbacks.remove(callback)
                callback()
        return QtCore.QMimeData.retrieveData(self, mime_type, preferred_type)