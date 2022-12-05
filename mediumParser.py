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

options = webdriver.ChromeOptions()
# options.add_argument("--headless")

try:
    urls = ["https://medium.com/tag/testnet/latest", "https://medium.com/tag/airdrop/latest"]

    temp = {}
    with open("medium_dict.json", "r", encoding="utf-8") as file:
        medium_dict = json.load(file)

    for url in urls:
        s = Service("chromedriver.exe")
        driver = webdriver.Chrome(service=s, options=options)
        driver.get(url=url)
        time.sleep(3)

        with open("medium.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open("medium.html", "r", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        articles = soup.find_all("article")

        for item in articles:
            #print(item)
            article_links = item.find_all("a")
            http = "medium.com"
            if http in article_links[2].get("href"):
                article_link = article_links[2].get("href")
                article_link = article_link[:article_link.rindex('?source=')]
            else:
                article_link = "https://medium.com" + article_links[2].get("href")
                article_link = article_link[:article_link.rindex('?source=')]

            if article_link in medium_dict:
                print("The link is already in the dictionary")
            else:
                print("New, added " + article_link)
                title = item.find("h2").text
                medium_dict[article_link] = title
                temp[article_link] = title

    with open('medium_dict.json', 'w', encoding="utf-8") as file:
        json.dump(medium_dict, file, indent=4, ensure_ascii=False)

        if temp:
            text_message_MED = "New articles in Medium \n\n"

            for key, value in temp.items():
                text_message_MED = text_message_MED + '▪' + value + '\n' + key + '\n\n'

            bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

            async def send_message(channel_id: int, text: str):
                await bot.send_message(channel_id, text)

            async def main():
                await send_message(CHANNEL_ID, text_message_MED)

            if __name__ == '__main__':
                asyncio.run(main())
        else:
            print("no new articles")

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()