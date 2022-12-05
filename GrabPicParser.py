from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json
import time
from aiogram import Bot, types
import os
import asyncio

config = json.load(open('config.json','r'))
API_TOKEN = config['bot_token']
CHANNEL_ID = config['channel_id']

# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
print("start")

try:
    url = "https://www.bybit.com/en-US/nft/grabpic/"
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s)#, options=options)
    driver.get(url=url)
    time.sleep(5)

    with open("grabpic.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    with open("grabpic.html", "r", encoding="utf-8") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    new_cards = soup.find_all(class_="card-wrapper")
    
    for item in new_cards:
        print("start loop")
        grabpic_link = "https://www.bybit.com" + item.find(class_="card-item").get("href")
        print(grabpic_link)

        with open("grabpic_link.txt", "r", encoding="utf-8") as file:
            all_links = file.read()

        if grabpic_link in all_links:
            print("already exist")
            print(grabpic_link)
        else:
            # url = grabpic_link
            # s = Service("chromedriver.exe")
            # driver = webdriver.Chrome(service=s)#, options=options)
            # driver.get(url=url)
            # time.sleep(5)

            # with open("grabpic.html", "w", encoding="utf-8") as file:
            #     file.write(driver.page_source)

            # with open("grabpic.html", "r", encoding="utf-8") as file:
            #     src = file.read()

            # card_data = BeautifulSoup(src, "lxml")
            #print(src)
            #print(item)
            img_link = item.find(class_="el-image__inner").get("src")
            print("Img_link " + img_link)
            title = item.find("h3").text
            print("Title " + title)
            #value = item.find(class_="right flex-row flex-items-center")
            #print(value.text)
            price = item.find(class_="right flex-row flex-items-center").find(class_="gray").text
            price = price.replace("(", "")
            price = price.replace(")", "")
            print("Price " + price)
            date1 = item.find(class_="countdown-time right flex-row flex-items-center")
            print(date1)
            date = date1.find_all("span")
            days = date[0].text
            days = days.replace("d", " days")
            hours = date[1].text
            hours = hours.replace("h", " hours")
            print("Date " + date)

            with open("grabpic_link.txt", "a", encoding="utf-8") as file:
                file.write(grabpic_link + "\n")
            print("save link in file")

            text_message_GP = hide_link(img_link) + '#GrabPic\n🔸' + title + '\n▪️' + grabpic_link + '\n▪️Price: ' + price + ' USDT\n▪️Starts in: ' + days + hours
            #text_message_GP = (f'#GrabPic\n🔸<b>{title}</b>\n▪️{grabpic_link}\n▪️Price: {price} USDT\n▪️Starts in: {date[0].text} day {date[1].text} hours {date[2].text} minutes')
            #print(text_message_GP)
            print("start TG")

            bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

            async def send_message(channel_id: int, text: str):
                await bot.send_message(channel_id, text)

            async def main():
                await send_message(CHANNEL_ID, text_message_GP)

            if __name__ == '__main__':
                asyncio.run(main())
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
