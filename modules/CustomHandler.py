from watchdog.events import FileSystemEventHandler
import modules.helper as helper


#Custom handler class for watchdog observer
class CustomHandler(FileSystemEventHandler):
    def on_created(self, event):
        if ".adbfm" in event.src_path and "ADBFileManager" not in event.src_path :
            print("on_created", event.src_path)
            helper.last_dropped_location=event.src_path
            print("last_dropped_location changed",event.src_path)
