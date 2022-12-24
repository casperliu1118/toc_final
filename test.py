# -*- coding: cp950 -*-
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,AudioSendMessage
import json
import chatgpt
import random
import re
import speeak
from urllib.parse import quote
app = Flask(__name__)

channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

level =0
state =99
option=0
res = 'hello'
ngrok_url = "https://1df2-140-116-112-158.jp.ngrok.io"

@app.route("/callback", methods=['POST'])
def callback():
    global level
    global res
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print('level = '+str(level))
    res = json.loads(body)
    profile = line_bot_api.get_profile(res['events'][0]['source']['userId'])
    #print(profile)
    if res['events'][0]['message']['text'] == 'FSM':
        reply_picture(ngrok_url+ "/static/FSM.jpg")
    elif level ==0 or res['events'][0]['message']['text'] == 'q':
        initial_state(profile.display_name)
        # image_message = ImageSendMessage(original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
        # preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
        # )
        # line_bot_api.reply_message(res['events'][0]['replyToken'], image_message)
    elif(level ==1):
        if(len(res['events'][0]['message']['text'])>1):
            a =[]
            for w in res['events'][0]['message']['text']:
                if w in a:
                    reply_mess(w+"！")
                    break
                else:
                    a.append(w)
            if(len(a)==len(res['events'][0]['message']['text'])):
                initial_state(profile.display_name)
            level =0
        else:
            get_choice(res)
    if(level >=1):
        if(option ==1):
            state1(profile.status_message)
        elif(option ==2):
            state2(profile.picture_url)
        elif(option == 3):
            state3()
        elif(option == 4):
            state4()

    level +=1
    return 'OK'
def reply_sound(mes):
    speeak.tts(mes)
    message = AudioSendMessage(
                    original_content_url = ngrok_url+"/static/welcome.mp3",
                    duration=5000
            )
    line_bot_api.reply_message(res['events'][0]['replyToken'],
    message)

def reply_mess(mes):
    line_bot_api.reply_message(res['events'][0]['replyToken'], 
        TextSendMessage(mes)
    )
        
def reply_picture(url):
    line_bot_api.reply_message(res['events'][0]['replyToken'], 
        ImageSendMessage(original_content_url = url, 
        preview_image_url = url))

def initial_state(name):
    global level
    level =0
    #profile = line_bot_api.get_profile('<user_id>')
    #print(profile)

    mess = '哈嘍'+name[1:]+', please select:'+'\n\n'+'1. 《人生導師》' +'\n'+'2. 《看帥哥》'+'\n'+'3. 《進入山洞》'+'\n'+'4. 《要吃什麼？》'
    reply_mess(mess)

def get_choice(res):
    global option 

    option = int(res['events'][0]['message']['text'])
    
def state1(mes):
    if(level ==1):
        reply_mess("黑, 幫你聯絡MENTOR\n他說：What can I help you?")
    #elif(level ==4):
    #    reply_mess("你對「" +mes + "」怎麼看？")
    else:
        response = chatgpt.chat(res['events'][0]['message']['text'])

        reply_mess("他說："+response[2:])
mirror =1
pic_status =1
def state2(url):
    place = "/static/IMG_9622.jpg"
    #reply_picture(ngrok_url+place)
    global mirror,pic_status
    if('帥'in res['events'][0]['message']['text']):
        mirror =1
    elif('梗圖' in res['events'][0]['message']['text'] or 
    '別的' in res['events'][0]['message']['text']):
        mirror =0
    if mirror ==1:
        reply_picture(url)
    else:
        reply_picture(ngrok_url+ "/static/" + str(pic_status)+ ".jpg")
        if(pic_status ==2):
            pic_status =1
        else:
            pic_status =2
depth =1
audio =0
def state3():
    global depth, audio
    if(level ==1):
        reply_mess("歡迎來到大山洞 洞洞洞...")
        return
    if('好黑' in res['events'][0]['message']['text'] or '看不見' in res['events'][0]['message']['text']):
        audio =1
        reply_sound("那我用唸的")
        return 
    if('火' in res['events'][0]['message']['text']or 
        '電' in res['events'][0]['message']['text'] or 
        '光' in res['events'][0]['message']['text']):
        reply_sound("太好了！變亮嘍")
        audio =0
        return 
    if("向前" in res['events'][0]['message']['text']):
        depth +=1
        if depth >3:
            depth =3
            if audio == 0:
                reply_mess("你撞到牆了\n"*depth)
            else:
                reply_sound("你撞到牆了\n"*depth)

            return
    elif("向後" in res['events'][0]['message']['text']):
        depth -=1
        if depth<0:
            depth =0
    if("向前" in res['events'][0]['message']['text'] or "向後" in res['events'][0]['message']['text']):
        if depth>0:
            if audio==0:
                reply_mess("啪嗒 "*depth)
            else:
                reply_sound("啪嗒 "*depth)
        else :
            if audio==0:
                reply_mess("從山洞出來了")
            else:
                reply_sound("從山洞出來了")
                audio =0

    else:
        echo_sound =""
        if(depth ==0):
            reply_mess("（沒回音）\n（為什麼要對空氣說話）")
            return
        for w in res['events'][0]['message']['text']:
            echo_sound += w*depth
        if audio == 0:
            reply_mess(echo_sound[::-1])
        else:
            reply_sound(echo_sound+echo_sound[-1])

food = []
def state4():
    global food
    if(res['events'][0]['message']['text'] == '吃啥' or
    "這樣" in res['events'][0]['message']['text'] or
    "就醬" in res['events'][0]['message']['text']):
        print(food)
        reply_mess('那就吃'+random.choice(food)+'好了')
    else:
        if(level ==1):
            reply_mess("說一下你的選項：")
        else:
            reply_mess("還有咧")
            food.append(res['events'][0]['message']['text'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

    # 啪嗒啪嗒改成語音合成
    # 翻譯->爬蟲