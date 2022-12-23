# -*- coding: cp950 -*-
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
import json
import chatgpt
import random
app = Flask(__name__)

channel_secret = os.environ.get('LINE_CHANNEL_SECRET')
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

level =0
state =99
option=0
res = 'hello'

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
    if level ==0 or res['events'][0]['message']['text'] == 'q':
        initial_state(profile.display_name)
        # image_message = ImageSendMessage(original_content_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png',
        # preview_image_url='https://media.nownews.com/nn_media/thumbnail/2019/10/1570089924-27a9b9c9d7facd3422fe4610dd8ebe42-696x386.png'
        # )
        # line_bot_api.reply_message(res['events'][0]['replyToken'], image_message)
    elif(level ==1):
        # if(len(res['events'][0]['message']['text'])>1):
        #     a =[]
        #     for w in res['events'][0]['message']['text']:
        #         if w in a:
        #             reply_mess(w+"！")
        #             break
        #         else:
        #             a.append(w)
        #     # if(len(a)==len(res['events'][0]['message']['text'])):
        #     #     initial_state(profile.display_name)
        #     level =0
        # else:
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

    mess = '哈嘍'+name[1:]+', please select:'+'\n'+'1. 《人生導師》:)' +'\n'+'2. 《看帥哥》'+'\n'+'3. 《進入山洞》'+'\n'+'4. 要吃什麼？'
    reply_mess(mess)

def get_choice(res):
    global option 

    option = int(res['events'][0]['message']['text'])
    
def state1(mes):
    if(level ==1):
        reply_mess("黑, i am your MENTOR\nWhat can I help you?")
    #elif(level ==4):
    #    reply_mess("你對「" +mes + "」怎麼看？")
    else:
        response = chatgpt.chat(res['events'][0]['message']['text'])

        reply_mess(response[2:])

def state2(url):
    ngrok_url = "https://742b-140-116-112-158.jp.ngrok.io"
    place = "/static/IMG_9622.jpg"
    #reply_picture(ngrok_url+place)
    reply_picture(url)
depth =1
def state3():
    global depth
    if(level ==1):
        reply_mess("歡迎來到大山洞 洞洞洞...")
        return
    if(res['events'][0]['message']['text'] == "向前走"):
        depth +=1
        if depth >3:
            depth =3
            reply_mess("你撞到牆了\n"*depth)
            return
    elif(res['events'][0]['message']['text'] == "向後走"):
        depth -=1
        if depth<0:
            depth =0
    if(res['events'][0]['message']['text'] == "向前走" or res['events'][0]['message']['text'] == "向後走"):
        if depth>0:
            reply_mess("啪嗒 "*depth)
        else :
            reply_mess("從山洞出來了")
    else:
        echo_sound =""
        if(depth ==0):
            reply_mess("（沒回音）\n（為什麼要對空氣說話）")
            return
        for w in res['events'][0]['message']['text']:
            echo_sound += w*depth
        reply_mess(echo_sound[::-1])
food = []
def state4():
    global food
    if(res['events'][0]['message']['text'] == '吃啥'):
        reply_mess('那就吃'+random.choice(food)+'好了')
    else:
        if(level ==1):
            reply_mess("說一下你的選項：")
        else:
            reply_mess("還有咧")
        food.append(res['events'][0]['message']['text'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)