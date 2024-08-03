import requests
from bs4 import BeautifulSoup

def check_weather(city):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    responce = requests.get(f"https://www.google.com/search?q=погода+в+{city}+на+сегодня", headers=headers)
    soup = BeautifulSoup(responce.text, "html.parser")
    rain_chance = soup.select("#wob_pp")[0].getText()
    temperature = soup.select("#wob_tm")[0].getText()
    title = soup.select("#wob_dc")[0].getText()
    humidity = soup.select("#wob_hm")[0].getText()
    time = soup.select("#wob_dts")[0].getText()
    wind = soup.select("#wob_ws")[0].getText()

    weather = f'На сегодня погода в городе {city} следующая:\n\nТемпература: {temperature}°\n{title}\nВероятность осадков: {rain_chance}\nВлажность воздуха: {humidity}\nСкорость ветра: {wind}'
    return weather