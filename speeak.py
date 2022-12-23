# -*- coding: cp950 -*-
import time
# Import the required module for text 
# to speech conversion
from gtts import gTTS
import shutil
  
# This module is imported so that we can 
# play the converted audio
import os
def tts(mytext):
# The text that you want to convert to audio
#mytext = '這樣可以嗎' #怎麼做中文的

    
    # Language in which you want to convert
    language = 'zh-tw'
    
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
    
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save("welcome.mp3")
    time.sleep(3)
    shutil.move("welcome.mp3", "static/welcome.mp3")

    # Playing the converted file

