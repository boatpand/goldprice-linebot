import requests
import threading

URL = "https://www.goldtraders.or.th"
raw_html = requests.get(URL).text

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
    # print(gold)
    return gold

# gold(raw_html)
data= gold(raw_html)

def autoData():
    threading.Timer(5.0, autoData).start()
    raw_html = requests.get(URL).text
    data = gold(raw_html)
    # print(gold)
    timeStamp = str(data["Date"])
    print(timeStamp)

    # try:
    #     prev_f = open("timeStamp.txt", "r")
    #     prev_timeStamp = prev_f.read()
    # except:
    #     f = open("timeStamp.txt", "w")
    #     f.write(timeStamp)
    #     f.close()
    #     prev_timeStamp = timeStamp
    
    prev_f = open("timeStamp.txt", "r")
    prev_timeStamp = prev_f.read()
    print(prev_timeStamp)
    print(type(prev_timeStamp))
     
    if(timeStamp!=prev_timeStamp):
        print("Data Updated!!")
        f = open("timeStamp.txt", "w")
        f.write(timeStamp)
        f.close()

        f = open("timeStamp.txt", "r")
        new_timeStamp = f.read()
        print("update : ",new_timeStamp)
    # else:
    #     print("same data")

autoData()

# timeStamp = str(data["Date"]) + str(data["Time"])
# print(timeStamp)

# prev_f = open("timeStamp.txt", "r")
# prev_timeStamp = prev_f.read()
# print(prev_timeStamp)

# f = open("timeStamp.txt", "w")
# f.write(timeStamp)
# f.close()