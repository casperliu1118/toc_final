# -*- coding: cp950 -*-

import time
# Import the required module for text 
# to speech conversion
from gtts import gTTS
import shutil
  
# This module is imported so that we can 
# play the converted audio
import os
import azure.cognitiveservices.speech as speechsdk

# 複製貼上你的剛剛的參數
speech_key, service_region = "<貼上你的key>", "<貼上你所選的區域>"  ## 沒有 <> 這個符號

def STT(text="說出一句話"):
    #先config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language='zh-tw')
    #創建分辨器
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config = speech_config)
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def TTS(text):
    print(text)
    #先config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # The full list of supported languages can be found here:
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support#text-to-speech
    #設定語系或是設定指定人的聲音(擇一)
    
    # #特定語系
    language = "zh-TW"
    speech_config.speech_synthesis_language = language

    # #特定人聲
    # voice = "Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)"
    # speech_config.speech_synthesis_voice_name = voice

    # 創建語音合成器Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config = speech_config)


    # Synthesizes the received text to speech.
    # The synthesized speech is expected to be heard on the speaker with this line executed.
    result = speech_synthesizer.speak_text_async(text).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # print("Speech synthesized to speaker for text [{}]".format(text))
        pass
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
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

