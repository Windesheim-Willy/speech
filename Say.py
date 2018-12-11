#!/usr/bin/python

import sys
import getopt
import os
import rospy
import logging
import time
import datetime
import HTMLParser
from gtts import gTTS
from xml.dom import minidom
from std_msgs.msg import String

def log(message):
   time = str(datetime.datetime.now())
   logging.basicConfig(filename='rosspeech.log',level=logging.DEBUG)
   
   logger = logging.getLogger()
   
   logging.info(time + ' ' + message)
   logger.handlers[0].flush()


def getFileName():
   # Read settings file
   xmlDoc = minidom.parse('settings.xml')
   settings = xmlDoc.getElementsByTagName('setting')
   filename = ""
   for setting in settings:
      if  setting.attributes['name'].value == 'filename':
         filename = setting.firstChild.data
   return filename

def getFolder():
   # Read settings file
   xmlDoc = minidom.parse('settings.xml')
   settings = xmlDoc.getElementsByTagName('setting')
   folder = ""
   for setting in settings:
      if  setting.attributes['name'].value == 'folder':
         folder = setting.firstChild.data
   return folder

def getSleepTime():
   # Read settings file
   xmlDoc = minidom.parse('settings.xml')
   settings = xmlDoc.getElementsByTagName('setting')
   time = 0.0
   for setting in settings:
      if  setting.attributes['name'].value == 'sleep':
         time = setting.firstChild.data
   return float(time)

def listener():
   log("Listener start")
   rospy.init_node('sayText', anonymous=True)
   log("Listener initialized")
   rospy.Subscriber("/speech", String, callback)

   #while not rospy.core.is_shutdown():
      #log('test spk')
      #rospy.rostime.wallsleep(2)
   #rospy.spin()

def callback(textToSpeech):
   html_parser = HTMLParser.HTMLParser()
   unescaped = html_parser.unescape(textToSpeech.data)
   log("Saving MP3 with text: " + unescaped)
   tts = gTTS(text=textToSpeech.data, lang='nl')
   tts.save(getFolder() + getFileName())

def main(argv):
   listener()

if __name__ == "__main__":
   print('')
   print('**********************************')
   print('*** Willy Speech MP3 generator ***')
   print('**********************************')
   print('')
   log('')
   log('**********************************')
   log('*** Willy Speech MP3 generator ***')
   log('**********************************')
   log('')
   time.sleep(getSleepTime())
   log('Willy Speech Initializing')
   main(sys.argv[1:])