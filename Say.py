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
   logging.info(time + ' ' + message)
   logging.handlers[0].flush()

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

def listener():
   log("Listener start")
   rospy.init_node('sayText', anonymous=True)
   log("Listener initialized")
   rospy.Subscriber("/speech", String, callback)
   rospy.spin()

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
   time.sleep(60)
   log('Willy Speech Initializing')
   main(sys.argv[1:])