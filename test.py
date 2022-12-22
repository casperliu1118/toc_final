from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import func
import json

app = Flask(__name__)

channel_secret = "27b6044fca2f0f59f46001283189e291"
channel_access_token = "0YptVYTNVQbhpRCezn9hCys1U1nLiQyW6WWAI79h0fUhnUPnFigeXKuSkCDGfwMqYEGkz0X3wz8lqtS3Hbcg2eGpm1GnUyjBHpgcMTCe0tcpDxk34PL9EMk8/5tKi/0QRej7A1Jv5JsjbNEwA1YlgAdB04t89/1O/w1cDnyilFU="

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
    if level ==0 or res['events'][0]['message']['text'] == 'q':
        initial_state()

    if(level ==1):
        get_choice(res)
    if(level >=1):
        if(option ==1):
            state1()
        elif(option ==2):
            state2()
        elif(option == 3):
            state3()
        

    level +=1
    return 'OK'
def reply_mess(mes):
    line_bot_api.reply_message(res['events'][0]['replyToken'], 
        TextSendMessage(mes)
    )
def initial_state():
    global level
    level =0
    mess = 'hello, please select'+'\n'+'1. chatGPT' +'\n'+'2. me'
    reply_mess(mess)

def get_choice(res):
    global option 

    option = int(res['events'][0]['message']['text'])
    
def state1():
    reply_mess("state1")

def state2():
    reply_mess("state2")

def state3():
    reply_mess("state3")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)