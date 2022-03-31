from importlib.resources import contents
from flask import Flask, jsonify, render_template, request
import requests
import json
import numpy as np
import threading
import datetime

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage, FlexSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)

URL = "https://www.goldtraders.or.th"

lineaccesstoken = 'T3ayj4TD2rhw4kuCya1hhLLxXKOWgdOuxhmUCyQn0SPD+2ClYWbPIw0ieJsOW3B8yjVyx7+YX6JGxHw6TkNqGeMb+h07PmmEJiKtRJaNo+dse9m6a5hTxmgeASfSx+Tsem1LC2LJK221ZqFgRrfCggdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)

@app.route('/')
def index():
    return "hello world"

@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '',200

def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''

    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)

    if msgType == "text":
        msg = str(event["message"]["text"])
        replyObj = handle_message(msg)
        line_bot_api.reply_message(rtoken, replyObj)

def handle_message(inpmessage):
    if inpmessage == "ราคาทองวันนี้":
        flex = flexMessage()
        replyObj = FlexSendMessage(alt_text="Flex Message alt text", contents=flex)
    else:
        msg = 'พิมพ์ "ราคาทองวันนี้" เพื่อทราบราคาทอง'
        replyObj = TextSendMessage(text=msg)
    return replyObj

def flexMessage():
    res = getData()
    Date, GoldBullionSellingPrice, GoldBullionSellingPriceTrend, GoldBullionPurchasePrice, GoldBullionPurchasePriceTrend, GoldJewelrySellingPrice, GoldJewelrySellingPriceTrend, TaxBase, TaxBaseTrend = res
    flex = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://cdn-icons-png.flaticon.com/512/1473/1473504.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "backgroundColor": "#F7F55AFF",
            "action": {
            "type": "uri",
            "label": "Action",
            "uri": "https://linecorp.com"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "action": {
            "type": "uri",
            "label": "Action",
            "uri": "https://linecorp.com"
            },
            "contents": [
            {
                "type": "text",
                "text": "ราคาทองวันนี้",
                "weight": "bold",
                "size": "xl",
                "contents": []
            },
            {
                "type": "text",
                "text": Date,
                "weight": "bold",
                "size": "sm",
                "contents": []
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://cdn-icons-png.flaticon.com/512/138/138540.png",
                    "size": "xl"
                },
                {
                    "type": "text",
                    "text": "ทองคำแท่ง 96.5%",
                    "weight": "bold",
                    "size": "xl",
                    "margin": "lg",
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "ขายออก",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xxl",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": GoldBullionSellingPrice,
                        "weight": "bold",
                        "size": "xl",
                        "color": GoldBullionSellingPriceTrend,
                        "align": "end",
                        "contents": []
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "รับซื้อ",
                        "weight": "bold",
                        "size": "xl",
                        "flex": 0,
                        "margin": "xxl",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": GoldBullionPurchasePrice,
                        "weight": "bold",
                        "size": "xl",
                        "color": GoldBullionPurchasePriceTrend,
                        "align": "end",
                        "contents": []
                    }
                    ]
                }
                ]
            },
            {
                "type": "box",
                "layout": "baseline",
                "contents": [
                {
                    "type": "icon",
                    "url": "https://cdn-icons-png.flaticon.com/512/2022/2022643.png",
                    "size": "xl"
                },
                {
                    "type": "text",
                    "text": "ทองรูปพรรณ 96.5%",
                    "weight": "bold",
                    "size": "xl",
                    "margin": "lg",
                    "contents": []
                }
                ]
            },
            {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "ขายออก",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xxl",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": GoldJewelrySellingPrice,
                        "weight": "bold",
                        "size": "xl",
                        "color": GoldJewelrySellingPriceTrend,
                        "align": "end",
                        "contents": []
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": "ฐานภาษี",
                        "weight": "bold",
                        "size": "xl",
                        "flex": 0,
                        "margin": "xxl",
                        "contents": []
                    },
                    {
                        "type": "text",
                        "text": TaxBase,
                        "weight": "bold",
                        "size": "xl",
                        "color": TaxBaseTrend,
                        "align": "end",
                        "contents": []
                    }
                    ]
                }
                ]
            }
            ]
        }
    }

    return flex

def getDate(raw_html):
    pattern_start = 'ประจำวันที่ <span id="DetailPlace_uc_goldprices1_lblAsTime"><b><font size="3">'
    pattern_end = '</font>'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            date = raw_html[start:end]
            index = end
        else:
            break
    return date

# ราคาขายออกทองคำแท่ง 96.5%
def getGoldBullionSellingPrice(raw_html):
    pattern_start = '<span id="DetailPlace_uc_goldprices1_lblBLSell"><b><font color='
    pattern_end = '</font>'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            cost = raw_html[start:end]
            cost = cost.replace('"','')
            costNtrend = cost.split(">")
            index = end
        else:
            break
    return costNtrend

# ราคารับซื้อทองคำแท่ง 96.5%
def getGoldBullionPurchasePrice(raw_html):
    pattern_start = '<span id="DetailPlace_uc_goldprices1_lblBLBuy"><b><font color='
    pattern_end = '</font>'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            cost = raw_html[start:end]
            cost = cost.replace('"','')
            costNtrend = cost.split(">")
            index = end
        else:
            break
    return costNtrend

