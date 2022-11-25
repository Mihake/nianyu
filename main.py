from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]
user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]
tx_key = os.environ["TX_KEY"]

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

today = datetime.now()

def get_weather():
  url = "http://api.tianapi.com/tianqi/index?key="+ tx_key +"&city=" + city +"市"
  res = requests.get(url).json()
  weather = res['newslist'][0]
  newdate = weather['date']
  return newdate, weather['week'], weather['weather'], weather['real'], weather['lowest'], weather['highest'], weather['pcpn'], weather['uv_index'], weather['tips'], weather['windspeed'], weather['windsc'], weather['humidity'], weather['sunrise'], weather['sunset'],

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

##
def get_age():
  delta = today - datetime.strptime('2001-'+ birthday, "%Y-%m-%d")
  return int(delta.days/365)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
newdate,week,weather,real,lowest,highest,pcpn,uv_index,tips,windspeed,windsc,humidity,sunrise,sunset = get_weather()
data = {
  "love_days":{"value":get_count()},
  "date":{"value":newdate},
  "week":{"value":week},
  "min_temperature":{"value":lowest,},
  "max_temperature": {"value":highest},
  "now_temperature":{"value":real},
  "rain_fall":{"value":pcpn},
  "windspeed":{"value":windspeed},
  "windsc":{"value":windsc},
  "uv_index":{"value":uv_index},
  "humidity":{"value":humidity},
  "sunrise":{"value":sunrise},
  "sunset":{"value":sunset},
  "weather":{"value":weather},
  "weather_tips":{"value":tips},
  "age":{"value":get_age()},
  "birthday":{"value":get_birthday()},
  "words":{"value":get_words()},
  "rain_odds":{"value":50},
}
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("发送了" + str(count) + "条消息")
