import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


#https://api.openweathermap.org/data/2.5/weather?q=London,UK&appid=6d428b71340665c52f9bc134a2a9630e

account_sid = ""
auth_token = ""

OWN_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
api_key = ""

weather_params = {
    "lat": 43.874168,
    "lon": -79.258743,
    "appid": api_key,
    "cnt":4,
}

response = requests.get(OWN_Endpoint,params=weather_params)
response.raise_for_status()
weather_data=(response.json())
#print(weather_data["list"][0]["weather"][0])
will_rain = False
for hour_data in weather_data["list"]:
    condition_code =  hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
   #print("Yahoo")
   proxy_client = TwilioHttpClient()
   proxy_client.session.proxies = {
       'https': os.environ['https_proxy']
   }
   client = Client(account_sid, auth_token, http_client=proxy_client)
   message = client.messages\
   .create(
       body="It's gonna rain. Bring your umbrella ☔️!",
       from_="+XXXXXXXXX",
       to="+XXXXXXXXXXX",
   )
   print(message.body)

