#!/usr/bin/python

import sys
import getopt
import os
import rospy
from gtts import gTTS
from xml.dom import minidom
from std_msgs.msg import String

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
   print("Listener start")
   rospy.init_node('sayText', anonymous=True)
   print("Listener initialized")
   rospy.Subscriber("/speech", String, callback)
   rospy.spin()

def callback(textToSpeech):
   if textToSpeech.data == 'aboutMe':
      rospy.loginfo("About Willy")
      textToSpeech.data = aboutMe()
   else:
      rospy.loginfo("Dit is de text: " + textToSpeech.data)
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
   main(sys.argv[1:])