# ราคาขายออกทองรูปพรรณ 96.5%
def getGoldJewelrySellingPrice(raw_html):
    pattern_start = '<span id="DetailPlace_uc_goldprices1_lblOMSell"><b><font color='
    pattern_end = '</font>'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            cost = raw_html[start:end]
            cost = cost.replace('"','')
            costNtrend = cost.split(">")
            index = end
        else:
            break
    return costNtrend

# ฐานภาษีทองคำรูปพรรณ 96.5%
def getTaxBase(raw_html):
    pattern_start = '<span id="DetailPlace_uc_goldprices1_lblOMBuy"><b><font color='
    pattern_end = '</font>'
    index = 0
    length = len(raw_html)
    while index < length:
        start = raw_html.find(pattern_start, index)
        if start > 0:
            start = start + len(pattern_start)
            end = raw_html.find(pattern_end, start)
            cost = raw_html[start:end]
            cost = cost.replace('"','')
            costNtrend = cost.split(">")
            index = end
        else:
            break
    return costNtrend

def gold(raw_html):
    gold = {
    # ข้อมูลประจำวันที่
    "Date":getDate(raw_html),
    # ราคาขายออกทองคำแท่ง 96.5%
    "Gold bullion selling price 96.5%":getGoldBullionSellingPrice(raw_html),
    # ราคารับซื้อทองคำแท่ง 96.5%
    "Gold bullion purchase price 96.5%":getGoldBullionPurchasePrice(raw_html),
    # ราคาขายออกทองคำรูปพรรณ 96.5%
    "Gold jewelry selling price 96.5%":getGoldJewelrySellingPrice(raw_html),
    # ฐานภาษี ทองคำรูปประพรรณ
    "Tax base":getTaxBase(raw_html),
    }
    return gold

def getData():
    raw_html = requests.get(URL).text
    data = gold(raw_html)
    Date = str(data["Date"])
    GoldBullionSellingPrice = str(data["Gold bullion selling price 96.5%"][1])
    if(data["Gold bullion selling price 96.5%"][0]=="Green"):
        GoldBullionSellingPriceTrend = "#1E9D07"
    elif(data["Gold bullion selling price 96.5%"][0]=="Red"):
        GoldBullionSellingPriceTrend = "#D50606"
    else:
        GoldBullionSellingPriceTrend = "#000000"

    GoldBullionPurchasePrice = str(data["Gold bullion purchase price 96.5%"][1])
    if(data["Gold bullion purchase price 96.5%"][0]=="Green"):
        GoldBullionPurchasePriceTrend = "#1E9D07"
    elif(data["Gold bullion purchase price 96.5%"][0]=="Red"):
        GoldBullionPurchasePriceTrend = "#D50606"
    else:
        GoldBullionPurchasePriceTrend = "#000000"

    GoldJewelrySellingPrice = str(data["Gold jewelry selling price 96.5%"][1])
    if(data["Gold jewelry selling price 96.5%"][0]=="Green"):
        GoldJewelrySellingPriceTrend = "#1E9D07"
    elif(data["Gold jewelry selling price 96.5%"][0]=="Red"):
        GoldJewelrySellingPriceTrend = "#D50606"
    else:
        GoldJewelrySellingPriceTrend = "#000000"

    TaxBase = str(data["Tax base"][1])
    if(data["Tax base"][0]=="Green"):
        TaxBaseTrend = "#1E9D07"
    elif(data["Tax base"][0]=="Red"):
        TaxBaseTrend = "#D50606"
    else:
        TaxBaseTrend = "#000000"

    return Date, GoldBullionSellingPrice, GoldBullionSellingPriceTrend, GoldBullionPurchasePrice, GoldBullionPurchasePriceTrend, GoldJewelrySellingPrice, GoldJewelrySellingPriceTrend, TaxBase, TaxBaseTrend

def autoData():
    threading.Timer(60.0, autoData).start()
    msg = str(datetime.datetime.now())
    line_bot_api.broadcast(TextSendMessage(text=msg))
    print(msg)
    raw_html = requests.get(URL).text
    data = gold(raw_html)
    timeStamp = str(data["Date"])

    prev_f = open("timeStamp.txt", "r")
    prev_timeStamp = prev_f.read()

    if(timeStamp!=prev_timeStamp):
        f = open("timeStamp.txt", "w")
        f.write(timeStamp)
        f.close()
        msg = "ราคาทองมีการเปลี่ยนแปลง!! ณ เวลา " + str(timeStamp)
        line_bot_api.broadcast(TextSendMessage(text=msg))
        flex = flexMessage()
        replyObj = FlexSendMessage(alt_text="Flex Message alt text", contents=flex)
        line_bot_api.broadcast(replyObj)
    else:
        msg = "ทดสอบสำเร็จ"
        line_bot_api.broadcast(TextSendMessage(text=msg))
        print(msg)

# autoData()
threading.Timer(60.0, autoData).start()

if __name__ == '__main__':
    app.run(debug=True)