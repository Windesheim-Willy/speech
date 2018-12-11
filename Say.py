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
   log("From here all logging will be in ~/.ros/log")
   
   rospy.init_node('sayText', anonymous=True)
   rospy.loginfo("Listener initialized")
   rospy.Subscriber("/speech", String, callback)
   rospy.spin()

def callback(textToSpeech):
   html_parser = HTMLParser.HTMLParser()
   unescaped = html_parser.unescape(textToSpeech.data)
   rospy.loginfo("Saving MP3 with text: " + unescaped)
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

   sleepTime = getSleepTime()
   log('Startup delay is set to ' + str(sleepTime) + ' seconds')
   time.sleep(sleepTime)

   log('Willy Speech Initializing')

   main(sys.argv[1:])