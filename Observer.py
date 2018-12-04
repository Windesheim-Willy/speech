import time
import os
import pygame

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pygame import mixer
from xml.dom import minidom

def GetVolume():
   # Read settings file
   xmlDoc = minidom.parse('settings.xml')
   settings = xmlDoc.getElementsByTagName('setting')
   volumeValue = float(0)
   for setting in settings:
      if  setting.attributes['name'].value == 'volume':
         volumeValue = setting.firstChild.data
   return volumeValue

def GetFolder():
   # Read settings file
   xmlDoc = minidom.parse('settings.xml')
   settings = xmlDoc.getElementsByTagName('setting')
   folder = ""
   for setting in settings:
      if  setting.attributes['name'].value == 'folder':
         folder = setting.firstChild.data
   return folder

def CleanFolder():
   # Clean folder
   print("delete files from folder")
   mydir =  GetFolder()
   filelist = [ f for f in os.listdir(mydir) if f.endswith(".mp3") ]
   for f in filelist:
      os.remove(os.path.join(mydir, f))

class Watcher:
   DIRECTORY_TO_WATCH = GetFolder()
   def __init__(self):
      self.observer = Observer()

   def run(self):
      event_handler = Handler()
      self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
      self.observer.start()
      try:
         while True:
            time.sleep(5) #time in seconds
      except:
         self.observer.stop()
         print "Error"

      self.observer.join()

class Handler(FileSystemEventHandler):
   @staticmethod
   def on_any_event(event):
      if event.is_directory:
         return None

      elif event.event_type == 'created':
         # Notify on reception of file and initialize
         print "Received file - %s." % event.src_path
         mixer.init()

         # Get volume setting
         mixer.music.set_volume(float(GetVolume()))
         print("volume: " + str(pygame.mixer.music.get_volume()))

         # Play file
         mixer.music.load(event.src_path)
         mixer.music.play()

         # Clean up folder
         os.remove(event.src_path)
         print("File Removed!")

if __name__ == '__main__':
   print('')
   print('*****************************')
   print('*** Willy Speech Observer ***')
   print('*****************************')
   print('')
   CleanFolder()
   w = Watcher()
   w.run()
