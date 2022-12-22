from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
channel_secret = "27b6044fca2f0f59f46001283189e291"
channel_access_token = "0YptVYTNVQbhpRCezn9hCys1U1nLiQyW6WWAI79h0fUhnUPnFigeXKuSkCDGfwMqYEGkz0X3wz8lqtS3Hbcg2eGpm1GnUyjBHpgcMTCe0tcpDxk34PL9EMk8/5tKi/0QRej7A1Jv5JsjbNEwA1YlgAdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
# line_bot_api.reply_message(res['events'][0]['replyToken'], 
#         TextSendMessage(res['events'][0]['message']['text'])
#     )

def get_choice(res):
    print(type(res['events'][0]['message']['text']))
    mess = 'hello, please select'+'\n'+'1. chatGPT' +'\n'+'2. me'
    line_bot_api.reply_message(res['events'][0]['replyToken'], 
        TextSendMessage(mess)
    )
