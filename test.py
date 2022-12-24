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
                    reply_mess(w+"�I")
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

    mess = '����'+name[1:]+', please select:'+'\n\n'+'1. �m�H�;ɮv�n' +'\n'+'2. �m�ݫӭ��n'+'\n'+'3. �m�i�J�s�}�n'+'\n'+'4. �m�n�Y����H�n'
    reply_mess(mess)

def get_choice(res):
    global option 

    option = int(res['events'][0]['message']['text'])
    
def state1(mes):
    if(level ==1):
        reply_mess("��, ���A�p��MENTOR\n�L���GWhat can I help you?")
    #elif(level ==4):
    #    reply_mess("�A��u" +mes + "�v���ݡH")
    else:
        response = chatgpt.chat(res['events'][0]['message']['text'])

        reply_mess("�L���G"+response[2:])
mirror =1
pic_status =1
def state2(url):
    place = "/static/IMG_9622.jpg"
    #reply_picture(ngrok_url+place)
    global mirror,pic_status
    if('��'in res['events'][0]['message']['text']):
        mirror =1
    elif('���' in res['events'][0]['message']['text'] or 
    '�O��' in res['events'][0]['message']['text']):
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
        reply_mess("�w��Ө�j�s�} �}�}�}...")
        return
    if('�n��' in res['events'][0]['message']['text'] or '�ݤ���' in res['events'][0]['message']['text']):
        audio =1
        reply_sound("���ڥΰ᪺")
        return 
    if('��' in res['events'][0]['message']['text']or 
        '�q' in res['events'][0]['message']['text'] or 
        '��' in res['events'][0]['message']['text']):
        reply_sound("�Ӧn�F�I�ܫG��")
        audio =0
        return 
    if("�V�e" in res['events'][0]['message']['text']):
        depth +=1
        if depth >3:
            depth =3
            if audio == 0:
                reply_mess("�A������F\n"*depth)
            else:
                reply_sound("�A������F\n"*depth)

            return
    elif("�V��" in res['events'][0]['message']['text']):
        depth -=1
        if depth<0:
            depth =0
    if("�V�e" in res['events'][0]['message']['text'] or "�V��" in res['events'][0]['message']['text']):
        if depth>0:
            if audio==0:
                reply_mess("���� "*depth)
            else:
                reply_sound("���� "*depth)
        else :
            if audio==0:
                reply_mess("�q�s�}�X�ӤF")
            else:
                reply_sound("�q�s�}�X�ӤF")
                audio =0

    else:
        echo_sound =""
        if(depth ==0):
            reply_mess("�]�S�^���^\n�]������n��Ů𻡸ܡ^")
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
    if(res['events'][0]['message']['text'] == '�Yԣ' or
    "�o��" in res['events'][0]['message']['text'] or
    "�N��" in res['events'][0]['message']['text']):
        print(food)
        reply_mess('���N�Y'+random.choice(food)+'�n�F')
    else:
        if(level ==1):
            reply_mess("���@�U�A���ﶵ�G")
        else:
            reply_mess("�٦���")
            food.append(res['events'][0]['message']['text'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

    # ���ְ��֧令�y���X��
    # ½Ķ->����